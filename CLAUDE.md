# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 언어 규칙

모든 대화와 커밋 메시지는 한국어로 작성한다.

## 디자인 규칙

버튼은 연보라(`#bb8cff`) 배경, 둥근 모서리 `border-radius: 12px`.

## 저장소 구성

바이브 코딩 연습용 저장소. 빌드 시스템, 패키지 매니저, 테스트 스위트는 없다 — 실행할 lint/build/test 명령이 없다.

- `index.html` — 단일 파일 자기소개 페이지 (인라인 `<style>`, 외부 의존성 없음). 브라우저로 직접 열어 확인한다.
- `page-tools/skills/page-check/` — HTML 점검 스킬 (page-tools 플러그인으로 포장돼 있다) (title / 내부 링크 / img alt / viewport / UTF-8 5개 항목을 🔴🟡🟢로 보고)
- `.claude/agents/` — `page-checker` (page-check 스킬로 점검, 수정 안 함), `copy-helper` (문구 개선안 제안, 수정 안 함)

두 에이전트 모두 읽기 전용이다. 수정은 사용자가 요청할 때 메인 세션에서 한다.
