# from pymysql.converters import escape_string as es
import random, codecs, json
import debugger
import selscrapy, rawscrapy

# conn = core.load_mysql()

def get_new_content():

    fp = codecs.open(json_contents_filename, 'w', 'utf-8')
    contents = sel_scrapy.get_contents_for_yahoo("中国", "五輪", getall=True)

    fp.write(json.dumps(contents, indent=4, separators=(',', ': '), ensure_ascii=False))
    fp.close()
    debugger.INFO("written to json file: {}".format(json_contents_filename))

if __name__ == '__main__':

    debugger.INFO("Hello SRT!")
    yahoo_tyuugoku_gorin = ""
    url = "https://www.yomiuri.co.jp/olympic/2020/20210812-OYT1T50095/"
    sel_scrapy = selscrapy.SelScrapy()
    raw_scrapy = rawscrapy.RawScrapy()

    json_contents_filename = "./resources/contents.json"
    get_new_content()

    fp = codecs.open(json_contents_filename, 'r', 'utf-8')
    contents = json.load(fp, strict=False)
    debugger.INFO("loaded json file: {}".format(json_contents_filename))
    fp.close()

    # sel_scrapy.get_page_for_yahoo(contents[0]["url"])
    debugger.INFO("prepare to get {} pages".format(len(contents)))
    for index, article in enumerate(contents):
        article_body = sel_scrapy.get_page_for_yahoo(contents[index]["url"])
        article["body"] = article_body
    debugger.INFO("got pages finished!")

    json_all_filename = "./resources/all.json"
    fp = codecs.open(json_all_filename, 'w', 'utf-8')
    fp.write(json.dumps(contents, indent=4, separators=(',', ': '), ensure_ascii=False))
    debugger.INFO("written to json file: {}".format(json_all_filename))
    fp.close()

