import random, math

import requests.exceptions

from utils import core, debugger
import bs4.element
from bs4 import BeautifulSoup
from requests import get

intercept_cnt = 0
news_content = []

class RawScrapy():
    """
    Scrap with BeautifulSoup and requests without headless browsers
    """

    def __init__(self, site: str):
        self.ua_list = core.load_ua()
        self.settings = core.load_settings()
        self.header = {
            'User-Agent': random.choice(self.ua_list),
            'Cookie': self.settings['cookie_yahoo']
        }
        if site == "yomiuri":
            self.header['Cookie'] = self.settings['cookie_yomiuri']

        self.comment_params = {
            "origins": "https://news.yahoo.co.jp",
            "sort": "lost_points",
            "order": "desc",
            "page": "1",
            "type": "t",
            "topic_id": "",
            "space_id": "",
            "content_id": "",
            "full_page_url": "",
            "comment_num": "10",
            "ref": "",
            "bkt": "",
            "flt": 2,
            "grp": "",
            "opttype": "",
            "disable_total_count": "",
            "compact": "",
            "compact_initial_view": "",
            "display_author_banner": "off",
            "mtestid": "",
            "display_blurred_comment": "",
        }

    def get_page_for_yomiuri(self, url: str):

        self.header['Referer'] = url
        response = get(url, headers=self.header)
        soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')
        # title = soup.find('h1', class_="title-article").text.strip()
        # datetime = soup.find('time').text.strip()

        # news_content.append({
        #     'url': url,
        #     'title': title,
        #     'datetime': datetime,
        #     'body': "",
        # })
        main_content = soup.find(class_='p-main-contents')
        body = ""
        for child in main_content.children:
            # print(type(child))
            if type(child) == bs4.element.NavigableString:
                continue
            if not child.has_attr('itemprop'):
                continue

            if child.attrs['itemprop'] == 'articleBody':
                body += child.text.replace('\n', '')
                body += '\n'
                # print(body + "\n ========\n")
        return body

        # with conn.cursor() as cur:
        #     sql = "INSERT INTO raw(html_content) VALUES ('" + es(content) + "');"
        #     cur.execute(sql)
        # conn.commit()

    def get_contents_for_yomiuri(self, url: str):

        # cookie = "XA=f7tap6dgc0c76&sd=B&t=1623208166&u=1623208166&v=1; XB=f7tap6dgc0c76&b=3&s=2n; JV=A7PW9GAAAFPfl8jJetBqy41Oji6hKHjxPowSVa18LhoCRwricIpBFyx38AEyyBKB5QVCHFUC6EKtw4Td_H7BaPd45Fr861x0ZCYsO3qO3ba3ZzMYkdFfIJtlBWKSijRdXut24-w8gpHOoP8TMv9UnElNxalVXUEoULyWkovXCe6pwFJ22VGXAQFoIYLU3TbM-_jcwBb194C8eB9skACplhDbfP0BnyrgywDITfW9OPLlKFy7y0MaJWEaFEYDUGg4iTQ9sS2F3PbVbxYaETlWC3hICs7Folr5aFYm_ZFWWiDFUcc_73qypuFIZn6mNHJueCaQb8rSq-VvuQPLBG5Sk-7SBHW-qEzwPfxeFA9t6GE2rhis-qptWb2gUF4agoPTLr-oGyFSRNYRQiqNa1SjEAb4Dd0Zxq7xFqzLV4Im7NFE5L1aYKzUt0E5GkHyCuByYDMAckSpvej1QRxUD-5qqJ_9O5AsOOTF4vs98lsXNB3Zx2p9aLOar5hiOvOwU4ftE2I01mqXwY1jksh8kNExyjEoO1UE9MkQktGoPyPEnLYuV5zMwIgD8BJ8pgbuwCea2tgfEuaQ0wg5DGflMuaN-eh_IAb38Bidaw8_fVEGnkGL4r7hIOIJ42JPOUXbb4I3x6wkDBKUTRXU0BwLkMMv68G1Q1Vc&v=2; A=f7tap6dgc0c76&sd=B&t=1623208166&u=1623208166&v=1"
        # self.header['Cookie'] = cookie

        content_url = url + ("&paged=%d" % 1)
        response_content = get(content_url, headers=self.header)
        soup = BeautifulSoup(response_content.content.decode('utf-8'), 'lxml')
        num = soup.find(class_="search-result").span.text.strip()
        num0 = math.ceil(int(num) / 20)
        debugger.INFO("Find {} results".format(num))
        url_list = []
        contents = soup.find_all(class_="p-list-item__inner")
        for content in contents:
            content0 = content.find(class_="c-list-title").a
            content_title = content0.text.strip()
            content_url = content0['href']
            content_time = content.find(class_="c-list-date").time.text.strip()
            url_list.append({
                "title": content_title,
                "time": content_time,
                "url": content_url,
            })
        debugger.INFO("get 1st page of contents!")
        for i in range(2, num0 + 1):
            content_url = url + ("&paged=%d" % i)
            response_content = get(content_url, headers=self.header)
            soup = BeautifulSoup(response_content.content.decode('utf-8'), 'lxml')
            contents = soup.find_all(class_="p-list-item__inner")
            for content in contents:
                content0 = content.find(class_="c-list-title").a
                content_title = content0.text.strip()
                content_url = content0['href']
                content_time = content.find(class_="c-list-date").time.text.strip()
                url_list.append({
                    "title": content_title,
                    "time": content_time,
                    "url": content_url,
                })
            debugger.INFO("get {}th page of contents!".format(i))
        return url_list
        # response = get(url, headers=self.header)

    def get_comment_for_yahoo(self, url: str):

        self.header['Referer'] = url
        if url.find("articles") == -1:
            debugger.WARNING("No comments!")
            return ""
        # print(url)
        try:
            response = get(url, headers=self.header)
        except requests.exceptions.ProxyError:
            debugger.ERROR("ConnectionResetError!")
            return ""
        soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')
        # print(soup)

        news_comment_plugin = soup.find(class_="news-comment-plugin")

        try:
            data_topic_id = news_comment_plugin["data-topic-id"]
            data_space_id = news_comment_plugin["data-space-id"]
            data_full_page_url = news_comment_plugin["data-full-page-url"]
        except TypeError:
            try:
                data_topic_id = news_comment_plugin["data-topic-id"]
                data_space_id = news_comment_plugin["data-space-id"]
                data_full_page_url = news_comment_plugin["data-full-page-url"]
            except TypeError:
                debugger.WARNING("Zero comments!")
                return ""

        bkt = "art62t1"
        mtestid = "mfn_15510=art62t1"
        comment_base_url = "https://news.yahoo.co.jp/comment/plugin/v1/full/"
        params = self.comment_params
        params["topic_id"] = data_topic_id
        params["space_id"] = data_space_id
        params["full_page_url"] = data_full_page_url
        params["bkt"] = bkt
        params["mtestid"] = mtestid

        response = get(comment_base_url, headers=self.header, params=params)
        soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')

        comment_list = soup.find(id="comment-list-item")
        comments_ret = ""
        # print(comment_list.contents[0])
        if comment_list is None:
            return ""

        for comment_item in comment_list.children:
            if type(comment_item) == bs4.element.NavigableString:
                continue
            # print(comment_item)
            name = comment_item.find(class_="name").text.strip()
            cmtBody = comment_item.find(class_="cmtBody").text.strip()
            good = comment_item.find(class_="good").find(class_="userNum").text.strip()
            bad = comment_item.find(class_="bad").find(class_="userNum").text.strip()
            comments_ret += "%s vs %s:\n" % (good, bad)
            comments_ret += "%s\n\n" % (cmtBody)

        return comments_ret
        # print(soup)