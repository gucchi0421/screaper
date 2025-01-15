import os
import sys

from dotenv import load_dotenv

from scraping import Scraping
from utility import save_json

load_dotenv()


def main() -> None:
    """
    スクレイピング用のPythonスクリプトです。
    記事一覧ページから記事詳細ページのURLを取得し、記事詳細ページから記事の情報を取得します。
    デフォルトではJSON形式で保存、オプションで標準出力に出力できます。

    Variables:
        url(str):
        ・記事一覧ページのURL
        ・例: "https://example/blog"

        link_selector(str):
        ・記事一覧ページから記事詳細ページのURLを取得するためのCSSセレクター
        ・例: ".post-title > a"

        pagination_slug(str|None):
        ・オプション: 一覧ページが分割されている場合の下層のスラッグ
        ・デフォルト: None
        ・例: "https://example/blog/page/2" ← こちらの/page/が該当します。

        max_page_num(int|None):
        ・オプション: 一覧ページが分割されている場合の最大ページ番号
        ・デフォルト: None
        ・例: "https://example/blog/page/2" ← こちらの/2/などのページ番号が該当します。

        date_selector:(str) (str)
        ・記事詳細の日付を取得するためのCSSセレクター
        ・例: ".date"

        title_selector(str):
        ・記事詳細のタイトルを取得するためのCSSセレクター
        ・例: ".content-title > h2"

        content_selector(str):
        ・記事詳細のコンテンツを取得するためのCSSセレクター
        ・例: ".content-body"

        filename(str):
        ・デフォルト: "example"
        ・保存するJSONファイルのパス
    """
    url = os.getenv("TARGET_URL")
    if url is None:
        print("TARGET_URL is not set.")
        sys.exit(1)

    print("Start scraping...")

    sc = Scraping(url=url)
    post_urls = sc.get_post_urls(link_selector=".textArea > h3 > a", pagination_slug="page", max_page_num=20)

    if not post_urls:
        print("No posts found.")
        return

    print(f"\nGet {len(post_urls)} urls\n")

    posts = []
    for url in post_urls:
        print(f"Target: {url}")
        post = sc.get_post(
            url=url, date_selector=".date", title_selector=".blogContent > h3 > a", content_selector=".commentArea"
        )
        posts.append(post)

    print(f"\nScraped {len(posts)} posts")

    if posts:
        filename = "posts"
        save_json(data=posts, filename=filename)
        print(f"\nSent {len(posts)} posts to JSON file: ./data/{filename}.json")
    else:
        print("No posts found.")


if __name__ == "__main__":
    main()
