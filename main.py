# from pymysql.converters import escape_string as es
import codecs, json
import datetime
from utils import debugger
from scrawler import selscrapy
from scrawler.rawscrapy import RawScrapy
from db import sqldb
import time


def get_new_content(*args: str):

    global json_contents_filename
    global contents
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

    fp = codecs.open(json_contents_filename, 'r', 'utf-8')
    contents = json.load(fp, strict=False)
    debugger.INFO("loaded json file: {}".format(json_contents_filename))
    fp.close()


def get_new_pages():
    # sel_scrapy.get_page_for_yahoo(contents[0]["url"])
    debugger.INFO("prepare to get {} pages".format(len(contents)))
    for index, article in enumerate(contents):

        if article["url"].find('image') != -1:
            debugger.INFO("pass an image article")
            continue

        article_body = sel_scrapy.get_page_for_yahoo(contents[index]["url"])
        if article_body == "None":
            article_body = sel_scrapy.get_page_for_yahoo(contents[index]["url"])
            if article_body == "None":
                debugger.ERROR("Cannot get this article")
            else:
                debugger.INFO("Problem solved. Got this article.")

        article["body"] = article_body

    debugger.INFO("got pages finished!")

    json_all_filename = json_contents_filename.replace("contents", "all")
    fp = codecs.open(json_all_filename, 'w', 'utf-8')
    fp.write(json.dumps(contents, indent=4, separators=(',', ': '), ensure_ascii=False))
    debugger.INFO("written to json file: {}".format(json_all_filename))
    fp.close()


def write_to_db(filename: str, tablename: str):

    db = sqldb.Sqldb()

    debugger.INFO("begin writing {} to table {}".format(filename, tablename))
    gen = db.generate("./resources/" + filename, tablename)
    if gen is False:
        debugger.ERROR("Writing to table failed")
    else:
        debugger.INFO("Writing to table succeeded.")

    db.close()

    
def get_comments(filename: str):
    path_contents = "./resources/" + filename
    debugger.INFO("prepare to get comments for {}".format(filename))
    fp = codecs.open(path_contents, 'r', 'utf-8')
    contents = json.load(fp)
    fp.close()
    raw_scrapy = RawScrapy()
    # content = contents[15]
    # url = content["url"]
    # comment = raw_scrapy.get_comment(url + "/comments")
    # content["comment"] = comment
    for (id, content) in enumerate(contents):
        start_time = time.time()
        url = content["url"]
        debugger.INFO("getting {}th comments for {}".format(id, url))
        comment = raw_scrapy.get_comment(url + "/comments")
        content["comment"] = comment
        debugger.INFO("got by {:.2f}s!".format(time.time() - start_time))
    debugger.INFO("Getting comments finished!")
    debugger.INFO("Begin writing to file")

    json_all_filename = path_contents.replace("all", "all_plus")
    fp = codecs.open(json_all_filename, 'w', 'utf-8')
    fp.write(json.dumps(contents, indent=4, separators=(',', ': '), ensure_ascii=False))
    debugger.INFO("written to json file: {}".format(json_all_filename))


if __name__ == '__main__':

    debugger.INFO("Hello SRT!")
    # sel_scrapy = selscrapy.SelScrapy(headless=False)

    # get_new_content("??????", "??????", "??????")

    # get_new_pages()

    get_comments("all??????_??????_??????_2021-12-01-14_16_57.json")

    # write_to_db("all??????_??????_??????_2021-10-22-12_33_35.json", "yahoo_A")

    # sel_scrapy.quit()

