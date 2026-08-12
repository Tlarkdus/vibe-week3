# Week 5 — 규칙 파일 도입 전/후 비교

실험 저장소: `agentic-lab` (결제 코드 실습용)
질문: **"환불 수수료 5%를 떼는 기능을 추가하고 싶어. 어느 파일을 고쳐야 하고, 금액 단위는 뭘 쓰고, 로그는 어떻게 남겨야 하는지 계획만 말해줘. 코드는 아직 수정하지 마."**

이 저장소는 함정이 깔려 있다. 같은 이름의 `refund()` 함수가 `src/payments/`, `src/billing/`, `src/old/` 세 곳에 있고, 그중 살아 있는 건 `src/payments/` 하나뿐이다.

---

## 도입 전 (규칙 파일 없음)

<!-- STEP2-BEFORE:START -->

> ✅ **이번엔 제대로 된 "도입 전"이다.** 규칙 파일 7개를 치웠을 뿐 아니라 `.git` 디렉터리 자체를 저장소 밖으로 옮겨,
> `git show`로 되찾을 수 있는 경로까지 막았다. Claude가 본 건 소스 코드와 `package.json`뿐이다.

받은 답변:

> **이미 있음. 고칠 파일 없음.**
>
> `src/payments/refund.js`가 5% 수수료를 이미 구현하고 있고, `npm test` 10개 전부 통과한다.
>
> ```js
> const REFUND_FEE_PERCENT = 5;
> const feeMinor = Math.floor((amountMinor * REFUND_FEE_PERCENT) / 100);
> const netMinor = amountMinor - feeMinor;   // fee + net === amount 보장
> ```
>
> | 항목 | 답 |
> |---|---|
> | 파일 | `src/payments/refund.js` — 이게 유일한 현역. 요율은 `REFUND_FEE_PERCENT` 상수 하나 |
> | 금액 단위 | minor unit(전) 정수, 100전 = 1원. 필드명 `amountMinor` / `feeMinor` / `netMinor`. 실수·부동소수 금지, 나눗셈은 `Math.floor` 내림 |
> | 로그 | `lib/logger.js`의 `logPayment()`만 사용. JSON line 1줄 = 이벤트 1개. `refund.start`(진입) → `refund.done`(성공, `fee_minor`/`net_minor` 포함). `console.log` 직접 호출 금지 |
>
> 주의할 함정 두 개:
> - `src/billing/refund.js` — 원 단위 정수에 `console.log` 문자열 로그. 주석 처리된 `REFUND_FEE = 500`(2018년 정액 정책)이 있어서 여기를 고치고 싶어지는데, 테스트가 없고 payments 쪽과 단위가 달라 손대면 이중 차감 위험. 통합 TODO만 2020년부터 방치된 상태.
> - `src/old/legacy.js` — 어디서도 import 안 되는 죽은 코드. `calcRefundLegacy`는 수수료가 아니라 세금 10% 역산이라 아예 다른 계산이다.
>
> **정말 필요한 게 뭔지 다시 확인하고 싶은 지점:** 요율 변경(5% → 다른 값)이면 상수 한 줄, 주문별·등급별 차등 요율이면 그건 새 기능이라 시그니처가 바뀐다. `src/billing/refund.js` 통합이 목적이면 그건 별도 작업. 어느 쪽인지 알려주면 그것만 하겠다.

이때 Claude가 실제로 한 행동:

1. 두 작업 디렉터리를 훑고 파일 목록을 뽑았다 — 규칙 파일이 없으니 참조할 지침도 없었다
2. `src/payments/refund.js`, `src/billing/refund.js`, `src/old/legacy.js`, `lib/logger.js`, `tests/refund.test.js`를 **전부 열어서 읽었다**
3. 어느 게 현역인지 문서가 아니라 **증거로 판정했다** — 테스트가 import 하는 건 payments 하나, legacy는 어디서도 import 안 됨, billing은 2020년 TODO 방치
4. `npm test`를 돌려 10 pass를 확인했다
5. 함정 두 파일을 "열지 않았다"가 아니라 **"열어보고 손대지 말라고 경고했다"** — 이중 차감 위험과 단위 불일치까지 짚었다

결론 자체는 도입 후와 같았다. 다른 건 거기까지 가는 길이다.

<!-- STEP2-BEFORE:END -->

---

## 도입 후 (`CLAUDE.md` + `GOLDEN_RULES.md` + `docs/payment-rules.md` + `.claude/commands/` 도입)

> **이미 구현돼 있습니다.** 추가할 게 없습니다.
>
> `src/payments/refund.js`:
> - 파일: `src/payments/refund.js` — 이미 여기서 처리 (`src/billing/`, `src/old/`는 열지 않음)
> - 상수: `REFUND_FEE_PERCENT = 5` (refund.js:6), 정책 변경 시 이 한 줄만
> - 계산: `Math.floor(amountMinor * 5 / 100)` → `netMinor = amountMinor - feeMinor` (refund.js:30-31). 정수 연산, 빼기로 실지급액 산출 — 규칙대로
> - 단위: `amountMinor` 전(minor unit) 정수, 원금 그대로 보존. 결과에 `feeMinor`/`netMinor` 별도 필드
> - 검증: 수수료 차감 **전** 원금 기준, `Error`/`TypeError`/`RangeError` 구분해서 던짐
> - 로그: `logPayment()`로 `refund.start` / `refund.done` 두 줄. 수수료는 종료 로그에 `fee_minor`/`net_minor`로 실림 — 별도 이벤트 없음
>
> `npm test`: 10 pass / 0 fail. 수수료 내림, `fee + net === amount`, 1전 케이스, 한도 판정 기준까지 이미 테스트가 있습니다.
>
> 계획 대신 결론: 코드 변경 0줄. 바꿀 게 생긴다면 요율뿐이고, 그건 refund.js:6 상수 한 줄입니다.

이때 Claude가 실제로 한 행동:

1. `payment-feature` 스킬(`.claude/commands/`)을 먼저 호출해 정해진 순서를 따랐다
2. `GOLDEN_RULES.md`, `docs/payment-rules.md`를 읽었다
3. 파일 목록에서 `src/billing/refund.js`, `src/old/legacy.js`를 **보고도 열지 않았다**
4. `npm test`를 직접 돌려 10 pass를 확인하고 보고했다

---

## 관찰 3줄

<!-- OBSERVATION:START -->

1. **규칙이 없어도 답은 맞았다 — 코드가 증거를 남겨놨으면.** 테스트가 payments만 import 하고, legacy는 아무도 import 하지 않고, billing에는 2020년 TODO가 박혀 있었다. 규칙 파일 없이도 현역을 골라냈지만 그건 **저장소가 친절했기 때문**이고, 근거가 흐릿한 코드였다면 셋 중 아무거나 골랐을 수 있다.
2. **규칙의 값어치는 "안 읽어도 되는 파일"을 지정해주는 데 있다.** 도입 전은 함정 두 파일을 열어 읽고 스스로 위험을 판정했고, 도입 후는 DEPRECATED라는 한 줄만 보고 열지 않았다. 결론은 같지만 도입 전은 읽기 5개 + 판정, 도입 후는 규칙 읽기 + 정답 파일 1개다. 파일이 3개라 감당된 거지, 30개였다면 얘기가 다르다.
3. **규칙이 바꾼 건 답이 아니라 답의 모양이다.** 도입 전은 함정 경고와 "어느 쪽이냐"는 되물음이 붙었고, 도입 후는 `payment-feature` 스킬이 순서를 정해 곧장 결론으로 갔다. 규칙 파일이 사주는 건 더 나은 답이 아니라 **더 짧고 재현 가능한 경로**다 — 같은 질문을 열 번 던져도 같은 길로 간다는 것.

<!-- OBSERVATION:END -->
