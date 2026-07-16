# Midjourney v8.1 — 캐릭터 시트·전신 레퍼런스

## 적용 조건
사용자가 Midjourney **v8.1**에서 인물 레퍼런스를 주고 캐릭터 시트·턴어라운드·전신 고정을 요구할 때 적용한다. 실제 UI 모델 선택, 단일 잡 검증, 10각도 독립 시퀀스의 배치 게이트는 [midjourney-v81-identity.md](midjourney-v81-identity.md)를 함께 읽는다.

## 파라미터 계약
- 레퍼런스 고정 문법·이미지 영향도 조절은 [midjourney-v81-identity.md](midjourney-v81-identity.md) §Reference syntax가 정본이며, 확인되지 않은 플래그를 추정해 붙이지 않는다.
- 드리프트 대응도 identity.md의 UI-확인 규칙을 따른다.

## 프롬프트 구조
1. `character turnaround sheet` + 한 캔버스의 뷰 수·순서를 첫 문장에 고정한다.
2. `face identity is the highest priority` 뒤에 **관찰된** 얼굴·헤어 식별점을 짧게 적는다. 실존인물·국적·나이를 추정하지 않는다.
3. 전신 보장은 `entire figure fully visible from hair to feet`, `both feet visible`, `camera positioned far enough back`, `generous space above head and below feet`로 중복 고정한다.
4. 체형 수치는 시각 비례로 번역한다: `170 cm-tall fashion proportion, approximately 7.5 heads tall, long-leg balanced silhouette`. 생성 모델이 실제 단위를 측정하지 않으므로 “정확한 신장”이라고 약속하지 않는다.
5. 턴어라운드는 `front / three-quarter / side profile / back` 순서, neutral A-pose, 팔을 몸통에서 약간 분리, 동일한 의상·조명·간격을 명시한다.

## 판정
- 얼굴 고정 품질은 얼굴이 보이는 전면·3/4·측면에서만 판단한다. 후면뷰는 얼굴 불가시가 정상이다.
- 한 이미지에 다중 뷰를 넣으면 동일성은 강한 유도이지 절대 보증이 아니다. 결과에 드리프트가 있으면 identity.md의 image-weight 규칙을 확인한 뒤 재생성한다.
