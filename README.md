# WebCrawlings

Researched on WAT, WET, and WARC formate to understand about the response and content returned by them. As WARC has whole webpage content I didn't choose it for this process as searching the HTML pages would be computationally heavy and more time consumption.

Usually, for data processing like this it is better to choose distibuting computing frameworks like Apache Spark, however because of time limitation to set-up the spark I chose the cocurrent programming for processing the data.

Approach:

  As WET files are segragated by month, I launched an individual process for each month. For example: process #1 process the data for month Jan and writes the output to output-jan.json 
  
  At first, we check if the page title has the covid keyword.
  If yes, then we do the regex search on the page text content to see if it has any economy related keywords.
  
Flaws During tests:

    1) Initially tested with threading which results in blocking the requests.
    2) Searched inside the text content using warc which results in a latency.
