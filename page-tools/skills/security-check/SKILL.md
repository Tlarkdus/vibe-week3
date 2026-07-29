---
name: security-check
description: HTML/JS 파일을 4가지 보안 관점(하드코딩된 비밀번호·API 키, escape 없이 innerHTML에 들어가는 사용자 입력(XSS), console.log의 민감 정보 노출, http:// 외부 요청)으로 점검하고 🔴심각/🟡주의/🟢제안 + 파일:라인 근거로 보고한다. "보안 점검", "security check"라고 하거나, 만든 웹페이지에 키·비밀번호가 노출됐는지 / XSS가 있는지 봐 달라고 할 때 사용한다. HTML·JS를 수정한 뒤 안전한지 확인해 달라는 요청에도 사용한다.
---

# security-check

HTML/JS 파일을 읽고 아래 4가지를 점검한 뒤 심각도별로 보고한다. **수정은 하지 않는다** — 고쳐 달라고 하면 그때 고친다. 점검만 하고 끝내야 사용자가 "무엇을 왜 고칠지" 판단할 기회를 갖는다.

## 대상

인자로 파일/글롭이 주어지면 그것. 없으면 저장소의 `**/*.{html,js}` (단, `node_modules`, `dist`, `build`, `vendor` 제외).

읽기 전용 도구(Read, Grep, Glob)만 쓴다. Grep으로 후보 라인을 먼저 좁히고, 후보가 나온 파일은 Read로 앞뒤 맥락을 확인한다 — 맥락 없이 패턴만 보고 판정하면 오탐이 쏟아진다.

## 점검 항목

### 1. 하드코딩된 비밀번호·API 키

찾을 것: `apiKey`, `api_key`, `secret`, `token`, `password`, `passwd`, `pw`, `credential`, `authorization` 같은 이름에 **문자열 리터럴이 직접 대입된** 곳. `sk-`, `ghp_`, `AKIA`, `AIza`, `xoxb-` 같은 알려진 키 접두사, 그리고 32자 이상의 base64/hex 리터럴도 본다.

- 🔴 실제 키/비밀번호로 보이는 값이 소스에 박혀 있음. 프론트엔드 파일은 **누구나 소스 보기로 읽을 수 있다**는 게 핵심 — "빌드하면 가려진다"는 방어는 통하지 않는다.
- 🟡 자리표시자(`"YOUR_API_KEY"`, `"changeme"`)나 예시값. 지금 위험하진 않지만 실제 값으로 바뀔 자리라 위치를 짚어 준다.
- 🟢 값이 `process.env`·서버 응답에서 오는데 변수명만 걸린 경우 — 오탐이므로 보고하지 않거나, 개선 여지가 있을 때만 제안한다.

### 2. escape 없이 innerHTML에 들어가는 사용자 입력 (XSS)

찾을 것: `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `eval`, `new Function`, `$(...).html(...)`.

대입되는 값의 출처를 역추적한다. `input.value`, `location.hash`/`search`, `localStorage`, `fetch` 응답, URL 파라미터처럼 **사용자나 외부가 정할 수 있는 값**이 escape 없이 섞이면 위험하다.

- 🔴 외부 입력이 escape·sanitize 없이 HTML로 들어감. 문자열 연결이나 템플릿 리터럴로 조립되면 특히 그렇다.
- 🟡 지금은 상수만 들어가지만 `innerHTML`을 쓰고 있어 나중에 변수를 끼우면 바로 뚫리는 자리.
- 🟢 `textContent`·`createElement`로 이미 안전하게 쓰고 있으면 통과 요약에만 넣는다.

권고는 대개 `textContent` / `createElement` + `append`다 — 이 저장소의 `expense.html` `render()`가 그 패턴의 예시다.

### 3. console.log의 민감 정보 노출

찾을 것: `console.log/warn/error/debug/info`, `alert`에 넘기는 값 중 토큰·비밀번호·개인정보(이메일, 전화번호, 주소)·응답 객체 통째(`console.log(res)`, `console.log(user)`)인 것.

- 🔴 비밀번호·토큰·키를 그대로 출력. 브라우저 콘솔은 사용자와 확장 프로그램 모두가 볼 수 있고, 스크린샷·화면 공유로도 새어 나간다.
- 🟡 사용자 객체나 API 응답을 통째로 출력 — 지금 필드에 민감 정보가 없어도 응답 스키마가 바뀌면 그대로 노출된다.
- 🟢 배포 전에 지우면 좋을 디버그용 로그.

### 4. `http://`로 시작하는 외부 요청

찾을 것: `src`, `href`, `action`, `fetch(...)`, `XMLHttpRequest.open`, `@import`, CSS `url(...)`에 쓰인 `http://` URL.

- 🔴 스크립트·스타일을 `http://`로 로드하거나, `http://`로 데이터를 전송(`fetch` POST, `form action`). 중간자가 내용을 보거나 코드를 갈아끼울 수 있다.
- 🟡 이미지·링크 등 그 외 `http://` 리소스. HTTPS 페이지에서는 혼합 콘텐츠로 차단되기도 한다.
- 🟢 `http://localhost`, `127.0.0.1` — 로컬 개발용이라 위험하지 않다. 굳이 보고하지 않아도 되고, 언급한다면 🟢로.

## 심각도 기준

- 🔴 **심각** — 지금 이 상태로 배포하면 비밀이 새거나 코드가 주입될 수 있음
- 🟡 **주의** — 당장 뚫리진 않지만 조건이 조금만 바뀌면 위험해지는 자리
- 🟢 **제안** — 있으면 좋은 개선

판정이 애매하면 한 단계 낮추고 근거를 적는다. 과장된 🔴이 반복되면 사용자가 보고 전체를 무시하게 되고, 그때 진짜 🔴도 같이 묻힌다.

## 출력 형식

파일별로:

```
## expense.html

🔴 심각 (1)
- expense.html:42  `el.innerHTML = '<b>' + input.value + '</b>'` — 입력창 값이 escape 없이 HTML로 삽입됨. `<img onerror=...>` 입력만으로 스크립트 실행 가능
   → textContent 또는 createElement로 교체

🟡 주의 (1)
- expense.html:78  `console.log(user)` — 응답 객체 통째 출력. 지금은 name만 있어도 필드가 늘면 그대로 노출됨

🟢 제안 (0)
```

근거 줄에는 **파일:라인 + 실제 코드 조각 + 왜 위험한지 한 줄**을 반드시 붙인다. 라인 번호만 있으면 사용자가 파일을 다시 열어 봐야 하고, 코드 조각만 있으면 왜 문제인지 판단할 수 없다.

문제가 없는 항목은 나열하지 말고 마지막에 한 줄로 요약한다: `✅ 통과: 하드코딩 비밀, http:// 요청`. 전부 통과면 `✅ 4개 항목 모두 통과`.

여러 파일을 점검했으면 맨 끝에 총계를 한 줄 붙인다: `총 3개 파일 — 🔴 1 / 🟡 2 / 🟢 0`.
