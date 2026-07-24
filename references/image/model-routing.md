# 모델 라우팅 — 목적축 → 후보 모델 (S2 플랫폼 표면)

**이 파일은 후보를 좁히는 용도다. 파라미터의 정본이 아니다.** 실제 파라미터·비율·미디어 롤은 런타임 확인(`models_explore`)이 이긴다. 표면 판정은 [surfaces.md](surfaces.md)가 선행한다.

"Higgsfield"는 엔진 하나가 아니라 여러 공급자의 모델을 호스팅하는 **플랫폼**이다. "Higgsfield로 간다"는 라우팅 결정이 아니며, 목적축에서 **모델 id**까지 내려가야 결정이 끝난다.

## 1. 이미지 — 목적축 라우팅

| 목적 | 1순위 | 대안 | 결정 파라미터 |
|---|---|---|---|
| 정확한 텍스트 렌더·타이포·로고 배치 | `openai_hazel` ⚠️비율제약 | `nano_banana_pro`, `gpt_image_2` | `quality`(hazel) / `resolution`(nbp, gpt) |
| 다이어그램·인포그래픽·도해 | `nano_banana_pro` | `openai_hazel`, `gpt_image_2` | `resolution: 2k~4k` |
| 벡터 로고·아이콘·플랫 브랜드 자산 | `recraft_v4_1` | — | `model_type: vector`/`utility_vector`, `colors[]`, `background_color` |
| 제품컷·목업(깨끗·정면·예측가능) | `recraft_v4_1` `model_type: utility` | `marketing_studio_image` | `background_color`, `resolution` |
| 인물 사실감·UGC·패션 에디토리얼 | `soul_2` (=`soul_v2`) | `nano_banana_2`, `seedream_v5_pro` | `quality: 1.5k/2k`, `soul_id` |
| 동일 인물 시리즈 | `soul_2` + `soul_id` | `soul_cast`(시네마틱 아이덴티티) | `soul_id` |
| 시네마 스틸·컨셉아트 | `soul_cinematic` | `cinematic_studio_2_5` | `quality` / `resolution: 4k` |
| 지시 기반 편집·변형 | `seedream_v5_pro` | `seedream_v5_lite`, `flux_kontext`, `openai_hazel` | `resolution: 1k/1.5k/2k` |
| 스타일 전이·컨텍스트 편집 | `flux_kontext` | `seedream_v5_pro` | — |
| 프롬프트 준수 정밀도 | `flux_2` | `nano_banana_pro` | `variant: pro/flex/max`, `resolution` |
| 초고해상(4K 이상) | `seedream_v4_5` (`quality: high` ~6K) | `nano_banana_2/pro`, `gpt_image_2`, `cinematic_studio_2_5` (4k) | `quality` / `resolution` |
| 광각·와이드 비율(21:9 등) | `kling_omni_image` | `nano_banana_*`, `seedream_v5_pro`, `recraft_v4_1` | `aspect_ratios` 배열 확인 |
| 표현적·고대비 크리에이티브 | `grok_image` | `flux_2` | `mode: std/quality` |
| 빠르고 싼 시안 스윕 | `z_image` | `nano_banana`, `nano_banana_2_lite` | `thinking: MINIMAL/HIGH`(lite) |
| DTC 광고 크리에이티브 | `ms_image` | `marketing_studio_image` | `style_id`(**필수**), `brand_kit_id`, `product_ids` |
| 게임 스프라이트 시트 | `autosprite` | — | `kind`, `frame_count`, `frame_size`, `video_tier` |
| 모델 선택이 실제로 무의미할 때 | `image_auto` | — | 없음 |

**⚠️비율제약 — `openai_hazel`은 요구 비율을 못 낼 수 있다.** `aspect_ratios`가 `1:1`·`3:2`·`2:3`·`auto` 4종뿐이다(2026-07-25 런타임 확인). 즉 **타이포 포스터 라우터의 `9:16`, promo 라우터의 `4:5`, 덱·배너의 `16:9`는 이 모델로 낼 수 없다.**

- 정사각·세로 `2:3`·가로 `3:2`면 `openai_hazel` 그대로 간다(텍스트 렌더 축의 1순위는 유지).
- **그 밖의 세로/와이드 비율이 필요하면 `nano_banana_pro`로 내려간다** — `1:1`·`3:2`·`2:3`·`4:3`·`3:4`·`4:5`·`5:4`·`9:16`·`16:9`·`21:9`(2026-07-25 런타임 확인)로 위 세 요구를 모두 흡수한다.
- `gpt_image_2`는 `16:9`·`9:16`은 되지만 `4:5`·`21:9`가 없다(2026-07-25 런타임 확인). 덱·숏폼 전용 대안으로만 쓴다.

**표 전체에 적용:** 1순위는 목적축 기준이며 비율을 보장하지 않는다. 레인이 비율을 요구하면 후보를 고른 뒤 그 모델의 `aspect_ratios`를 반드시 대조하고, 없으면 대안 열로 내려간다(규칙 4).

**후처리 전용**(생성 모델 아님): `image_background_remover`, `outpaint`, `topaz_image`, `topaz_image_generative`, `bytedance_image_upscale`.

## 2. 영상 — 목적축 라우팅

| 목적 | 1순위 | 대안 | 결정 파라미터 |
|---|---|---|---|
| 최고급 시네마틱 | `veo3_1` | `cinematic_studio_3_0`, `kling3_0` | `quality: basic/high/ultra`, `variant`, `duration: 4/6/8` |
| 장르 제어·다중 샷 | `cinematic_studio_video_v2` | `kling3_0` | `genre`, `multi_shots`, `cfg_scale`, `speedramp`, `mode` |
| 레퍼런스 기반 아이덴티티 유지 | `seedance_2_0` | `seedance_2_0_mini`, `gemini_omni` | `image_references`/`video_references`/`audio_references`, `mode`, `resolution` |
| 제품·멀티 SKU 커머스 | `seedance_2_0` | `marketing_studio_video` | `product_ids`(MS), `generate_audio` |
| 물리·표정 자연스러움 | `minimax_hailuo` | `kling2_6` | `variant`, `duration: 6/10`, `resolution` |
| 오디오 동기·캐릭터 일관 | `wan2_7` | `kling3_0`, `seedance_2_0` | `duration: 2~15`, `resolution` |
| 시작·끝 프레임 지정 | `seedance_2_0`, `minimax_hailuo`, `kling3_0`, `wan2_7` | `veo3_1_lite` | `start_image` / `end_image` 롤 |
| 빠르고 싼 배치 | `veo3_1_lite` | `kling3_0_turbo`, `seedance_2_0_mini` | `generate_audio: false` |
| 실험적·스타일라이즈 | `wan2_6` | `grok_video` | `quality`, `duration: 5/10/15` |
| 프리셋 바이럴 템플릿(i2v) | `higgsfield_preset` | — | `preset_id`(**필수**, `presets_show`) |
| 마케팅 UGC·릴스 | `marketing_studio_video` | — | `mode`(프리셋 slug), `hook_id`/`setting_id` **또는** `ad_reference_id`(상호배타) |
| 유튜브 → 숏폼 클립 | `clipify` | — | `clips_num`, `clip_aspect`, 자막 파라미터 |

**후처리 전용**: `video_background_remover`/`sam_3_video`, `topaz_video`, `bytedance_video_upscale`, `video_upscale`, `video_deflicker`, `sync_so`(립싱크), `reframe`.

## 3. 라우팅 규칙

1. **사용자가 모델을 지정하면 그대로 쓴다.** 지정이 없을 때만 이 표를 쓴다.
2. **목적이 둘이면 컷을 나눈다.** "정확한 한글 카피 + 인물 사실감"은 한 모델의 최적점이 아니다. 텍스트 컷과 인물 컷을 분리한다.
3. **모델을 바꾸면 프롬프트도 바꾼다.** 같은 문장을 다른 모델에 그대로 옮기지 않는다. 특히 Soul 계열의 4레이어 구조([soul-v2-director.md](soul-v2-director.md))는 Soul 전용이다.
4. **비율·해상도는 모델이 정한다.** 배열이 비어 있지 않은데 원하는 비율이 그 모델의 `aspect_ratios`에 없으면 모델을 바꾸거나 비율을 바꾼다. 프롬프트로 우회하지 않는다. **배열이 비어 있는 경우는 다르다** — `minimax_hailuo`·`autosprite`·`clipify`·`tripo_3d`처럼 빈 배열인 모델은 비율을 파라미터로 받지 않으므로 비율을 넘기지 않고 입력 이미지·모델 기본값을 따른다([surfaces.md](surfaces.md) §2). 이걸 "비율 없음 = 부적합"으로 읽고 1순위를 버리지 않는다.
5. **영상 길이는 임의 값이 아니다.** 열거값(`5/10`, `4/8/12`, `6/10`)인 모델과 범위(`3~15`, `4~15`)인 모델이 섞여 있다. 스토리보드의 씬 길이를 모델 제약에 맞춘다.
6. **네거티브 프롬프트 파라미터는 이 플랫폼의 이미지·영상 생성 모델에는 없다**(2026-07-25 로스터 전수 확인, 3D 계열 `tripo_3d` 제외 — 로스터에서 `negative_prompt`를 갖는 것은 이 모델뿐이다). 따라서 이미지·영상 표면에서 배제는 긍정형 재서술로 처리한다 — 이는 플랫폼 사실이지 모든 엔진에 대한 일반 원칙이 아니다. 별도 `negative_prompt`를 가진 엔진(`tripo_3d` 포함)에서는 그 파라미터를 쓴다.

## 4. 스냅샷 신선도

<!-- roster-snapshot: 2026-07-25 -->
<!-- 위 마커가 신선도 검사의 유일한 기계 앵커다. 로스터를 다시 뜨면 이 날짜만 고치면 되고,
     아래 산문은 자유롭게 써도 검사에 영향을 주지 않는다. 마커가 없으면 검사가 loud하게 실패한다. -->

이 표는 **2026-07-25** `models_explore(action:"list")` 실측 로스터 기반이다. 모델 추가·제거·파라미터 변경은 공지 없이 일어난다.

- 30일 이내: 그대로 후보 선택에 쓴다.
- 30~90일: 후보 선택에는 쓰되, 파라미터는 반드시 `models_explore(action:"get")`로 확인한다.
- 90일 초과: 표를 근거로 단정하지 않는다. 목록부터 다시 뜬다.

과거 오판 기록: 2026-07-21에 "Seedream 계열 전체 소멸"로 결론냈으나 실제로는 `list` 페이지네이션 미진행에 따른 오판이었다. **모델이 사라졌다고 결론내기 전에 `has_more`를 끝까지 따라간다.**
