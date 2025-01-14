import os

from dotenv import load_dotenv

from scraping import Scraping
from utility import save_json

load_dotenv()


def main() -> None:
    """
    スクレイピング用のPythonスクリプトです。
    記事一覧ページから記事詳細ページのURLを取得し、記事詳細ページから記事の情報を取得します。
    デフォルトではJSON形式で保存、オプションで標準出力に出力できます。

    url: str
    ・記事一覧ページのURL

    link_selector: str
    ・記事一覧ページから記事詳細ページのURLを取得するためのCSSセレクター

    pagination_slug: str | None
    ・デフォルト: None
    ・オプション: 分割されている場合のスラッグ(例: https://example/blog/page/2 ← これのpageが該当します。)

    max_page_num: int | None
    ・デフォルト: None
    ・オプション: 分割されている場合の最大ページ数(一覧ページが/page/20まで存在刷り場合は20を指定します。)

    date_selector: str
    ・記事詳細の日付を取得するためのCSSセレクター

    title_selector: str
    ・記事詳細のタイトルを取得するためのCSSセレクター

    content_selector: str
    ・記事詳細の日付、タイトル、コンテンツを取得するためのCSSセレクター

    path: str
    ・デフォルト: "example.json"
    ・保存するJSONファイルのパス
    """

    if not os.getenv("URL"):
        print("URL is not set.")
        return

    url = os.getenv("URL")
    sc = Scraping(url=url)
    post_urls = sc.get_post_urls(link_selector=".textArea > h3 > a", pagination_slug="page", max_page_num=20)

    if not post_urls:
        print("No posts found.")
        return

    posts = []
    for url in post_urls:
        print(f"Target URL: {url}")
        post = sc.get_post(
            url=url, date_selector=".date", title_selector=".blogContent > h3 > a", content_selector=".commentArea"
        )
        posts.append(post)

    if posts:
        save_json(data=posts, path="posts.json")
    else:
        print("No posts found.")


if __name__ == "__main__":
    main()
