"""quote.py와 quotes.json의 동작을 검증하는 테스트."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

import quote

SCRIPT = Path(__file__).with_name("quote.py")
QUOTES_FILE = Path(__file__).with_name("quotes.json")


@pytest.fixture
def quotes():
    with open(QUOTES_FILE, encoding="utf-8") as f:
        return json.load(f)


def run_cli(*args):
    """실제 CLI처럼 quote.py를 별도 프로세스로 실행하고 결과를 돌려준다."""
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        encoding="utf-8",
    )


# --- quotes.json 데이터 검증 ---

def test_quotes_json_is_non_empty_list(quotes):
    assert isinstance(quotes, list)
    assert len(quotes) > 0


def test_each_quote_has_text_and_author(quotes):
    for q in quotes:
        assert isinstance(q.get("text"), str) and q["text"].strip()
        assert isinstance(q.get("author"), str) and q["author"].strip()


def test_load_quotes_matches_json(quotes):
    assert quote.load_quotes() == quotes


# --- 인수 없이 실행 ---

def test_no_args_prints_one_line():
    result = run_cli()
    assert result.returncode == 0
    lines = result.stdout.splitlines()
    assert len(lines) == 1


def test_no_args_prints_a_known_quote(quotes):
    result = run_cli()
    expected = {quote.format_quote(q) for q in quotes}
    assert result.stdout.strip() in expected


def test_no_args_uses_random_choice(monkeypatch, capsys, quotes):
    monkeypatch.setattr(quote.random, "choice", lambda seq: seq[-1])
    assert quote.main([]) == 0
    assert capsys.readouterr().out.strip() == quote.format_quote(quotes[-1])


# --- --list 실행 ---

def test_list_prints_all_quotes(quotes):
    result = run_cli("--list")
    assert result.returncode == 0
    lines = result.stdout.splitlines()
    assert len(lines) == len(quotes)


def test_list_prints_numbered_quotes_in_order(quotes):
    result = run_cli("--list")
    lines = result.stdout.splitlines()
    for i, (line, q) in enumerate(zip(lines, quotes), 1):
        assert line == f"{i}. {quote.format_quote(q)}"


# --- 포맷과 오류 처리 ---

def test_format_quote():
    q = {"text": "포스가 함께하기를.", "author": "〈스타워즈〉"}
    assert quote.format_quote(q) == '"포스가 함께하기를." - 〈스타워즈〉'


def test_empty_quotes_returns_error(monkeypatch, capsys):
    monkeypatch.setattr(quote, "load_quotes", lambda: [])
    assert quote.main([]) == 1
    assert "등록된 명언이 없습니다" in capsys.readouterr().err


def test_missing_file_returns_error(monkeypatch, capsys):
    def raise_missing():
        raise FileNotFoundError("quotes.json")

    monkeypatch.setattr(quote, "load_quotes", raise_missing)
    assert quote.main([]) == 1
    assert "명언 파일을 읽을 수 없습니다" in capsys.readouterr().err
