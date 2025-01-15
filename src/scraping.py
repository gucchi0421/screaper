import dataclasses

import requests
from bs4 import BeautifulSoup

from utility import ism_date, to_json


@dataclasses.dataclass
class Post:
    date: str
    title: str
    content: str


class Scraping:
    def __init__(self, url: str) -> None:
        self.url = url

    def _set_soup(self, url: str) -> BeautifulSoup:
        """ HTMLパーサーの共通化 """
        req = requests.get(url, timeout=60)
        req.encoding = req.apparent_encoding
        return BeautifulSoup(req.text, "html.parser")

    def get_post_urls(
        self, *, link_selector: str, pagination_slug: str | None = None, max_page_num: int | None = None
    ) -> list[str]:
        """
        記事一覧ページから記事詳細ページのURLを取得するメソッドです。
        pagination_slug, max_page_numはオプション引数として必要な場合のみ指定してください。

        Args:
            link_selector(str): 記事詳細ページのURLを取得するためのセレクターを指定します。
            pagination_slug(str): ページが分割されている場合は、それを表すスラッグを指定します。
            max_page_num(int): 分割されている場合の最大ページ数を指定します。

        Returns:
            list[str]: 記事一覧ページから取得したURLのリストを返します。
        """
        return_urls = set()

        try:
            soup = self._set_soup(self.url)
            elements = soup.select(link_selector)
            urls = [
                element.get("href") for element in elements
                if element.get("href") and isinstance(element.get("href"), str)
            ]
            return_urls.update(urls)

            if not pagination_slug or not max_page_num:
                return list(return_urls)

            for i in range(2, max_page_num + 1):
                url = f"{self.url.rstrip('/')}/{pagination_slug}/{i}"
                soup = self._set_soup(url)
                elements = soup.select(link_selector)

                if not elements:
                    print(f"No elements found on page {i}. Stopping.")
                    break

                urls = [
                    element.get("href") for element in elements
                    if element.get("href") and isinstance(element.get("href"), str)
                ]
                return_urls.update(urls)

        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return []

        return list(return_urls)


    def get_post(self, url: str, date_selector: str, title_selector: str, content_selector: str) -> Post:
        """
        記事詳細ページから記事の情報を取得するメソッドです。

        Args:
            url (str): 記事詳細ページのURLを指定します。
            date_selector (str): 記事の日付を取得するためのCSSセレクタを指定します。
            title_selector (str): 記事のタイトルを取得するためのCSSセレクタを指定します。
            content_selector (str): 記事のコンテンツを取得するためのCSSセレクタを指定します。

        Returns:
            Post: 取得した記事の情報を表すPostオブジェクトを返します。
        """
        soup = self._set_soup(url)
        date = soup.select_one(date_selector).text
        title = soup.select_one(title_selector).text
        content = soup.select_one(content_selector).decode_contents()

        return Post(date=ism_date(date), title=title, content=content)


if __name__ == "__main__":
    sc = Scraping(url="http://video-clear.jp/blog")
    post_urls = sc.get_post_urls(link_selector=".textArea > h3 > a")
    if post_urls:
        post = sc.get_post(
            url=post_urls[0],
            date_selector=".date",
            title_selector=".blogContent > h3 > a",
            content_selector=".commentArea",
        )
        print(to_json([post]))
    else:
        print("No posts found.")
