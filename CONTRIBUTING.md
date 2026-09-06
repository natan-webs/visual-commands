# Contributing

New commands should be added to `skills/visual-commands/references/commands.json`
with a concise description, execution prompt, category, aliases, mode, parameters,
and conflict behavior where needed.

A command should:
1. express a reusable visual intent;
2. have predictable composition behavior;
3. avoid duplicating an existing command or alias;
4. preserve source fidelity unless the command explicitly changes it.

When adding a command, also add it to `references/COMMANDS.md` and add at least one
example when its behavior is non-obvious.
