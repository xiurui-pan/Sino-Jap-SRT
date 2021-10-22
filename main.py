# from pymysql.converters import escape_string as es
import random, codecs, json
import datetime
import debugger
import selscrapy, rawscrapy

# conn = core.load_mysql()


def get_new_content(*args: str):

    global json_contents_filename
    json_contents_filename = "./resources/contents"
    for arg in args:
        json_contents_filename += arg + '_'
    json_contents_filename += str(datetime.datetime.now().strftime('%Y-%m-%d-%H_%M_%S'))
    json_contents_filename += ".json"

    fp = codecs.open(json_contents_filename, 'w', 'utf-8')
    contents = sel_scrapy.get_contents_for_yahoo(*args, getall=True)

    fp.write(json.dumps(contents, indent=4, separators=(',', ': '), ensure_ascii=False))
    fp.close()
    debugger.INFO("written to json file: {}".format(json_contents_filename))

if __name__ == '__main__':

    debugger.INFO("Hello SRT!")
    json_contents_filename = "./resources/contents.json"
    # yahoo_tyuugoku_gorin = ""
    # url = "https://www.yomiuri.co.jp/olympic/2020/20210812-OYT1T50095/"
    sel_scrapy = selscrapy.SelScrapy(headless=True)
    # body = sel_scrapy.get_page_for_yahoo("https://news.yahoo.co.jp/articles/0e327ec61ddd49e1cfa7ff57a8dfd7486560a9cc")
    # print(body)
    # raw_scrapy = rawscrapy.RawScrapy()

    get_new_content("中国", "五輪", "選手")

    fp = codecs.open(json_contents_filename, 'r', 'utf-8')
    contents = json.load(fp, strict=False)
    debugger.INFO("loaded json file: {}".format(json_contents_filename))
    fp.close()

    # sel_scrapy.get_page_for_yahoo(contents[0]["url"])
    debugger.INFO("prepare to get {} pages".format(len(contents)))
    for index, article in enumerate(contents):

        if article["url"].find('image') != -1:
            debugger.INFO("pass an image article")
            continue

        article_body = sel_scrapy.get_page_for_yahoo(contents[index]["url"])
        if article_body == "None":
            article_body = sel_scrapy.get_page_for_yahoo(contents[index]["url"])
            debugger.ERROR("Cannot get this article")

        article["body"] = article_body

    debugger.INFO("got pages finished!")

    json_all_filename = json_contents_filename.replace("contents", "all")
    fp = codecs.open(json_all_filename, 'w', 'utf-8')
    fp.write(json.dumps(contents, indent=4, separators=(',', ': '), ensure_ascii=False))
    debugger.INFO("written to json file: {}".format(json_all_filename))
    fp.close()

    sel_scrapy.quit()

