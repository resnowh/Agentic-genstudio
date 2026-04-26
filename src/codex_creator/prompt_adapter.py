from __future__ import annotations

import re


QUALITY_TAGS = [
    "masterpiece",
    "best quality",
    "high score",
    "great score",
    "absurdres",
]

NEGATIVE_TAGS = [
    "lowres",
    "bad anatomy",
    "bad hands",
    "missing fingers",
    "extra digits",
    "fewer digits",
    "cropped",
    "worst quality",
    "low quality",
    "low score",
    "bad score",
    "average score",
    "text",
    "signature",
    "watermark",
    "username",
    "blurry",
]


ZH_TAGS = {
    "女孩": "1girl",
    "少女": "1girl",
    "萝莉": "petite girl",
    "小萝莉": "petite girl",
    "男孩": "1boy",
    "少年": "1boy",
    "银发": "silver hair",
    "白发": "white hair",
    "黑发": "black hair",
    "蓝发": "blue hair",
    "粉发": "pink hair",
    "金发": "blonde hair",
    "红发": "red hair",
    "长发": "long hair",
    "短发": "short hair",
    "双马尾": "twintails",
    "蓝眼": "blue eyes",
    "红眼": "red eyes",
    "绿眼": "green eyes",
    "紫眼": "purple eyes",
    "金色眼睛": "golden eyes",
    "坐着": "sitting",
    "站着": "standing",
    "跑步": "running",
    "走路": "walking",
    "躺着": "lying",
    "回头": "looking back",
    "微笑": "smile",
    "哭": "crying",
    "害羞": "blush",
    "仰视": "low angle",
    "仰拍": "low angle",
    "低角度": "low angle",
    "俯视": "high angle",
    "广角": "wide angle",
    "超广角": "ultra wide angle",
    "近大远小": "foreshortening",
    "空间感": "depth of field",
    "空间冲击": "dynamic composition",
    "视觉冲击": "dynamic composition",
    "冲击力": "dynamic composition",
    "全身": "full body",
    "半身": "upper body",
    "特写": "close-up",
    "侧脸": "profile",
    "雨夜": "rainy night",
    "雨": "rain",
    "霓虹": "neon lights",
    "街道": "street",
    "城市": "city",
    "森林": "forest",
    "海边": "beach",
    "室内": "indoors",
    "窗边": "by window",
    "教室": "classroom",
    "赛博朋克": "cyberpunk",
    "和风": "japanese clothes",
    "女仆": "maid",
    "制服": "school uniform",
    "连衣裙": "dress",
    "短裙": "short skirt",
    "兔耳": "rabbit ears",
    "猫耳": "cat ears",
    "二次元": "anime style",
    "动漫": "anime style",
    "精致": "detailed",
    "背景": "detailed background",
}


def adapt_prompt(prompt: str) -> dict[str, object]:
    """Return local prompt metadata without calling external services."""
    normalized = " ".join(prompt.split())
    language = "zh" if _contains_cjk(normalized) else "en"
    if language != "zh":
        return {
            "prompt_language": language,
            "positive_prompt": normalized,
            "negative_prompt": ", ".join(NEGATIVE_TAGS),
            "prompt_adapter": "identity",
        }

    tags = _dedupe([*QUALITY_TAGS, *_zh_tags(normalized), *_preserve_ascii_tags(normalized)])
    return {
        "prompt_language": language,
        "positive_prompt": ", ".join(tags),
        "negative_prompt": ", ".join(NEGATIVE_TAGS),
        "prompt_adapter": "zh_cn_rule_based_v1",
    }


def _contains_cjk(text: str) -> bool:
    return any("\u4e00" <= char <= "\u9fff" for char in text)


def _zh_tags(text: str) -> list[str]:
    tags: list[str] = []
    for keyword, tag in ZH_TAGS.items():
        if keyword in text:
            tags.append(tag)
    return tags


def _preserve_ascii_tags(text: str) -> list[str]:
    # Keep existing model-friendly tags that the user may mix into a Chinese prompt.
    pieces = re.split(r"[,，、;；\n]+", text)
    return [piece.strip() for piece in pieces if piece.strip() and piece.strip().isascii()]


def _dedupe(tags: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for tag in tags:
        normalized = tag.strip()
        if not normalized:
            continue
        key = normalized.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(normalized)
    return result
