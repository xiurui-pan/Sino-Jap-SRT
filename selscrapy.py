from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import *
import debugger
import time


class SelScrapy():
    """
    Scrap with selenium and headless chrome
    """

    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")

        self.driver = webdriver.Chrome(executable_path="./chromedriver", options=self.chrome_options)
        self.driver.set_page_load_timeout(3)

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
        nums0 = self.driver.find_element_by_class_name("sc-gtGrDH").text
        nums = ""
        for num in nums0:
            if num.isdigit():
                nums += num
        nums = int(nums)

        debugger.INFO("got {} results".format(nums))

        # click mottomiru until unable to click more
        if getall == True:
            i = 1
            try:
                mottomiru0 = self.driver.find_element_by_class_name("sc-emWXYZ")
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
            debugger.DEBUG(url)
            debugger.ERROR("No element {}".format("sc-etwtAo"))

        return article_body

        # print(article_time)
        # print(article_body)

    def close(self):
        self.driver.close()