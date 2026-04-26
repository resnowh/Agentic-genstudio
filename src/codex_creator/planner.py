from __future__ import annotations

import re

from .schemas import Job, SUPPORTED_TASKS


def _contains_any(text: str, words: list[str]) -> bool:
    lowered = text.lower()
    return any(word.lower() in lowered for word in words)


def _extract_outputs(text: str, default: int = 4) -> int:
    patterns = [
        r"output\s+(\d+)",
        r"generate\s+(\d+)",
        r"(\d+)\s+images?",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return max(1, min(32, int(match.group(1))))
    return default


def _extract_resolution(text: str, default: str = "1024x1024") -> str:
    match = re.search(r"(\d{3,4})\s*[xX*]\s*(\d{3,4})", text)
    if match:
        return f"{match.group(1)}x{match.group(2)}"
    return default


def _extract_input_images(text: str) -> list[str]:
    image_pattern = r"[\w./\\:-]+\.(?:png|jpg|jpeg|webp|bmp)"
    return re.findall(image_pattern, text, re.IGNORECASE)


def _has_reference_intent(text: str) -> bool:
    markers = [
        "reference image",
        "reference photo",
        "input image",
        "source image",
        "use this image",
        "use this photo",
        "from this image",
        "based on this image",
        "reference",
        "photo",
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".bmp",
        "图片",
        "照片",
        "参考图",
        "原图",
    ]
    return _contains_any(text, markers)


def plan(prompt: str, task_type_override: str | None = None) -> Job:
    text = prompt.strip()
    lower = text.lower()
    input_images = _extract_input_images(text)

    task_type = "text_to_image"
    preserve: list[str] = []
    change: list[str] = []

    has_image = bool(input_images) or _has_reference_intent(lower)
    wants_train = _contains_any(lower, ["train", "lora"])
    wants_3d = _contains_any(lower, ["3d", "mesh", "glb", "obj"])
    wants_pose = _contains_any(lower, ["pose", "action", "sitting", "standing", "running"])
    wants_inpaint = _contains_any(lower, ["inpaint", "mask", "region"])
    wants_upscale = _contains_any(lower, ["upscale"])

    if wants_train and _contains_any(lower, ["style"]):
        task_type = "style_training"
    elif wants_train:
        task_type = "character_training"
    elif wants_3d:
        task_type = "image_to_3d"
    elif wants_inpaint:
        task_type = "inpaint"
    elif wants_pose and has_image:
        task_type = "pose_transfer"
        preserve.extend(["identity", "face", "hair"])
        change.append("pose")
    elif has_image and _contains_any(lower, ["keep", "preserve", "same"]):
        task_type = "character_reference"
        preserve.extend(["identity", "face"])
    elif has_image:
        task_type = "image_to_image"
    elif wants_upscale:
        task_type = "upscale"

    if task_type_override and task_type_override in SUPPORTED_TASKS:
        task_type = task_type_override

    style = "anime" if _contains_any(lower, ["anime"]) else None

    return Job(
        prompt=text,
        task_type=task_type,
        input_images=input_images,
        preserve=preserve,
        change=change,
        style=style,
        outputs=_extract_outputs(text),
        resolution=_extract_resolution(text),
        parameters=_recommended_parameters(task_type, style),
    )


def _recommended_parameters(task_type: str, style: str | None) -> dict[str, object]:
    params: dict[str, object] = {
        "seed": "auto",
        "safety": "local_policy",
    }
    if task_type in {"text_to_image", "batch_variation"}:
        params.update({"steps": 28, "cfg": 5.0, "sampler": "euler"})
    elif task_type == "image_to_image":
        params.update({"steps": 28, "cfg": 5.0, "denoise": 0.45})
    elif task_type == "pose_transfer":
        params.update({"steps": 30, "cfg": 5.0, "denoise": 0.65, "pose_weight": 0.8, "identity_weight": 0.75})
    elif task_type == "character_reference":
        params.update({"steps": 30, "cfg": 5.0, "denoise": 0.55, "identity_weight": 0.8})
    elif task_type == "inpaint":
        params.update({"steps": 28, "cfg": 5.0, "denoise": 0.6})
    elif task_type.endswith("_training"):
        params.update({"rank": 16, "epochs": "auto", "captioning": "auto"})
    elif task_type == "image_to_3d":
        params.update({"format": "glb", "texture": True})

    if style == "anime":
        params["negative_prompt"] = "low quality, blurry, bad anatomy, text, watermark"
    return params
