LRU Cache Project

LRU Cache
Add memory management

1. Upon running, creates a folder “cache” if it doesn’t already exist
2. Remove stuff from cache based on “Last Opened” timestamp on files

1. Keep counter for memory usage according to system’

Input: files to download from the Internet
Then: wget them off the Internet X
Then: save to cache


Later: add authentication features


To executable: list of cache folders to create

Will require some flags

./main:
-c (args to mkdir.py) -u (ordered pairs (URL, cache))

Args to mkdir.py:
- None
- A single number
- A list of ordered pairs x1,y1 x2,y2 where y is memory size of cache, set to 500 MB by default, store this value in file “.size”

LRUcache.py: works with caches one-by-one to prevent memory overload. That is, for each (URL, cache), it opens cache, adds file, deletes LRU files until memory is low enough

- Later on: add caches with automatic web scraping features (e.g., for arxiv, twitter accounts, etc); use flag -s for this


LIST OF FLAGS:
-r remove
-f force to remove
-c cache creation
-s scrape

TODO:
- make all files read-only when in the simulated shell
