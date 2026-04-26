# Prompt Adapter

The prompt adapter is a local preprocessing layer between the user's natural
language input and the model-facing prompt used by `diffusers`.

## Why It Exists

The current production model, `Animagine XL 4.0`, responds best to English tag
style prompts. Raw Chinese prompts are not reliable enough on their own.

The adapter bridges that gap without calling an external translation service.

## Current Behavior

For Chinese input, the adapter currently:

- detects that the prompt is Chinese
- maps known Chinese terms to English anime-style tags
- prepends default quality tags
- generates a default negative prompt
- stores prompt metadata in the job parameters

For non-Chinese input, the adapter currently:

- preserves the original prompt text
- still injects the default negative prompt
- marks the adapter mode as `identity`

## Stored Fields

The adapter writes these fields into `job.parameters`:

- `prompt_language`
- `positive_prompt`
- `negative_prompt`
- `prompt_adapter`

These fields are then visible in the web task preview and available to the
backend adapter.

## Current Limits

The implementation is intentionally simple:

- rule-based keyword mapping
- no grammar understanding
- no subject disambiguation
- no style-specific prompt planning beyond a small tag map

It is useful for common anime-generation requests, but it is not a general
translation engine.

## Future Direction

The next step should be a stronger local prompt planner that can:

- parse scene roles and composition more reliably
- map camera language and pose language into better tag sets
- choose model-specific prompt templates
- adapt negative prompts per task type
- eventually support a local language model for prompt rewriting
