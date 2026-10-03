# vibe-week3

바이브 코딩 3주차 연습 저장소. 자기소개 페이지 하나와, 그 페이지를 점검·관리하는 도구들이 들어 있다.

👉 **https://tlarkdus.github.io/vibe-week3/**

## 오늘의 한마디

<!-- QUOTE:START -->
막힐 땐 잠깐 쉬어도 괜찮아.
<!-- QUOTE:END -->

## index.html

자기소개 페이지. 외부 라이브러리 없이 파일 하나로 굴러간다. 브라우저로 직접 열어 확인한다.

기분 버튼과 다크모드 토글이 있다.

## 도구

- `page-tools/skills/page-check/` — HTML을 title·내부 링크·이미지 alt·viewport·UTF-8 5개 관점으로 점검하는 스킬 (플러그인으로 포장)
- `.claude/agents/` — `page-checker`(위 스킬로 점검), `copy-helper`(문구 개선안 제안). 둘 다 읽기 전용이다
- `.claude/hooks/worklog.sh` — 작업 한 턴이 끝날 때마다 `.claude/worklog.txt`에 기록을 남기는 Stop 훅
- `.github/workflows/daily-hello.yml` + `update_quote.py` + `quotes.txt` — 매일 위 '오늘의 한마디'를 무작위로 갈아 끼우고 자동 커밋하는 GitHub Actions
