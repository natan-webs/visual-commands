# Contributing to Visual Commands

Contributions are welcome! Whether adding new visual commands, refining composition rules, expanding documentation, or adding test cases, follow these guidelines to keep Visual Commands modular and deterministic.

## Command Guidelines

New commands must be added to [`skills/visual-commands/references/commands.json`](skills/visual-commands/references/commands.json) with:
- `name`: Lowercase canonical command identifier (e.g. `xray`, `isometric`, `16:9`).
- `description`: Clear, concise explanation of the visual effect.
- `prompt`: Execution directive used when compiling the image-generation plan.
- `category`: Functional category (`action`, `background`, `camera`, `composition`, `environment`, `fidelity`, `layout`, `lighting`, `look`, `material`, `optics`, `output`, `transform`).
- `mode`: `modifier` (default) or `master` (for structural/multi-view layouts).
- `aliases`: Optional list of common alias shortcuts without conflicts.
- `parameters`: Optional parameter specification if the command takes free-text arguments.

### Design Principles

Every command should:
1. **Express reusable visual intent**: Avoid hyper-specific or one-off modifications.
2. **Compose predictably**: Follow additive rules across categories and last-command-wins within mutually exclusive categories.
3. **Avoid duplication**: Check existing commands and aliases before adding a new command.
4. **Preserve source fidelity**: Maintain subject identity and proportions by default unless the command explicitly changes them.

## Documentation and Tests

When adding or modifying a command:
1. Update [`skills/visual-commands/references/COMMANDS.md`](skills/visual-commands/references/COMMANDS.md) in the appropriate category section.
2. Add an example in [`skills/visual-commands/references/examples.md`](skills/visual-commands/references/examples.md) when the command's behavior or composition is non-obvious.
3. Run the validation and compiler test suite:
   ```bash
   python tests/test_compiler.py
   ```
4. Submit a pull request with a clear description of the changes.
