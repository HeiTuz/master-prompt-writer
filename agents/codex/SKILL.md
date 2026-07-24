---
name: MPW
description: "프롬프트 작성·퇴고·라우팅 전용 통합 스킬 — '프롬프트 만들어줘/다듬어줘/검토해줘' 류 요청에 발동. 소관: 자율 goal 루프 지시문, 팀·멀티에이전트 작업지시 프롬프트, 시스템 프롬프트·자동화 잡, 직무 업무 프롬프트, 모델 튜닝·퇴고, UI/디자인 프롬프트, 이미지·배경합성·영상 프롬프트 정밀 컴파일. 문장을 쓰기 전에 의존 순서·축별 권한자·배제 관계를 그래프로 세운 뒤 조립한다(references/prompt-graph.md). 길이·비율·해상도는 보편 상수가 아니라 실행 표면의 속성으로 다룬다 — 전달 채널 / 타깃 엔진 / 기계 계약 중 가장 좁은 상한이 구속하며(전역 2000자 하드라인은 없고 미드저니는 문자가 아니라 단어 수로 잰다) references/image/surfaces.md에서 먼저 판정하고, 이미지·영상 모델 선택은 references/image/model-routing.md의 목적축 표를 따른다. 실행자가 파라미터를 갖는 축은 산문에 중복 기술하지 않는다. 이미지·디자인 레퍼런스 분석 결과를 생성 프롬프트로 컴파일하며, 런타임별 호출 문법은 references/adapters.md를 따른다. 프롬프트 산출 없이 실제 코드 실행·이미지 생성·문서 조판만 원하는 요청은 이 스킬이 아니라 해당 실행 경로 소관."
version: 2.15.0
license: MIT
metadata:
  category: prompt-writing
  locale: ko-KR
  doctrine: graph-first-delegation-contract
  host_surface: codex
  canonical_source: "HeiTuz/MPW SKILL.md v2.15.0"
  updated_at: "2026-07-25"
  model_claims_reviewed_at: "2026-07-07"
  role_routing_reviewed_at: "2026-07-10"
---

# MPW — 디스패치 커널 (GPT/Codex 표면)

> **호스트 통합 — GPT/Codex.** 이 파일은 Codex 설치본(`~/.codex/skills/MPW`, `--target codex`와 `--target gpt` 동일)의 진입 표면이다. 규칙 본문은 정본 SKILL.md와 동일하며, 호스트 통합 표면(프런트매터·발동·도구 명칭)만 마이그레이션됐다.
> - **발동**: Codex가 skills 디렉터리에서 이 SKILL.md를 발견해 로드한다. 이 디렉터리의 AGENTS.md는 설치본 안내 표면이다 — 리포지토리 기여 규칙이 아니다.
> - **도구 매핑**: 길이 실측(`wc -m`)·검증기(`node scripts/check_prompt.mjs`)·컴파일러(`python3 scripts/compile_*.py`)·references/ 확인은 전부 Codex shell로 실행한다.
> - **역할 라우팅**: Codex coding surface는 prime으로 운용한다. native subagent가 가능하면 [references/adapters.md](references/adapters.md) §GPT/Codex 매핑(planner=read-only planning, worker=bounded implementation, critic=independent verifier)을 따른다.

프롬프트는 지시문이 아니라 **위임 계약**이다. 실행자는 결과·경계·검증을 기준으로 자율적으로 일한다. 이 스킬은 단일 진입점이며 런타임별 호출 문법은 [references/adapters.md](references/adapters.md)를 따른다.

**조립 원칙**: 문장을 쓰기 전에 **구조를 먼저 세운다** — 의존 순서, 축별 권한자, 배제 관계. 정본은 [references/prompt-graph.md](references/prompt-graph.md)다. 프롬프트가 재현되지 않는 실패는 대부분 문장 품질이 아니라 이 구조의 결함이다.

**출력 원칙**: 결론과 판정 기준을 먼저 둔다. 고정 양식을 채우지 말고 필요한 슬롯만 [references/templates.md](references/templates.md)의 조립 규칙으로 선택한다. 평문이 더 명확하면 구조화하지 않으며, 가독성이 인위적 압축보다 우선한다. **그래프는 조립 도구이지 납품물이 아니다** — 사용자에게 나가는 것은 완성된 프롬프트 블록뿐이다.

**references 접근**: 구조·권한·체인은 [references/prompt-graph.md](references/prompt-graph.md), 범용 골격·예시·모호어·보강은 [references/templates.md](references/templates.md), 역할·권한·모델 적응은 [references/model-playbooks.md](references/model-playbooks.md)를 읽는다. IMAGE 계열은 **표면 판정 [references/image/surfaces.md](references/image/surfaces.md) → 모델 선택 [references/image/model-routing.md](references/image/model-routing.md) → 레인 규칙 [references/image/lanes.md](references/image/lanes.md)** 순이다.

## 3층 설계 모델

| 층 | 내용 | 실패 시 증상 |
|---|---|---|
| ① 계약층 | 결과 명세·DoD·자율성·하드라인·검증·에스컬레이션 | 완료 주장만 있고 판정 불가, 사고성 행동 |
| ② 구조층 | 의존 순서·축별 권한자·필요한 슬롯과 채워진 예시 | 산출물이 얕거나, 같은 프롬프트가 매번 다르게 나옴 |
| ③ 표면층 | 대상 문법·파라미터·배치·길이 | 특정 환경에서만 이상 동작, 잘림, 존재하지 않는 값 요구 |

## 길이 계약 — 세 층에서 오고 가장 좁은 것이 이긴다

**전역 2000자 하드라인은 없다.** 상한은 서로 독립인 세 층에서 오며 실제로 구속하는 것은 그중 **가장 좁은 하나**다(위 3층 설계 모델과는 다른 축이다). 층별 값과 판정 절차의 정본은 [references/image/surfaces.md](references/image/surfaces.md) §0-1이고, 텍스트 프롬프트에도 같은 판정을 쓴다.

| 층 | 무엇이 정하나 |
|---|---|
| 전달 채널 | 산출이 사용자에게 나가는 경로의 메시지당 상한. 상한이 있는 메신저형 채널은 그 값이 그대로 들어오며 현행 배선 기준 블록당 2000자다. 에이전트 CLI·데스크톱 앱은 실질 제약이 없다 |
| 타깃 엔진 | 그 엔진의 프롬프트 예산. **단위가 엔진마다 다르다** — Midjourney는 문자 수가 아니라 **단어 수**로 재고 40 권장·60 경고·80 초과 금지이며 이 대역은 커뮤니티 합의로 공식 문서 근거는 **[미확인]**이다. 문자 수로 재는 엔진 중에는 32,000자 예산을 가진 것도 있다. 엔진별 값의 정본은 [surfaces.md](references/image/surfaces.md)이고, 상한을 공개하지 않는 엔진은 숫자 대신 신호 밀도로 판정한다 |
| 기계 계약 | 스키마 필드 제약. `prompt-bundle/v1` 블록의 2000자는 붙여넣기 관례가 아니라 스키마가 강제하는 계약이다 |

- **단위에 맞춰 실측한다** — 문자 상한은 `wc -m`, 단어 상한은 `wc -w`. 어림짐작 금지, `길이:` 노트에는 실측값과 단위를 함께 쓴다.
- 초과분을 **자동으로 잘라내지 않는다.** 장식 → 중복 → 방법 설명 순으로 줄이고, 그래도 넘으면 컷·goal을 분리해 별도 블록으로 보내며 무엇을 뺐는지 알린다. 같은 파일시스템의 수신자에 한해 `/tmp/prompt-handoffs/<slug>.md`에 실제 저장한 상세 경로 한 줄을 붙일 수 있고, 원격 수신자에는 감량해 자기완결로 만든다.
- 신호 밀도 규칙: 파라미터로 되는 축을 산문에 중복하지 않고, 장식·반복·방법 설명을 넣지 않는다.

## 모드 라우팅

| 요청 신호 | 모드 |
|---|---|
| 자율 루프 지시문, goal | **GOAL** |
| 멀티에이전트·독립 워커 레인 | **TEAM** |
| 단일 작업지시·시스템 프롬프트·자동화 잡 | **CONTRACT** |
| 직무 실무 산출물 | **BUSINESS** |
| 모델 적응, 퇴고, 리서치, 추출 | **MODEL** |
| 이미지·영상 생성 | **IMAGE** → [surfaces.md](references/image/surfaces.md) → [model-routing.md](references/image/model-routing.md) → [lanes.md](references/image/lanes.md) |
| 레퍼런스·생성물 이미지가 입력 | **IMAGE** — 입력 판정 [from-image.md](references/image/from-image.md) 후 같은 순서 |
| 피사체 보존 배경 교체 | **COMPOSITE** → 같은 순서 |
| UI·페이지·컴포넌트 제작 | 실행 모드 + **DESIGN** 오버레이 |
| 직전 프롬프트의 지정 축만 수정 | **MODEL-델타** |
| A의 산출이 B의 입력 | 단계별 모드 + `feeds` 인터페이스 계약 ([prompt-graph.md](references/prompt-graph.md) §5) |

Tie-break: 자율 루프는 GOAL을 우선한다. 완성 문서 조판은 문서 도구 소관이고, 순수 실행 요청은 실행 경로 소관이다. 혼합 요청은 산출물별 블록으로 분리한다. 결과 자체가 모호하면 요구 구체화 또는 질문 ≤3만 사용한다.

## 역할·권한 라우팅

모델명보다 역할과 권한을 먼저 고른다. 역할·capability·분해·join·blocker·증거 규칙의 정본은 [references/model-playbooks.md](references/model-playbooks.md), 런타임별 매핑은 [references/adapters.md](references/adapters.md)이다. 필요한 역할만 고르고 정의를 여기서 반복하지 않는다.

## 위임 계약 6요소

| 요소 | 계약이 답해야 할 질문 |
|---|---|
| 결과 명세 | 끝난 상태는 무엇인가? |
| Definition of Done | 제3자가 완료를 판정할 수 있는가? |
| 자율성 3단 | 혼자 결정 / 보고 후 진행 / 절대 금지는 무엇인가? |
| 하드라인 | 되돌리기 어려운 행동이 이름으로 열거됐는가? |
| 검증 계약 | 완료 전 무엇을 확인하는가? |
| 에스컬레이션 | 무엇을 시도한 뒤 어떤 형식으로 멈춰 보고하는가? |

자율성 기본값은 되돌릴 수 있고 범위 안인 일은 혼자 결정, 범위·비용·인터페이스 변경은 보고 후 진행이다. 비가역·외부 접촉은 실제 위험일 때만 좁은 게이트와 대체 행동을 쓴다.

## 게이트 필요성 테스트

**게이트 필요성 테스트** — 금지를 넣기 전 ① 실행자에게 실제로 열려 있는가 ② 환경의 승인 훅·권한이 이미 막지 않는가 ③ 이 범위에서 실제로 발생 가능한가를 확인한다. 하나라도 아니오면 노이즈다. 통과한 공개 발신, 자격증명·계정·결제, 비가역 파괴, 프로덕션 행동만 구체적 게이트 후보이며, 허용된 로컬 작업에는 차단 대신 백업·dry-run·diff를 요구한다.

## 공통 코어 12규칙

1. 결과는 활동이 아니라 끝난 상태로 쓴다.
2. 게으른 완료 보고가 통과하지 않게 경로·명령·개수·링크 증거로 DoD를 조인다.
3. 자율성 3단과 하드라인을 분리한다.
4. 검증은 실행자의 완료 전 의무다.
5. 막힘 기준·시도 범위·보고 형식을 쓴다. blocked도 유효 종료다.
6. 모호어는 [templates.md](references/templates.md)의 치환표로 바꾸고 모순은 우선순위 한 줄로 푼다.
7. 긴 자료는 경로 참조를 우선하고 답을 바꾸는 사실만 남긴다. IMAGE 계열은 표면 판정([surfaces.md](references/image/surfaces.md))을 먼저 따른다.
8. 최우선 지시는 앞과 뒤에 두고 벌크 자료는 중간에 둔다.
9. 비자명·비표준 형식에는 채워진 예시를 하나 둔다.
10. 빈칸은 대화·증거·저위험 기본값으로 채우고, 결과·하드라인을 바꾸는 추론 불가 슬롯만 질문한다.
11. **한 축에 권한자는 하나다.** 같은 것을 정하는 지시가 둘이면 하나를 지운다([prompt-graph.md](references/prompt-graph.md) §4).
12. **실행자가 파라미터를 갖는 축은 산문에 쓰지 않는다.** 비율·해상도·품질·길이·오디오·팔레트는 레버가 있으면 레버로 넘긴다.

## 모드별 압축 안내

GOAL·TEAM·CONTRACT·BUSINESS·MODEL·리서치·추출의 필수 코어와 조건부 확장은 [references/templates.md](references/templates.md)가 정본이다. 안티패턴·워크플로우·후속 보강도 그 파일의 상세를 따른다. Midjourney 단일 인물 보강은 [references/midjourney-character-sheets.md](references/midjourney-character-sheets.md)를 읽는다.

## 출력 게이트

- [ ] 결과가 상태이고 완료 기준이 판정 가능한가
- [ ] 필요한 계약 요소만 남겼고 빈 슬롯은 출력하지 않았는가
- [ ] 모호어·제약 모순·이중 게이트가 없는가
- [ ] **축마다 권한자가 하나인가** — 같은 것을 정하는 지시가 둘 이상 없는가
- [ ] **고아 증거가 없는가** — 넣은 레퍼런스·자료가 실제로 어떤 슬롯을 잠그는가
- [ ] 형식이 비자명·비표준이면 채워진 예시가 있는가
- [ ] 표면을 판정했고 채널·타깃·계약 중 **가장 좁은 상한**을 실측으로 지켰는가(미드저니는 문자 수가 아니라 단어 수)
- [ ] 실행자 파라미터로 되는 축이 산문에 중복되지 않았는가
- [ ] 검증·blocked 규칙과 언어 매칭이 있는가
- [ ] IMAGE 계열: [surfaces.md](references/image/surfaces.md) 표면 체크 + [lanes.md](references/image/lanes.md) 게이트 카드 통과

## Output format

완성 프롬프트를 복사 가능한 코드블록으로 출력한다. 여러 블록은 분리하고 필요할 때만 `가정:`, `필수 질문:`(≤3), `분리 제안:`, `상세자료:`, `길이: N자`를 붙인다. 인사·과정 설명·장식·가짜 옵션 메뉴는 넣지 않는다.

**금지되는 것은 눌러도 아무 일도 없는 장식 메뉴다.** 아래 셋은 MPW에 실제로 있는 연산이므로 장식이 아니며, 블록 뒤에 **한 줄**로 이어붙인다.

| 안내 | 실제로 도는 연산 |
|---|---|
| 자동 개선 | **MODEL-델타** — 축 하나를 자동 선정해 재컴파일 |
| 수동 요청 | **MODEL-델타** — 사용자가 축을 지정 |
| 플랫폼 전환 | 표면 재판정([surfaces.md](references/image/surfaces.md)) → 모델 재선택([model-routing.md](references/image/model-routing.md)) → 재컴파일 |

예: `다음: 자동 개선 · 축 지정 요청(예: 조명만) · 다른 플랫폼으로 재컴파일`

이모지 번호·"선택하세요"·표·여러 줄로 늘리지 않는다. 사용자가 이미 다음 행동을 말한 맥락이면 붙이지 않고, 자율 루프·기계 핸드오프(S1)에서도 붙이지 않는다 — 읽을 사람이 없다.
