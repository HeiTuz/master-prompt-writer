#!/usr/bin/env python3
"""Golden prompt professionalism checks for the merged MPW output contract."""
import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GOLDEN_DIR = ROOT / "scripts" / "fixtures" / "golden"
EXPECTED_IDS = {
    "new-write",
    "revision",
    "delta",
    "system-prompt",
    "research-factcheck",
    "coding-agent",
    "business",
    "image-video",
}
DENYLIST = (
    re.compile(r"공냥이|gongnyang|specal1849|gpt-image-2|Higgsfield|Soul", re.IGNORECASE),
    re.compile(r"화보|에디토리얼|editorial|film grain|golden hour|rim light", re.IGNORECASE),
    re.compile(r"#[0-9A-Fa-f]{6}"),
    re.compile(r"\bAR\s+\d+\s*:\s*\d+", re.IGNORECASE),
)
VAGUE_WORD_DENYLIST = (
    ("적절히", re.compile(r"적절히")),
    ("알아서", re.compile(r"알아서")),
    ("잘 정리", re.compile(r"잘 정리")),
    ("최대한 자세히", re.compile(r"최대한 자세히")),
    ("최대한 빨리", re.compile(r"최대한 빨리")),
    ("필요하면", re.compile(r"필요하면")),
    ("중요한 것 위주", re.compile(r"중요한 것 위주")),
    ("완벽하게", re.compile(r"완벽하게")),
    ("깔끔하게", re.compile(r"깔끔하게")),
    ("고급스럽게", re.compile(r"고급스럽게")),
    ("nicely", re.compile(r"\bnicely\b", re.IGNORECASE)),
    ("properly", re.compile(r"\bproperly\b", re.IGNORECASE)),
    ("in detail", re.compile(r"\bin detail\b", re.IGNORECASE)),
)


def matching_vague_word(text: str) -> str | None:
    return next((term for term, pattern in VAGUE_WORD_DENYLIST if pattern.search(text)), None)


def has_denylisted_term(text: str) -> bool:
    return any(pattern.search(text) for pattern in DENYLIST)


def without_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return text
    end = re.search(r"^---\s*$", text[3:], re.MULTILINE)
    return text[3 + end.end():] if end else text


class OutputProfessionalismTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        manifest = json.loads((GOLDEN_DIR / "manifest.json").read_text(encoding="utf-8"))
        cls.entries = []
        for entry in manifest:
            payload = json.loads((GOLDEN_DIR / entry["file"]).read_text(encoding="utf-8"))
            cls.entries.append((entry["id"], payload))

    def test_manifest_has_exactly_the_contracted_ids(self):
        self.assertEqual({entry_id for entry_id, _ in self.entries}, EXPECTED_IDS)
        self.assertEqual(len(self.entries), len(EXPECTED_IDS))

    def test_all_expected_prompts_fit_the_codepoint_limit(self):
        for entry_id, payload in self.entries:
            expected = payload["expected"]
            prompts = expected.values() if entry_id == "image-video" else (expected,)
            for prompt in prompts:
                self.assertLessEqual(len(prompt), 2000, f"{entry_id} exceeds 2000 code points")

    def test_non_image_expected_prompts_have_no_image_lane_terms(self):
        for entry_id, payload in self.entries:
            if entry_id == "image-video":
                continue
            self.assertFalse(has_denylisted_term(payload["expected"]), entry_id)

    def test_non_image_expected_prompts_have_no_vague_words(self):
        for entry_id, payload in self.entries:
            if entry_id == "image-video":
                continue
            matched_term = matching_vague_word(payload["expected"])
            self.assertIsNone(matched_term, f"{entry_id}: {matched_term}")

    def test_execution_goldens_have_judgeable_completion_criteria(self):
        completion_criteria = re.compile(
            r"완료 기준|## 완료|완료 조건|Definition of Done|\bDoD\b|반환 형식",
            re.IGNORECASE,
        )
        for entry_id, payload in self.entries:
            if entry_id in {"new-write", "coding-agent", "system-prompt"}:
                self.assertRegex(payload["expected"], completion_criteria, entry_id)

    def test_image_expected_passes_the_prompt_validator(self):
        image = next(payload["expected"]["image"] for entry_id, payload in self.entries if entry_id == "image-video")
        result = subprocess.run(
            ["node", "scripts/check_prompt.mjs"],
            cwd=ROOT,
            input=image,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report["ok"])
        warning_codes = {warning["code"] for warning in report.get("warnings", [])}
        self.assertNotIn("W-HEX-MISS", warning_codes, "image golden must carry a scene-matched HEX palette")

    def test_video_expected_obeys_scene_invariants(self):
        video = next(payload["expected"]["video"] for entry_id, payload in self.entries if entry_id == "image-video")
        boundaries = list(re.finditer(r"(?m)^씬\s+\d+\s*$", video))
        self.assertTrue(boundaries, "video requires named scenes")
        negative_lines = []
        for index, boundary in enumerate(boundaries):
            scene = video[boundary.end():boundaries[index + 1].start() if index + 1 < len(boundaries) else len(video)]
            self.assertEqual(len(re.findall(r"(?m)^카메라 모션:\s*.+$", scene)), 1, "each scene needs one camera motion")
            self.assertRegex(
                scene,
                r'(?m)^Dialogue - .+?: \(.+? in Korean\) "[^"\n]+"$',
                "Korean dialogue needs the canonical English cue form",
            )
            negative_lines.extend(re.findall(r"(?m)^네거티브:\s*(.+)$", scene))
            prose = re.sub(r"(?m)^네거티브:.*$", "", scene)
            self.assertNotRegex(prose, r"없이|없는|없음|없다|않|하지 마|금지|제외", "scene prose must stay positive-form")
            self.assertNotRegex(prose, r"(?i)\bno\b|\bwithout\b", "scene prose must stay positive-form")
        self.assertTrue(negative_lines, "video golden must prove the noun-list negative form")
        for tokens in negative_lines:
            items = [token.strip() for token in tokens.split(",")]
            self.assertTrue(all(items), "negative list needs comma-separated noun tokens")
            for token in items:
                self.assertRegex(token, r"^[0-9A-Za-z가-힣·\- ]+$", f"negative token must be a bare noun: {token}")
                self.assertNotRegex(token, r"없|않|금지|아니", f"negative token must not negate: {token}")
                self.assertNotRegex(token, r"(?i)\bno\b|\bwithout\b", f"negative token must not negate: {token}")

    def test_generic_docs_do_not_leak_image_lane_terms(self):
        for path in (ROOT / "SKILL.md", ROOT / "references" / "templates.md"):
            body = without_frontmatter(path.read_text(encoding="utf-8"))
            for line_number, line in enumerate(body.splitlines(), start=1):
                if "references/image/" in line:
                    continue
                self.assertFalse(has_denylisted_term(line), f"{path.relative_to(ROOT)}:{line_number}: {line}")


if __name__ == "__main__":
    unittest.main()
