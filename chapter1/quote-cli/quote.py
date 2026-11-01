"""명언 CLI: 인수 없이 실행하면 무작위 명언을, --list를 주면 전체 목록을 출력합니다."""

import argparse
import json
import random
import sys
from pathlib import Path

QUOTES_FILE = Path(__file__).with_name("quotes.json")


def load_quotes(path=QUOTES_FILE):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def format_quote(quote):
    return f'"{quote["text"]}" - {quote["author"]}'


def main(argv=None):
    parser = argparse.ArgumentParser(description="명언을 출력합니다.")
    parser.add_argument("--list", action="store_true", help="전체 명언 목록을 출력합니다.")
    args = parser.parse_args(argv)

    # Windows 콘솔에서도 한글이 깨지지 않도록 UTF-8로 출력
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    try:
        quotes = load_quotes()
    except (OSError, json.JSONDecodeError) as e:
        print(f"명언 파일을 읽을 수 없습니다: {e}", file=sys.stderr)
        return 1

    if not quotes:
        print("등록된 명언이 없습니다.", file=sys.stderr)
        return 1

    if args.list:
        for i, quote in enumerate(quotes, 1):
            print(f"{i}. {format_quote(quote)}")
    else:
        print(format_quote(random.choice(quotes)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
