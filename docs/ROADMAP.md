# Roadmap

Agentic GenStudio is a local AI creation studio controlled by natural language.
The user describes the creative goal; the agent plans the task, selects models
and backends, manages assets, runs generation or training, and records outputs.

The product goal is not to expose advanced node graphs to the user. ComfyUI,
diffusers, trainers, 3D engines, and future tools are internal execution
backends that the agent can choose automatically.

## Current Status

- GitHub project scaffold is active.
- Local CLI and web app can accept natural-language tasks.
- The planner can detect text-to-image, image-to-image, inpaint, character
  reference, pose transfer, style training, character training, image-to-3D,
  upscale, and batch variation intents.
- Jobs, outputs, manifests, and backend adapters are structured.
- `dry_run` validates planning, routing, and persistence.
- The diffusers backend is wired for text-to-image, image-to-image, and inpaint.
- The first real-output smoke-test model is configured and can generate PNG
  files through the diffusers backend.
- The isolated `.venv-diffusers` environment is installed without touching the
  system Python.
- Verified GPU stack: Python 3.12.13, torch 2.11.0+cu130, torchvision
  0.26.0+cu130, CUDA 13.0, NVIDIA GeForce RTX 5080 Laptop GPU.

## Immediate Gap

The runtime and real-output smoke test are ready, but no production
image-generation model is configured yet. Useful image quality requires adding a
local SDXL/anime model and enabling it in the model manifest.

## Product Principles

- Natural-language first: the user gives goals, not workflow parameters.
- Agent-owned workflow: model choice, adapter choice, prompt expansion, retry
  strategy, and technical parameters are internal decisions.
- Local-first execution: user assets, jobs, outputs, and models stay on the
  local machine unless explicitly configured otherwise.
- Backend-agnostic design: diffusers, ComfyUI, training engines, and 3D engines
  are interchangeable tools behind a common job interface.
- Reproducible outputs: every job should record inputs, selected models,
  generated files, parameters, and errors.

## Phase 1: Local Orchestrator MVP

- Natural-language planner.
- Unified job schema.
- Asset manifests.
- Dry-run backend.
- Job and output records.

Status: implemented.

## Phase 2: Real Image Generation

- Add and configure the first production anime/SDXL model.
- Enable diffusers routing for real generation.
- Add text-to-image execution.
- Add image-to-image execution.
- Add inpaint execution.
- Add prompt expansion and negative prompt presets.
- Add model selection rules for anime, realistic, stylized, and utility tasks.
- Add output gallery metadata.

Target outcome: the user can type a natural-language request and receive real
images without touching model paths or workflow settings.

## Phase 3: Character Control

- Add reference-character generation.
- Add pose transfer from text, pose images, or detected skeletons.
- Add OpenPose/DWPose preprocessing.
- Add IP-Adapter, FaceID, or equivalent identity-preservation routing.
- Add ControlNet routing for pose, depth, lineart, tile, and inpaint control.
- Add character cards that store reference images, trigger phrases, preferred
  models, LoRAs, and notes.
- Add automatic retry rules.

Target outcome: the user can say "keep this character, change the action to
sitting by a window" and the agent chooses the right reference and pose-control
pipeline.

## Phase 4: Training

- Add dataset intake.
- Add image cleaning and captioning hooks.
- Add character LoRA training.
- Add style LoRA training.
- Add LoRA test grid generation.
- Add character and style cards.
- Add training job history, checkpoints, validation prompts, and comparison
  galleries.

Target outcome: the user can provide example images and ask the agent to learn a
character or art style, then reuse that learned asset in future generations.

## Phase 5: 3D

- Add image-to-3D adapter.
- Add mesh and texture export.
- Add Blender preview rendering.
- Add GLB/OBJ/FBX output management.

Target outcome: the user can provide or generate a character image and request a
3D asset export without configuring the 3D backend manually.

## Later Capabilities

- Batch generation, ranking, and automatic best-pick selection.
- Upscale, face/detail repair, and final polish passes.
- Multi-pass story or comic workflows with character consistency.
- Prompt library and reusable creative presets.
- Safety and content policy controls per backend/model.
- Plugin-style backend registration so other agents can control the same studio.
