import zipfile
import gzip
import requests
import re
from warcio import ArchiveIterator
import argparse
import json

def retreive_covidurl(wet_url):
    regex_covid = re.compile("(covid|corona|pandemic|covid-19)")
    regex_economy = re.compile(
        "(economy|revenue|profit|profits|financial|wealth|shops|tax|money|salary|wage|crisis|jobs|housing|market|income|business|businesses|buy)")
    #wet_url = warc_url.replace('/warc/', '/wet/').replace('warc.gz', 'warc.wet.gz')
    #wat_url = warc_url.replace('/warc/', '/wat/').replace('warc.gz', 'warc.wat.gz')
    r = requests.get(wet_url, stream=True)
    records = ArchiveIterator(r.raw)
    total_links = []
    for record in records:
        try:
            title = str(record.content_stream().readline()).lower()
            m = regex_covid.search(title)
            if m:
                    text = str(record.content_stream().read()).lower()
                    if regex_economy.search(text):
                        res = record.rec_headers.get_header('WARC-Target-URI')
                        total_links.append(res)
        except:
                pass
    return total_links

def total_archeivescovidurls(wet_urls):
    with gzip.open(wet_urls, 'rb') as f:
        file_content = f.readlines()
    covid_finalurls = []
    for line in file_content:
            s = line.decode('utf-8').strip()
            formatted_line = "http://commoncrawl.s3.amazonaws.com/{}".format(s)
            result = retreive_covidurl(formatted_line)
            covid_finalurls += result
    return covid_finalurls

if __name__  == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--uri',
                       required=True)
    parser.add_argument('--uri_out',
                       required=True)
    parser.add_argument('--month_name',
                       required=True)
    args = parser.parse_args()
    json_file = {'{} 2020'.format(args.month_name): total_archeivescovidurls(args.uri)}
    with open(args.uri_out, 'w') as f:
        json.dump(json_file, f)




