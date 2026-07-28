# vibe-week3

바이브 코딩 3주차 연습 저장소. 자기소개 페이지 하나와, 그 페이지를 점검·관리하는 도구들이 들어 있다.

## 오늘의 한마디

<!-- QUOTE:START -->
오늘 하루도 잘 해낼 거야.
<!-- QUOTE:END -->

## index.html

심가연(데이터사이언스전공 · 23학번)의 자기소개 페이지. 외부 라이브러리 없이 파일 하나로 굴러간다. 브라우저로 직접 열어 확인한다.

- **오늘의 기분** — 이모지 버튼 3개, 누르면 각각 다른 응원 문구가 뜨고 그 이모지가 위로 튀어오른다
- **다크모드 토글** — 우상단 버튼. 선택은 브라우저에 저장되고, 처음 방문이면 OS 설정을 따라간다
- **꾸미기** — 좋아하는 것(커피·고양이·라멘) 이모지가 배경에 떠오르고, 커서를 따라 반짝임이 생기며, 카드에 그라데이션 테두리가 있다
- **접근성** — 버튼에 `aria-label`·`aria-pressed`, 결과 문구에 `role="status"`, 목록에 `role="list"`. 장식은 전부 `aria-hidden`이고 `prefers-reduced-motion`이면 움직임이 꺼진다

## 도구

- `page-tools/skills/page-check/` — HTML을 title·내부 링크·이미지 alt·viewport·UTF-8 5개 관점으로 점검하는 스킬 (플러그인으로 포장)
- `.claude/agents/` — `page-checker`(위 스킬로 점검), `copy-helper`(문구 개선안 제안). 둘 다 읽기 전용이다
- `.claude/hooks/worklog.sh` — 작업 한 턴이 끝날 때마다 `.claude/worklog.txt`에 기록을 남기는 Stop 훅
- `.github/workflows/daily-hello.yml` + `update_quote.py` + `quotes.txt` — 매일 위 '오늘의 한마디'를 무작위로 갈아 끼우고 자동 커밋하는 GitHub Actions
