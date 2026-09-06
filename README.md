# Visual Commands

**A compact visual command language for AI image generation and editing in Codex.**

Attach an image and type:

```text
/xray
```

Or compose commands:

```text
/xray /cinematic /night
```

```text
/360view /productshot /blackbg
```

```text
/explodedview /technical /whitebg /16:9
```

Visual Commands turns those short instructions into a consistent image-editing workflow while preserving the source image by default.

## Why

Powerful image transformations often require long prompts. Visual Commands packages reusable intent into memorable slash commands.

Instead of explaining:
> Keep the exact product identity and proportions, produce eight consistent angles, use commercial studio lighting, and put every view on a seamless black background...

write:

```text
/360view /productshot /blackbg
```

## Composition model

Commands are additive by default.

- `/xray` = structural transformation
- `/night` = environment
- `/cinematic` = art direction

So `/xray /cinematic /night` applies all three in one operation.

Mutually exclusive commands use **last command wins**:

```text
/day /night          -> night
/blackbg /whitebg    -> white background
/frontview /rearview -> rear view
/9:16 /16:9          -> 16:9
```

Master commands such as `/360view`, `/explodedview`, `/beforeafter`, and `/contactsheet`
define the result structure. Other commands modify that structure.

## Install in Codex

Ask Codex's skill installer to install the skill directory from this repository:

```text
$skill-installer install https://github.com/YOUR-USER/visual-commands/tree/main/skills/visual-commands
```

Then restart Codex if your current Codex version requires a restart for newly installed skills.

You can also copy `skills/visual-commands` into your Codex skills directory.

## Included

- `SKILL.md` — core behavior and trigger rules
- `agents/openai.yaml` — Codex UI metadata
- `references/commands.json` — canonical machine-readable command registry
- `references/COMMANDS.md` — human-readable command catalog
- `references/composition.md` — deterministic combination/conflict rules
- `references/examples.md` — usage patterns
- `scripts/compile_commands.py` — optional parser/debug helper

## Examples

```text
[attach car image]
/xray /cinematic /night
```

```text
[attach watch image]
/360view /views 8 /productshot /blackbg
```

```text
[attach room image]
/remove chair /add walnut desk /goldenhour /sameangle
```

```text
[attach shoe image]
/beforeafter /explodedview /technical /whitebg
```

## Important

Visual Commands does not add native syntax to the model itself. It is an Agent Skill that teaches Codex how to interpret and execute this compact syntax consistently using the image-generation/editing tools available in the host environment.

## License

MIT


## Version 2.0
Expanded to **322 commands** with advanced visualization, product, camera, environment, material, layout, architecture and output workflows.
