---
name: visual-commands
description: Interpret compact slash commands for image generation and image editing, especially commands such as /xray, /explodedview, /360view, /cutaway, /cinematic, /night, /productshot, /removebg, and combinations of multiple visual commands. Use whenever a user attaches/references an image and enters one or more supported slash commands, or asks to use the Visual Commands syntax. Resolve command composition, conflicts, parameters, preservation rules, camera/layout behavior, and then execute the image task with the available image-generation/editing tool.
---

# Visual Commands

Turn short slash-command requests into precise, consistent image-generation/editing operations.

## Trigger behavior

When the user supplies an image plus a recognized command such as `/xray`, do not require a long prompt. Interpret the command according to this skill and execute the image edit.

When multiple commands are supplied, combine them according to `references/composition.md`.

Examples:
- `[image] /xray`
- `[image] /xray /cinematic /night`
- `[image] /360view /productshot /blackbg`
- `[image] /remove chair /add walnut desk /goldenhour`
- `[image] /explodedview /technical /whitebg /16:9`

## Required workflow

1. Verify that a usable image exists when the command requires an edit.
2. Parse slash commands left-to-right.
3. Normalize aliases using `references/commands.json`.
4. Resolve parameters and conflicts using `references/composition.md`.
5. Preserve the source by default:
   - same subject identity and defining features;
   - same proportions and geometry;
   - same camera, pose and composition unless a camera/layout command changes them;
   - same background unless an environment/background command changes it;
   - do not add unrelated text, labels, logos, props or redesigns.
6. Build one unified image instruction, not one separate generation per modifier.
7. Use the available built-in image generation/editing tool by default.
8. Do not show the internal compiled prompt unless the user explicitly requests it.
9. After successful image generation/editing, follow the host product's normal image-response behavior.

## Command composition

Default: commands are additive.

`/xray /cinematic /night`
means:
- structural transform: X-ray;
- visual direction: cinematic;
- environment: night.

Conflicts use last-explicit-command-wins:
- `/day /night` -> `/night`
- `/blackbg /whitebg` -> `/whitebg`
- `/frontview /rearview` -> `/rearview`
- `/9:16 /16:9` -> `/16:9`

Master commands control output structure. Notable masters:
`/360view`, `/turnaround`, `/orthographic`, `/explodedview`, `/layers`,
`/blueprint`, `/schematic`, `/beforeafter`, `/contactsheet`.

Other commands modify the master:
`/360view /productshot /blackbg` means every angle uses the requested product-shot and black-background treatment.

For all detailed rules read `references/composition.md`.
For command definitions and aliases read `references/commands.json`.
For user-facing command discovery read `references/COMMANDS.md`.
For patterns read `references/examples.md`.

## Natural-language coexistence

Slash commands can be mixed with normal language.

Examples:
- `/xray but keep the original background`
- `/360view /views 12 on a white studio background`
- `/color body matte black /samecolors` is contradictory only for the target changed by `/color`; preserve all other colors.
- `Make it more premium /cinematic /night`

Natural language has equal authority to explicit commands. If natural language directly contradicts a slash command, the later instruction in reading order wins.

## Parameterized commands

Supported parameterized commands include:
- `/remove <thing>`
- `/add <thing>`
- `/replace <from> -> <to>`
- `/color <target?> <color>`
- `/materialswap <from> -> <to>`
- `/changebg <description>`
- `/bg <description>`
- `/weather <description>`
- `/time <description>`
- `/season <season>`
- `/style <description>`
- `/views <number>`

Parameter text runs until the next slash command.

## Unknown commands

Do not invent a hidden meaning for an unknown slash command.
If there is an obvious typo or alias, map it to the closest known command.
Otherwise briefly say it is not in Visual Commands and suggest the closest known command(s).

## Quality standard

Results should feel intentionally art-directed rather than prompt-stacked:
- one coherent lighting model;
- one coherent camera model;
- physically plausible materials and reflections for photoreal work;
- consistent identity across multi-view outputs;
- no accidental duplication of parts;
- no unexplained labels or UI text;
- source fidelity takes precedence over decorative flourish.

For multi-view output, consistency between views is more important than adding extra detail.
For X-ray/cutaway/exploded views, structural plausibility and clear part relationships are more important than ornamental complexity.
