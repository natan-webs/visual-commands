# Examples

## Single-command edits
Input: `[image] /xray`
Plan: preserve the source image; reveal plausible internal components through a transparent outer shell.

Input: `[image] /removebg`
Plan: isolate the primary subject with clean edges and transparent output if supported.

Input: `[image] /360view`
Plan: create a consistent 8-angle turntable presentation of the same subject.

## Composed commands
Input: `[car image] /xray /cinematic /night`
Plan: preserve car identity and viewpoint, reveal internals, convert environment to night, then apply premium cinematic lighting/grading.

Input: `[watch image] /360view /views 8 /productshot /blackbg`
Plan: 8 consistent angles, premium commercial product photography, seamless black background.

Input: `[shoe image] /explodedview /technical /whitebg /16:9`
Plan: exploded assembly in technical presentation on white, framed 16:9.

Input: `[room image] /remove chair /add walnut desk /goldenhour /sameangle`
Plan: remove chair, insert walnut desk, preserve camera, relight to golden hour.

## Conflicts
Input: `[image] /day /night`
Resolved: night.

Input: `[image] /frontview /rearview`
Resolved: rear view.

Input: `[image] /blackbg /whitebg /transparentbg`
Resolved: transparent background.

## Nested masters
Input: `[image] /360view /contactsheet /productshot`
Resolved: multiple consistent angles arranged into one clean contact sheet.

Input: `[image] /beforeafter /xray /sameangle`
Resolved: original-like source on one side, X-ray transformation on the other at matched framing.
