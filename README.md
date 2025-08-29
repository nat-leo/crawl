# crawl

Welcome to crawl, a scraping and web analysis tool built on common crawl.

Webpages archived on common crawl are vast. The dataset itself is many petabytes - impossible to see or use the whole thing on a Laptop without a personal Data Center and millions in computation. Processing must be done thoughtfully

The dataset has to be queried. There's no good way to download the whole thing, so it's important to know what to look for and when to use it. 

## URLs

This is a CDX URL index
```
https://data.commoncrawl.org/cc-index/collections/CC-MAIN-2025-21/indexes/cdx-00000.gz
```

It's got thousands of these - CDX URL Index Lines
```
0,1,65,159)/ 20250514175125 {"url": "https://159.65.1.0/", "mime": "warc/revisit", "status": "304", "length": "563", "offset": "1945383", "filename": "crawl-data/CC-MAIN-2025-21/segments/1746990412443.21/crawldiagnostics/CC-MAIN-20250514163508-20250514193508-00738.warc.gz"}
```
This is split into important sections:
1. Prefix 
2. Timestamp
3. JSON Object Fields 

### Prefix
`0,1,65,159)/` is the SURT key for sorting and grouping by domain. Read it like `159.65.1.0`. Does that look familiar? It should - it's an IP Address!

### Timestamp
`20250514175125` This is when the crawler indexed this webpage. It's the WARC capure time in 14-digit format. Read it like `2025, May 14th at 5:51pm UTC`

### JSON object fields
This part is machine-readable metadata about the capture:

#### `"url": "https://159.65.1.0/"`
The original URL requested.

#### `"mime": "warc/revisit"`
A revisit record, not a full response. Revisit = instead of storing the whole HTML again, it points back to a previous capture of identical content. Saves storage when a page hasn’t changed.

#### `"status": "304"`
The HTTP response code.
304 Not Modified → server explicitly said content hasn’t changed.
Makes sense why it’s a warc/revisit.

#### `"length": "563"`
Size of this record (in bytes) inside the WARC file.

#### `"offset": "1945383"`
The byte offset inside the WARC file where this record starts.

#### `"filename": "crawl-data/CC-MAIN-2025-21/...00738.warc.gz"`
Which WARC file contains this record.
Prepend https://data.commoncrawl.org/ to get the full URL:
```
https://data.commoncrawl.org/crawl-data/CC-MAIN-2025-21/segments/1746990412443.21/crawldiagnostics/CC-MAIN-20250514163508-20250514193508-00738.warc.gz
```
You can go here to get the webarchived page in raw HTML (WARC). Or you can get the cleaned version (WET) 
