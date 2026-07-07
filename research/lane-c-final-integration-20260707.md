# Lane C final integration table — 2026-07-07

Task-4 reconciliation: after Lane A/B completion, read `research/image-prompt-web-research-20260707.md` (29 items, 27 adopted/partial, 2 failed alternatives) and `research/image-prompt-pattern-matrix-20260707.md` (12 practical/locality sources). Missing adopted patterns were folded into the canonical patch without copying web text.

| 출처 유형 | 반영 패턴 | 버린 패턴 | 변경 파일 | 검증 결과 |
|---|---|---|---|---|
| 공식 모델/엔진 가이드 계열 | prompt body와 UI preset/AR/camera motion/seed/timestamp를 분리, Higgsfield는 프리셋 라벨 + 본문 1문단, 영상은 씬당 지배 모션 1개 + 핵심 행동 1개, image-to-video는 입력 이미지 재묘사 대신 변화·동작·오디오만 | 프롬프트 본문에 motion preset/비율/seed를 뒤섞기, 한 클립에 dolly+orbit+crash zoom 누적, 모든 모델에 timestamp 강제 | `references/templates.md`, local `references/templates.md` | `python3 scripts/lint.py` OK, `node scripts/check_prompt.mjs --test` 14/14 green |
| 커뮤니티 실전 사례 계열 | `Korean` 단독 대신 성인 가상 페르소나 + 헤어/메이크업/의상/공간/조명/잡지 톤 4축 이상; skin realism은 pores/fine texture/vellus hair/tonal variation처럼 관찰 가능한 질감으로 확장 | 국적 하나로 얼굴·피부·체형을 추론, 실존 아이돌/배우 닮은꼴, flawless/poreless/plastic skin | `SKILL.md`, `references/templates.md`, `references/image/editorial-fashion.md`, local `SKILL.md`, local `references/templates.md` | 로컬 라벨 검사 `True`, readback 확인 |
| 사진·영화 제작 어휘 계열 | 필름명은 1개 emulation 앵커 + skin/shadow/highlight/halation/grain 결과로 환원; 렌즈 압축은 `distant camera position`과 배경 레이어 결과로 병기 | Kodak/Fuji/CineStill/Portra 다중 스택, `8K/masterpiece/ultra-realistic`류 SD-era 품질 주문, `85mm` 단독 magic token | `references/image/editorial-fashion.md`, `references/image/compiler.md`, local `references/templates.md` | lint OK |
| 한국 로컬리티·뷰티·패션 자료 계열 | 성수 창고형 파사드, 한남/한강진 갤러리 거리, 익선동 한옥 골목, DDP 은회색 곡면 건축처럼 공간 구조·재료·빛으로 명시; skin-first makeup/blurred lip/brushed brows는 브랜드명 없이 표면감으로 사용 | 유명 매장·상표 간판, 관광 스테레오타입만 나열, `K-beauty처럼` 단독, 전통 의상/궁궐 자동 치환 | `references/image/editorial-fashion.md`, local `references/templates.md` | readback으로 핵심 섹션 로드 확인 |
| 제품·포스터 실전 사례 계열 | 제품/캠페인은 hero object, readable label, reflection, contact shadow, supporting prop hierarchy를 명시하고 주변 소품은 낮은 대비·작은 면적으로 종속 | 모든 요소를 주연으로 만드는 과밀 포스터, 실재 상표/제품명 임의 생성, 모델·소품이 라벨을 가리는 구성 | `references/image/categories.md` | lint OK |
| 리얼리티/anti-AI 실무 자료 계열 | natural skin texture, visible pores, contact shadow, garment tension, hand-object contact, matching shadow direction, grain unification | `bad hands/no AI` 부정 토큰, plastic skin, 손·발·배경 상호작용 생략 | `references/image/editorial-fashion.md`, `references/templates.md`, local `references/templates.md` | lint OK, fixture suite green |

Backport scope: 로컬 배포본은 로컬 고유분을 보존한 채 라인 단위 이식(상세는 내부 문서).
