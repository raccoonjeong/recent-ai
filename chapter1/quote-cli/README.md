# quote-cli

프로그래밍 격언, 우주과학 명언, SF 영화 명대사를 터미널에 출력하는 간단한 CLI입니다.

## 프로젝트 구조

```
quote-cli/
├── quote.py        # CLI 본체
├── quotes.json     # 명언 데이터
├── test_quote.py   # pytest 테스트
└── README.md
```

## 설치

Python 3.7 이상이 필요합니다. `quote.py`는 표준 라이브러리만 사용하므로 별도 패키지 설치 없이 바로 실행할 수 있습니다.

```bash
cd quote-cli
python --version
```

테스트를 실행하려면 pytest를 설치합니다.

```bash
python -m pip install pytest
```

## 사용법

### 무작위 명언 출력

```bash
python quote.py
```

```
"단순함은 신뢰성의 전제 조건이다." - 에츠허르 다익스트라
```

실행할 때마다 다른 명언이 나올 수 있습니다.

### 전체 목록 출력

```bash
python quote.py --list
```

```
1. "말은 쉽다. 코드를 보여 달라." - 리누스 토르발스
2. "섣부른 최적화는 모든 악의 근원이다." - 도널드 커누스
...
15. "그 모든 순간이 시간 속으로 사라지겠지. 빗속의 눈물처럼." - 로이 배티, 〈블레이드 러너〉
```

### 도움말

```bash
python quote.py --help
```

## 명언 추가하기

`quotes.json`에 `text`와 `author`를 가진 항목을 추가하면 됩니다. 파일은 UTF-8로 저장해야 합니다.

```json
[
  {"text": "포스가 함께하기를.", "author": "〈스타워즈〉"}
]
```

## 테스트

```bash
python -m pytest test_quote.py -v
```

테스트는 다음을 확인합니다.

- `quotes.json`이 비어 있지 않고, 모든 항목에 `text`와 `author`가 있는지
- 인수 없이 실행하면 `quotes.json`에 있는 명언이 정확히 한 줄 출력되는지
- `--list`로 실행하면 전체 명언이 번호와 함께 순서대로 출력되는지
- 명언 파일이 없거나 비어 있으면 종료 코드 1과 오류 메시지를 반환하는지
