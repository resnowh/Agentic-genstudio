# Architecture

Codex Creator Agent is a local orchestration layer. The user gives natural
language instructions; the agent plans and executes through hidden backend
adapters.

## Flow

```text
Natural language
  -> Intent planner
  -> Unified job
  -> Asset manager
  -> Backend router
  -> Backend adapter
  -> Result evaluator
  -> Output registry
```

## Main Components

- `planner`: Converts natural language into a structured job.
- `assets`: Reads model, character, style, and backend manifests.
- `router`: Selects the best backend for a job.
- `executor`: Runs a job through a backend adapter and records the result.
- `adapters`: Backend-specific execution implementations.

## Backend Strategy

- `diffusers`: Stable basic generation API for text-to-image, image-to-image,
  inpaint, and batch generation.
- `comfyui`: Hidden advanced workflow executor for pose control, reference
  identity, ControlNet, IPAdapter, and community workflows.
- `training`: LoRA training through kohya_ss or an equivalent local trainer.
- `three_d`: Image-to-3D through Hunyuan3D or another specialized engine.
- `dry_run`: Local validation backend used before heavyweight engines exist.

## User Contract

The user never configures nodes, workflows, CFG, denoise, ControlNet weights,
or model paths. Those details are internal implementation choices.

