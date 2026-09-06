# Composition Engine

Use these rules whenever one or more slash commands are present.

## 1. Parse
Read every slash token in left-to-right order. Normalize aliases to canonical names.
For parameterized commands, bind free text after the command until the next slash token.

Examples:
- `/remove red car /night` -> remove=`red car`; then night.
- `/replace blue chair -> leather chair /studio` -> replacement + studio.
- `/360view /views 8 /blackbg` -> 8-view 360 presentation on black.

## 2. Classify
Commands are classified by category in `commands.json`.

- `transform`: changes internal/structural representation.
- `camera`: changes view or creates multi-view output.
- `action`: targeted edits such as add/remove/replace/color.
- `material`: surface/material changes.
- `environment`: time/weather/location context.
- `background`: isolation or background replacement.
- `lighting`: lighting treatment.
- `look`: visual/art direction.
- `optics`: depth-of-field / shutter / lens behavior.
- `composition`: framing.
- `fidelity`: preservation/quality constraints.
- `layout`: comparison/contact-sheet structure.
- `output`: aspect ratio/orientation.

## 3. Combine by default
Commands from different categories are additive unless they are inherently contradictory.

`/xray /cinematic /night`
= X-ray transform + cinematic art direction + night environment in one operation.

`/explodedview /technical /whitebg`
= exploded assembly + engineering presentation + white background.

## 4. Last-wins conflicts
When two commands set mutually exclusive values for the same property, the last explicit command wins.

- `/day /night` -> night
- `/blackbg /whitebg` -> white background
- `/frontview /rearview` -> rear view
- `/9:16 /16:9` -> 16:9

Do not treat additive conditions as conflicts:
- `/night /rain /fog` is valid.
- `/cinematic /luxury /productshot` is valid if the combination remains coherent.

## 5. Master commands
Master commands control the output structure:
`/360view`, `/turnaround`, `/orthographic`, `/explodedview`, `/layers`, `/blueprint`,
`/schematic`, `/beforeafter`, `/contactsheet`.

All normal compatible commands modify the master output.

Examples:
- `/360view /productshot /blackbg` -> every view is product-shot styled on black.
- `/beforeafter /xray /sameangle` -> left: source-like original; right: X-ray at matched angle.
- `/explodedview /carbonfiber /technical` -> exploded carbon-fiber technical presentation.

If master commands are nested logically, combine:
- `/360view /contactsheet` -> 360 views arranged as a contact sheet.
- `/beforeafter /explodedview` -> before + exploded result.
Otherwise prefer the last master unless user language explicitly requests both.

## 6. Fidelity defaults
When an image is attached and user invokes slash commands:
- preserve subject identity by default;
- preserve pose/camera/background unless a command changes them;
- do not redesign unrelated details;
- do not introduce text, labels, logos, people, props or decorations unless requested;
- maintain plausible geometry and lighting.

`/preserve`, `/sameangle`, `/samebg`, `/samecolors`, `/sameidentity` strengthen these constraints.

## 7. Execution
After resolving commands, create one concise unified image-edit instruction in this order:
1. source-fidelity requirements;
2. master/structural transform;
3. camera/view;
4. targeted actions;
5. material changes;
6. environment/background;
7. lighting/look/optics;
8. composition/output;
9. negative constraints.

When a built-in image-generation/editing tool exists, use it directly.
Do not expose the compiled internal prompt unless the user asks for it.

## 8. Missing image
If a command inherently edits an existing image (`/xray`, `/remove`, `/replace`, etc.) but no usable image is available, ask the user to attach the image.
For commands that can sensibly generate from text alone, use the supplied textual subject.

## 9. Ambiguity
Do not ask questions for harmless ambiguity when a high-quality default exists.
Ask only when the requested command requires a missing essential argument, such as `/replace` with no source or target.
