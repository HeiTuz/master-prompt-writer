# 에디토리얼 패션 — 사진 어휘

우선순위: [../lanes.md](../lanes.md) §레인 게이트 카드 > [../compiler.md](../compiler.md) 철칙 > 이 파일. 철칙 전문은 [../compiler.md](../compiler.md).

## 7. 사진 어휘 풀 — 결과 기반 토큰

판정문: gpt-image-2에는 카메라·조명 장비명을 그대로 박지 말고 **결과(빛·심도·질감·색)**로 환원해서 쓴다. 표현은 긍정형 기본 + 티어 화이트리스트다. 장면 배제 부정문은 0개, `no ~`는 Tier-1/Tier-2 캐노니컬 문구로만 쓴다. SD 품질태그·가중치 문법은 쓰지 않는다.

### 7.1 심도·렌즈 character (결과로)

| 축 | 결과 토큰 |
|---|---|
| 광각 느낌 | `wide field of view, environment fully visible, mild edge stretch, deep focus front-to-back` |
| 표준 | `natural perspective, balanced compression, subject and setting in proportion` |
| 망원/압축 | `distant camera position, compressed perspective, flattened planes, subject lifted from a soft background` |
| 얕은 심도 | `shallow depth of field, background falls off softly into creamy blur` |
| 빈티지 보케 | `swirly painterly bokeh, gentle vintage rendering` |
| 아나모픽 | `wide cinematic frame, horizontal flares, oval highlights` |
| 가장자리 감쇠 | `sharp central microtexture, soft edge focus falloff`(중심부 미세결은 선명, 프레임 가장자리만 점진적으로 풀림) |

### 7.2 조명 (방향·질·결과)

| 축 | 결과 토큰 |
|---|---|
| 패턴 | Rembrandt(뺨 삼각 하이라이트) / butterfly(코밑 나비 그림자) / split(반쪽광) / clamshell(위아래 부드러운 균등광) |
| 질 | `soft diffuse wraparound light, gentle gradient shadows` ↔ `hard directional light, crisp sharp-edged shadows`. 중간 단계 레이킹 = `low-angle soft light, gentle relief shadows`(낮은 측면의 넓은 연질광이 돌출부만 밝히고 홈·굴곡엔 완만한 그림자) |
| 비율 | `key:fill 1:1`(평탄) / `1:2`(자연) / `1:3`(드라마틱). 결과로 `moderate shadow contrast` 식 병기 |
| 보조 | `cool rim light separating the edge`, `warm practical glow`, `window light from camera left`, `rectangular catchlight, iris radial texture, aligned with key direction`(눈동자 안 사각 반사가 클로즈업에 실촬영 공간감을 만듦) |
| 시간광 | golden hour 따뜻한 저각광 / blue hour 차분한 한기 / 정오 톱라이트 |
| 색온도 분리 | `split color-temperature lighting, warm key on skin, cool background wash`(인물이 앞으로 분리되고 공간 깊이가 생김) / 변주 `cool key on subject, warm tungsten practical background` |
| 하이키 스튜디오 | `high-key white studio, large negative space, clean editorial margins`(순백 배경과 긴 여백이 인물·의상 실루엣을 선명하게 밀어 올림) |

### 7.3 색·그레이딩 (HEX·켈빈·룩)

| 축 | 규칙 |
|---|---|
| 팔레트 | 항상 HEX 3~5개 |
| 색온도 | 켈빈 또는 `warm 3200K-feel` / `neutral` / `cool` |
| 조화 | complementary / analogous / triadic |
| 룩 | teal & orange, bleach bypass(저채도 고대비), desaturated muted, warm filmic roll-off |
| 필름 결과 | Portra 룩 = `warm skin, soft pastel midtones, gentle highlight roll-off`; Tri-X = `high-contrast monochrome, visible grain`; CineStill 800T = `tungsten night palette, soft red halation around highlights` |

### 7.4 필름/매체 3파트

```text
[필름 emulation] — [스킨], [섀도], [하이라이트]. [매거진/매체] characteristic roll-off
```

예: `Kodak Portra 400 emulation — warm luminous skin, soft green-leaning shadows, creamy highlights. Editorial magazine roll-off.`

조합 공식(감성 키워드는 필름/룩 이름과 병기해야 결과 차이가 선명해진다):

```text
[필름/룩 이름] + [빛의 방향] + [노출 방식] + [색감] + [그레인] + [분위기]
```

예: `Kodak Portra 400 film photography, soft window light from camera left, slightly overexposed highlights, warm creamy skin tones, fine film grain, low contrast, quiet romantic mood.`

#### 필름 스톡 결과 사전 (단어 단독 금지 — 결과·장면과 병기)

| 스톡 | 결과 묘사 | 어울리는 장면 | 영어 토큰 |
|---|---|---|---|
| Kodak Portra 400 | 부드러운 피부톤 · 크리미한 색감 · 낮은 대비 | 웨딩 · 인물 · 자연광 스냅 | `soft creamy skin, warm natural light, fine film grain` |
| Kodak Portra 800 | 크리미한 화이트 · 부드럽게 날린 하이라이트 · 로맨틱 | 웨딩 · 실내 인물 | `creamy white tones, soft blown-out highlights, warm glowing skin` |
| Kodak Gold 200 | 따뜻한 노란빛 · 선명한 색감 · 레트로 무드 | 일상 · 여행 · 가족사진 | `warm golden tones, everyday snapshot, retro feeling` |
| Fujifilm Pro 400H | 낮은 채도 · 부드러운 그린톤 · 청량함 | 숲 · 바다 · 자연 | `low saturation, soft green shift, dreamy softness` |
| Kodak Ektar 100 | 높은 채도 · 선명한 디테일 · 또렷함 | 풍경 · 건축 · 하늘 | `high saturation, sharp detail, vivid colors` |
| Ilford HP5 | 강한 명암 · 거친 그레인 · 흑백 다큐 무드 | 거리 스냅 · 흑백 인물 | `black and white, strong contrast, heavy grain` |

#### 노출·기법 결과 사전

| 기법 | 결과 묘사 | 영어 토큰 |
|---|---|---|
| Overexposure | 하이라이트를 밝게 날려 부드럽고 몽환적 | `soft overexposed highlights, bright airy atmosphere` |
| Highlight retention | 강한 햇빛에서도 흰 옷의 주름·가장자리를 남겨 싸구려 과노출을 피한다 | `retained white fabric detail, soft sun contrast, clean high-key exposure` |
| Underexposure | 그림자를 깊게 만들어 무게감 있는 분위기 | `slightly underexposed shadows, deep muted tones, dark cinematic mood` |
| Diffused light | 빛을 부드럽게 퍼뜨려 피부·경계가 자연스러움 | `soft diffused daylight, light filtered through sheer curtains` |
| Cross process | 색을 비현실적으로 변형한 실험적 필름 무드 | `cross-processed film colors, cyan color shift, unusual color palette` |
| Soft focus | 초점을 부드럽게 풀어 회상적·로맨틱 | `soft focus, dreamy blur, gentle lens softness` |
| Vignetting | 가장자리를 어둡게 해 시선을 중앙으로 | `subtle vignetting, center-focused composition` |
| Film grain | 필름 특유의 질감과 아날로그 분위기 | `fine film grain, visible analog texture` |

#### 감성 프리셋 (라벨 = 설명 + 키워드 블록, 필름/룩 이름과 병기)

| 감성 | 결과 묘사 | 키워드 블록 |
|---|---|---|
| 숲속 필름 | 습한 공기 · 낮은 채도 · 그린 그림자 | `Pro 400H-look, overexposed by one stop, green color shift, humid forest atmosphere, soft film grain` |
| 디스포저블 스냅 | 파스텔톤 · 핑크/크림 계열 · 소프트 포커스 | `disposable camera aesthetic, soft pastel tones, slight lens distortion, nostalgic snapshot` |
| 흐린 날 다큐 | 회색 하늘 · 다큐멘터리 무드 · 차분한 도시감 | `overcast diffused daylight, cool grey undertones, heavy visible grain, melancholic realism` |
| 시안 실험 | 시안·블루 색감 · 차갑고 몽환적 | `cross-processed film, cyan and blue shift, cool teal shadows, experimental film look` |
| 웨딩 필름 | 크리미한 화이트 · 자연광 · 로맨틱 | `Portra 800-look, creamy white tones, soft blown-out highlights, warm glowing skin` |
| 플래시 스냅 | 순간 포착 · 직사 플래시 · 생활감 | `snapshot aesthetic, direct flash, imperfect composition, natural unposed moment` |

### 7.5 구도·시지각

| 축 | 어휘 |
|---|---|
| 분할 | rule of thirds, golden ratio, centered iconic |
| 여백 | 카피용 여백 확보, 매거진 여백, Ma(여백의 호흡) |
| 유도 | leading lines, 시선 궤적, 삼각 안정, 소품 위계 = `subordinate prop contrast, context props below hero`(소품을 히어로보다 낮은 대비로 두어 맥락은 주되 주 피사체를 가리지 않음) |
| 샷 사이즈 | ECU(극클로즈업) → CU → MS(미디엄) → FS(전신) → EWS(원경) |
| 앵글 | eye-level / low(우러름) / high(내려봄) / over-the-shoulder / dutch(기울임) |
| 거리 | 카메라-피사체 거리를 m로 명시 |
| 커버 크롭 | `upper-body fashion close-up, tilted head crop, clean cover portrait`(얼굴·주얼리·의상 일부만 크게 잘라 뷰티와 패션 정보를 동시에 압축) |
| 커버 크롭 변주 | `gesture beauty crop`(손·주얼리가 얼굴 일부를 가림) / `asymmetric cover crop`(대각 축으로 밀어 비대칭) |
| 풀블리드 매크로 | `full-frame surface macro, no container, texture as subject`(용기·배경을 지우고 표면 자체를 화면 가득 채워 질감이 주제가 됨) |

### 7.6 재질·후처리 (결과)

| 축 | 결과 토큰 |
|---|---|
| 표면 반응 | `matte buttery surface`, `wet specular highlights`, `translucent subsurface glow`, `thick applied paste, built-up edges, metallic sheen`(두꺼운 도포면·뭉친 가장자리), `fine aerated pores, matte whipped density`(미세 기공·저광택), `textured limestone surface, mineral pitting, chalky matte`(균열·구멍 있는 흰 석회암 면), `crochet and raffia texture, hand-made resort craft detail`(수공예 질감) |
| 마감 | `subtle film grain`, `gentle vignette`, `halation around bright edges`, `clean unbranded finish` |
| 피부 | `natural skin texture, visible pores, subtle film grain`, fine facial texture, soft tonal variation, fine vellus hair |
| 피부 — 촉촉 | `hydrated skin base, moisture-rich finish, dewy but natural skin` |
| 피부 — 유리알 투명 | `translucent skin clarity, visible texture, non-plastic glow`(반투명하되 모공은 유지) |
| 피부 — 꿀광 | `inner honey glow, warm luminous skin, subtle cheek highlight` |
| 피부 — 부분 매트 | `matte T-zone, controlled forehead shine, balanced dewy finish` |
| 피부 실패조건 짝 | `skin undertone preserved under split lighting` — §7.2 색온도 분리 조명에서 피부톤이 죽지 않게 병기 |
| 로고·워터마크 의도 | `clean, brand-free, copy-free finish` |

### 7.7 장르 즉시조합

| 장르 | 결과 토큰 묶음 |
|---|---|
| 패션 에디토리얼 | soft diffuse key + neutral palette + shallow DoF + magazine margins |
| 네온 누아르 | practical neon glow, teal&orange, wet reflective street, low-angle dutch |
| 스트리트 다큐 | available light, slightly desaturated, candid framing, deep focus |
| 제품 히어로 | clean softbox gradient, single hero spotlight, cool rim, HEX 배경 / 변주 gravity-balanced stacking, implied instability(아슬아슬한 균형 구성) |
| 제품 플랫레이 | clean top-down flatlay + even soft light + generous margins + single hero with subordinate props |
| 한국 웹툰 | soft cel shading, glossy K-beauty finish, dewy highlights, vertical scroll |

### 7.8 국문/영문 혼용 규칙

| 이기는 언어 | 영역 |
|---|---|
| **한국어 승** | 장면 서사 골격(누가·어디서·무엇을) · 무드 형용(아련한, 서늘한) · 문화 부하 명사(남성지풍, 청순, 물오른) · 렌더될 한글 카피 |
| **영어 승** | 심도(shallow DoF, deep focus) · 조명(rim light, key:fill 1:2, clamshell) · 필름(Portra emulation, halation) · 포즈 술어(contrapposto, over-the-shoulder) · 티어 고정 문구(Tier-1/Tier-2 캐노니컬) · HEX 주변 기술 토큰(gradient, duotone) |

하이브리드 패턴 = 한국어 골격 문장에 영어 기법 토큰 삽입.

1. `창가의 아침빛 아래 선 인물, soft window light from camera left, shallow DoF, 배경은 크림 #F7F4EC 단색.` — 한국어 골격 + 영어 조명/심도 토큰.
2. 조명 서술은 `부드러운 실내 자연광과 약한 필라이트` vs `soft window light, gentle fill` 어느 쪽도 허용한다. 단, 한 문장의 골격 언어는 통일한다. 반쪽짜리 번역체 금지.

렌더 텍스트는 한 줄 한 언어다. 한 따옴표 문자열 안 KO+EN 혼합 금지(`W-TEXT-MIXLANG`). 인물 신원은 고정 디테일로 쓴다. 실재 인물·상표 대신 가상 페르소나/브랜드를 쓴다.
