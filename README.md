# Sino-Jap-SRT
A simple scrawler for the srt project, mainly for Yomiuri news and Yahoo news Japan

## Build
You need to put the corresponding chromedriver at the root path of this project, and need to install the dependendies yourself.
They include but not limited to:
+ selenium
+ beautifulsoup4
+ ...
You can easily see the detail in the source code.

## Use
In main.py, set the arguments of `get_new_content()`, and the search result of those keywords of Yahoo News will be returned as the content.
Then, it will automatically get all the articles in the content.

The content and all the articles will be saved in ./resources as json files.

## TODO:
+ Implement getting the comments of each article
+ Implement the search limiting the date range and keywords