# Roadmap

Agentic GenStudio is a local AI creation studio controlled by natural language.
The long-term goal is not to expose workflow graphs; it is to let the user
describe a creative outcome and let the system choose the right local tools.

## Current Stage

The project is now past pure scaffolding and into a usable local prototype.

Implemented:

- local CLI and local web app
- unified job schema
- backend routing
- local job and result persistence
- real local text-to-image with `diffusers`
- production anime model wiring with `Animagine XL 4.0`
- progress tracking
- history preview and deletion
- rule-based Chinese prompt adaptation
- default negative prompt handling

Not yet production-complete:

- polished image upload flow
- polished image-to-image and inpaint UX
- character consistency control
- pose control
- training flows
- 3D workflows

## Product Principles

- natural-language first
- local-first execution
- backend-agnostic architecture
- reproducible job records
- hidden workflow complexity

## Phase 1: Local Orchestrator MVP

- planner
- unified job contract
- manifests
- router
- executor
- dry-run backend

Status: complete.

## Phase 2: Real Image Generation

- production anime model
- real diffusers execution
- web progress UI
- output gallery
- history preview
- Chinese prompt adaptation
- negative prompt defaults

Status: partially complete.

Remaining in this phase:

- stronger prompt adaptation
- prompt length control
- stable image-to-image and inpaint browser flow
- better model selection rules

## Phase 3: Character Control

- reference-character generation
- identity preservation
- pose transfer
- OpenPose or DWPose preprocessing
- ControlNet routing
- IP-Adapter or FaceID-style routing

Target outcome:

```text
Keep this character, change the pose to sitting by a window.
```

The system should choose the right reference and pose-control pipeline without
manual workflow editing.

## Phase 4: Training

- dataset intake
- captioning hooks
- character LoRA training
- style LoRA training
- test-grid generation
- reusable character/style cards

Target outcome:

The user can teach a character or style locally and reuse it later through the
same natural-language interface.

## Phase 5: 3D

- image-to-3D adapter
- mesh export
- texture export
- preview rendering
- GLB/OBJ/FBX output management

## Near-Term Priorities

1. strengthen the prompt adapter
2. finish browser-side image input flow
3. stabilize image-to-image and inpaint
4. add character consistency tooling
5. add pose control

## Later Work

- batch ranking and best-pick selection
- upscale and repair passes
- comic or multi-panel workflows
- reusable prompt libraries
- plugin-style backend registration
