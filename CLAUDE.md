# CLAUDE.md

이 저장소에서 작업할 때 지킬 것.

절대 위반 금지 규칙: @GOLDEN_RULES.md

## 언어

모든 대화와 커밋 메시지는 한국어로 작성한다.

## 파일 배치

- 페이지는 저장소 루트에 HTML 한 장씩. CSS는 `<style>`, JS는 `<script>`로 같은 파일 안에 둔다.
  공통 스타일시트나 `.js` 파일로 분리하지 않는다.
- **'오늘의 한마디' 후보 문구는 `quotes.txt`에만 둔다.** 한 줄에 하나. 다른 파일에 복사해 두지 않는다.
  `README.md`에 보이는 문구는 `update_quote.py`가 `quotes.txt`에서 골라 넣은 결과다.
- 점검 도구는 `page-tools/skills/`, 에이전트는 `.claude/agents/`.
- `.claude/worklog.txt`와 `.claude/settings.local.json`은 `.gitignore` 대상 — 커밋하지 않는다.

## 스타일

- 색은 각 파일 `:root`의 CSS 변수로 정의하고 그 변수만 쓴다. 색상 코드를 본문에 직접 박지 않는다.
- 버튼은 연보라(`#bb8cff`) 배경에 `border-radius: 12px`.
- 모든 페이지에 `<html lang="ko">`, `<meta charset="UTF-8">`, viewport 메타를 넣는다.
- 접근성 기본은 빼지 않는다: `<img>`의 `alt`, 아이콘 버튼의 `aria-label`,
  `:focus-visible` 윤곽선, `@media (prefers-reduced-motion: reduce)`.

## 고친 뒤 확인

빌드·lint·테스트 명령이 없다. 대신:

1. 브라우저로 해당 HTML을 직접 열어 확인한다.
2. `page-check` 스킬로 점검한다 (title / 내부 링크 / img alt / viewport / UTF-8).
3. 입력을 다루거나 저장하는 코드를 건드렸으면 `security-check` 스킬도 돌린다
   (하드코딩된 비밀값 / innerHTML XSS / console.log 노출 / http:// 요청).

## 페이지

- `index.html` — 자기소개. 기분 버튼, 다크모드 토글. 다크모드는 `:root` 변수 세트를 바꾸는 방식.
- `expense.html` — 미니 가계부 분석기. 항목 추가·삭제·합계. 금액은 정수, `toLocaleString('ko-KR')`로 표시.
- `secret.html` — 보안 실습용 비밀 메모장. **의도적으로 클라이언트 전용**이라 한계가 있고,
  코드 안 `ponytail:` 주석에 그 한계와 업그레이드 경로가 적혀 있다. 실제 인증 용도로 쓰지 않는다.

## 에이전트

`.claude/agents/`의 `page-checker`, `copy-helper`는 **읽기 전용**이다. 점검·제안만 하고 파일을 고치지 않는다.
수정은 사용자가 요청할 때 메인 세션에서 한다.
