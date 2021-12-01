from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils import debugger
import time


class SelScrapy():
    """
    Scrap with selenium and headless chrome
    """

    def __init__(self, headless=True):
        self.chrome_options = Options()

        if headless == True:
            self.chrome_options.add_argument("--headless")
            self.chrome_options.add_argument("--disable-gpu")

        self.driver = webdriver.Chrome(executable_path="./scrawler/chromedriver", options=self.chrome_options)
        self.driver.set_page_load_timeout(5)

        self.get_page_num = 0

    def get_contents_for_yahoo(self, *args: str, getall=False) -> list:
        """Search keywords in Yahoo News

        You can input the keywords to search like in browsers

        :param args: keywords in utf-8
        :return: a list of title and url
        """
        keywords = ""
        for arg in args:
            keywords += arg + ' '
        query_url = "https://news.yahoo.co.jp/search?p={}&ei=utf-8".format(keywords)
        debugger.INFO(query_url)

        start_time = time.time()
        debugger.INFO("get_contents by selenium started.")
        try:
            self.driver.get(query_url + "/")
        except TimeoutException:
            self.driver.execute_script("window.stop();")
        debugger.INFO("contents got by {:.2f}s.".format(time.time() - start_time))

        # get the number of results
        # nums0 = self.driver.find_element_by_class_name("sc-gtGrDH").text
        nums0 = self.driver.find_element_by_class_name("sc-bmlaxJ").text
        # debugger.DEBUG(nums0)
        nums = ""
        for num in nums0:
            if num.isdigit():
                nums += num
        # print()
        nums = int(nums)

        debugger.INFO("got {} results".format(nums))

        # click mottomiru until unable to click more
        if getall == True:
            i = 1
            try:
                # mottomiru0 = self.driver.find_element_by_class_name("sc-emWXYZ")
                mottomiru0 = self.driver.find_element_by_class_name("sc-eydyIs")
                mottomiru0.click()
                # debugger.INFO("clicked {} times".format(i))
                i = i + 1
            except NoSuchElementException:
                debugger.DEBUG("No element mottomiru0!")
            time.sleep(0.5)
            sleep_time = 0.2
            while i <= nums / 50:
                try:
                    mottomiru = self.driver.find_element_by_class_name("SearchMore__ButtonWrapper-bAaGOz")
                    mottomiru.click()
                    i = i + 1
                    time.sleep(0.2)
                    sleep_time = 0.2
                except NoSuchElementException:
                    time.sleep(0.2)
                    sleep_time = sleep_time + 0.2
                    # debugger.DEBUG("No element mottomiru!")
                    if sleep_time > 1.5:
                        break

            debugger.INFO("clicked Mottomiru {} times".format(i - 1))

        debugger.INFO("begin getting contents")
        url_list = []
        ol = self.driver.find_element_by_class_name("newsFeed_list")
        for li in ol.find_elements_by_class_name("newsFeed_item-normal"):
            li_title = li.find_element_by_class_name("newsFeed_item_title").text.replace(u'\u3000', u'')
            li_url = li.find_element_by_tag_name("a").get_attribute("href")
            li_time = li.find_element_by_tag_name("time").text
            url_list.append({
                "title": li_title,
                "time": li_time,
                "url": li_url,
            })
            # print(li_url)
        debugger.INFO("got content list")

        self.get_page_num = 0
        # self.driver.close()

        return url_list

    def get_page_for_yahoo(self, url: str) -> str:
        """Get article body for Yahoo news

        :param url: yahoo news article URL
        :return: article body in string
        """
        start_time = time.time()
        debugger.INFO("get_page: {} by selenium started.".format(url))
        try:
            self.driver.get(url + "/")
        except TimeoutException:
            self.driver.execute_script("window.stop();")
        self.get_page_num = self.get_page_num + 1
        debugger.INFO("page {} got by {:.2f}s.".format(self.get_page_num, time.time() - start_time))

        article_body = ""
        try:
            article_body = "  " + self.driver.find_element_by_class_name("sc-etwtAo").text.replace("\n\n", "\n")
        except NoSuchElementException:
            # debugger.DEBUG(url)
            debugger.WARNING("No element {}".format("sc-etwtAo"))
            article_body_elm = ""
            try:
                article_body_elm = self.driver.find_element_by_class_name("articleBody")#.find_element_by_tag_name("div")
            except NoSuchElementException:
                debugger.WARNING("No elm {}".format("articleBody"))
                try:
                    article_body_elm = self.driver.find_element_by_class_name("article_body")
                except NoSuchElementException:
                    debugger.LOG(self.driver.page_source)
                    debugger.WARNING("No elm {}".format("article_body"))
                    return "None"

            article_body_elm = article_body_elm.find_element_by_tag_name("div")
            for p in article_body_elm.find_elements_by_tag_name("p"):
                article_body += "  "
                article_body += p.text
                article_body += "\n"
            debugger.INFO("got~")

        # self.driver.close()
        return article_body

        # print(article_time)
        # print(article_body)

    def get_comment(self, url: str) -> str:
        # start_time = time.time()
        # debugger.INFO("get_comment: {} by selenium started.".format(url))
        # try:
        #     self.driver.get(url + "/")
        # except TimeoutException:
        #     self.driver.execute_script("window.stop();")
        # mottomiru = self.driver.find_element_by_id("loadMoreComments")
        # mottomiru.click()
        # print(self.driver.page_source)
        # wait = WebDriverWait(self.driver, 5)
        # comment_list = wait.until(EC.visibility_of_element_located((By.ID, ""comment-list-item"")))
        # time.sleep(5)
        # print(self.driver.page_source)
        # comment_list = self.driver.find_element_by_id("comment-list-item")
        # print(comment_list)
        #
        # for comment in comment_list:
        #     body = comment.find_element_by_class_name("root")
        #     name = body.find_element_by_class_name("name").find_element_by_class_name("rapidnofollow").text
        #     cmtBody = body.find_element_by_class_name("cmtBody").text
        #     print(cmtBody)
        pass




    def quit(self):
        self.driver.quit()