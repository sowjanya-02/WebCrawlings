import zipfile
import gzip
import requests
import re
from warcio import ArchiveIterator
import argparse
import json

def fun_format(wet_url):
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
            title = record.content_stream().readline().lower().decode('utf-8')
            m = regex_covid.search(title)
            if m:
                    text = record.content_stream().read().lower().decode('utf-8')
                    if regex_economy.search(text):
                        res = record.rec_headers.get_header('WARC-Target-URI')
                        total_links.append(res)
        except:
                pass
    return total_links

def final_list (wet_urls):
    with gzip.open(wet_urls, 'rb') as f:
        file_content = f.readlines()
    covid_finalurls = []
    for reformatted_lines in file_content:
            s = reformatted_lines.decode('utf-8').strip()
            print (s)
            s1 = "http://commoncrawl.s3.amazonaws.com/{}".format(s)
            res1 = fun_format(s1)
            covid_finalurls += res1
    return covid_finalurls

if __name__  == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--uri',
                       required=True)
    args = parser.parse_args()
    json_file = {'Jan 2020': final_list(args.uri)}
    print (len(json_file['Jan 2020']))

    with open('data_jan.json', 'w') as f:
        json.dump(json_file, f)




