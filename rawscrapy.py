import random, core
import debugger
import bs4.element
from bs4 import BeautifulSoup
from requests import get, post

intercept_cnt = 0
news_content = []




class RawScrapy():
    """
    Scrap with BeautifulSoup and requests without headless browsers
    """

    def __init__(self):
        self.ua_list = core.load_ua()
        self.settings = core.load_settings()
        self.header = {
            'User-Agent': random.choice(self.ua_list),
            'Cookie': self.settings['cookie_yahoo']
        }

    def get_page(self, url: str):

        self.header['Referer'] = url
        response = get(url, headers=self.header)
        soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')
        title = soup.find('h1', class_="title-article").text.strip()
        datetime = soup.find('time').text.strip()

        news_content.append({
            'url': url,
            'title': title,
            'datetime': datetime,
            'body': "",
        })
        main_content = soup.find(class_='p-main-contents')

        for child in main_content.children:
            # print(type(child))
            if type(child) == bs4.element.NavigableString:
                continue
            if not child.has_attr('itemprop'):
                continue

            if child.attrs['itemprop'] == 'articleBody':
                news_content[0]['body'] += child.text.strip()
                news_content[0]['body'] += '\n'
            print(news_content[0]['body'])

        # with conn.cursor() as cur:
        #     sql = "INSERT INTO raw(html_content) VALUES ('" + es(content) + "');"
        #     cur.execute(sql)
        # conn.commit()

    def get_contents(self, url: str):

        # cookie = "XA=f7tap6dgc0c76&sd=B&t=1623208166&u=1623208166&v=1; XB=f7tap6dgc0c76&b=3&s=2n; JV=A7PW9GAAAFPfl8jJetBqy41Oji6hKHjxPowSVa18LhoCRwricIpBFyx38AEyyBKB5QVCHFUC6EKtw4Td_H7BaPd45Fr861x0ZCYsO3qO3ba3ZzMYkdFfIJtlBWKSijRdXut24-w8gpHOoP8TMv9UnElNxalVXUEoULyWkovXCe6pwFJ22VGXAQFoIYLU3TbM-_jcwBb194C8eB9skACplhDbfP0BnyrgywDITfW9OPLlKFy7y0MaJWEaFEYDUGg4iTQ9sS2F3PbVbxYaETlWC3hICs7Folr5aFYm_ZFWWiDFUcc_73qypuFIZn6mNHJueCaQb8rSq-VvuQPLBG5Sk-7SBHW-qEzwPfxeFA9t6GE2rhis-qptWb2gUF4agoPTLr-oGyFSRNYRQiqNa1SjEAb4Dd0Zxq7xFqzLV4Im7NFE5L1aYKzUt0E5GkHyCuByYDMAckSpvej1QRxUD-5qqJ_9O5AsOOTF4vs98lsXNB3Zx2p9aLOar5hiOvOwU4ftE2I01mqXwY1jksh8kNExyjEoO1UE9MkQktGoPyPEnLYuV5zMwIgD8BJ8pgbuwCea2tgfEuaQ0wg5DGflMuaN-eh_IAb38Bidaw8_fVEGnkGL4r7hIOIJ42JPOUXbb4I3x6wkDBKUTRXU0BwLkMMv68G1Q1Vc&v=2; A=f7tap6dgc0c76&sd=B&t=1623208166&u=1623208166&v=1"
        # self.header['Cookie'] = cookie

        for start_ in range(1, 50, 4045):
            content_url = url.replace("_START_", str(start_))
            response_content = get(content_url, headers=self.header)
            print(response_content)

        # response = get(url, headers=self.header)
