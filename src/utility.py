import dataclasses
import json
from datetime import datetime
from pathlib import Path
from typing import TypeVar

T = TypeVar("T")


def ism_date(input_date: str) -> str:
    """日付文字列を指定のフォーマットに変換する"""
    naive_datetime = datetime.strptime(input_date, "%Y/%m/%d")  # noqa: DTZ007
    return naive_datetime.strftime("%Y-%m-%d %H:%M:%S")


def to_json(data: list[T]) -> str:
    """データクラスのリストをJSON形式に変換する"""
    return json.dumps([dataclasses.asdict(item) for item in data], ensure_ascii=False, indent=2)


def save_json(data: list[T], path: str = "example.json") -> None:
    """データクラスのリストをJSONファイルに保存する"""
    with Path(f"./data/{path}").open("w", encoding="utf-8") as f:
        json.dump([dataclasses.asdict(item) for item in data], f, ensure_ascii=False, indent=2)
