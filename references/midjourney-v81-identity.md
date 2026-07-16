# Midjourney v8.1 — identity-locked portrait and turnaround prompts

Use this only when the target is Midjourney v8.1 and the user needs face identity preserved from a reference image.

## Reference syntax

- (2026-07 실측) Midjourney v8.1에서 `--oref` / `--ow`를 사용하지 않는다.
- 참조 이미지는 일반 image prompt URL로 프롬프트 맨 앞에 둔다: `<reference-url> <text prompt>`.
- 이미지 영향도 조절이 필요하면 해당 v8.1 런타임 UI에서 실제 지원되는 image-weight 설정을 먼저 확인한다. 확인되지 않은 플래그를 추정해 붙이지 않는다.
- 얼굴 재현 우선 패스에서는 moodboard·personalization modifier를 생략하고, 기본 이미지 프롬프트가 안정된 뒤 하나씩 추가한다.

## Compact prompt delivery

- Midjourney prompts should be materially shorter than the general 2000-character ceiling. For a single portrait, target roughly **400–800 characters** unless the user explicitly requests a dense prompt.
- Put the user-provided image URL directly at the beginning of the copyable prompt; do not merely mention the link outside it.
- Preserve only identity geometry, pose, styling, lighting, lens, and mood. Remove explanatory prose, repeated synonyms, and low-impact micro-details.
- If the user rejects a nationality label, replace it with the requested broad descriptor (for example, `East Asian`) and preserve the intended appearance through directly observable facial geometry rather than nationality-based inference.
- Return the finished prompt first in one copyable block. Keep notes to one short line or omit them.

## Output layout

- **Four full-body turnaround views on one canvas:** use horizontal `--ar 3:2`; explicitly state one horizontal row, generous spacing, and full body from head to feet.
- **Face reconstruction:** do not make a grid. Generate independent chest-up portraits at `--ar 3:4` with the same reference supplied for every job.

## Active UI and ten-angle sequence

1. Inspect the Midjourney Web **Create settings** first. The visible model setting and the result-card label are authoritative; do not add a remembered `--v` token merely to force the UI selection.
2. Verify one minimal front-facing reference job in that same UI/model configuration before any batch. Parameter forms and batch support are runtime-sensitive.
3. For face fidelity, use ten independent jobs with the same reference and identity core; change **only** the angle clause per job: front, 15°/30°/45° left, left profile, 15°/30°/45° right, right profile, and a near-front high 15° view.
4. Do not assume permutation/batch syntax will compose with an external identity reference. If a single job is proven but a batch errors, keep the sequence as independent jobs instead of retrying an opaque batch.
5. A repeat count produces variants of one angle, not a controlled ten-angle set.

## Identity prompt core

State that facial identity is the highest priority and name stable, visible characteristics: face geometry, eye shape and spacing, brow angle/density, nose bridge and tip, lip outline, cheek contour, jawline, hairline, hairstyle. Specify chest-up framing and neutral expression for angle-comparison cuts.
