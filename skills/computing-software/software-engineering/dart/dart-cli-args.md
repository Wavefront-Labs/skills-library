---
id: computing-software.software-engineering.dart.dart-cli-args
name: dart-cli-args
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-cli, cli-args]
level: practitioner
status: docs-checked
description: "Build Dart CLIs with the cli template, package:args ArgParser and dart compile exe."
sources: ["https://dart.dev/tools/dart-create", "https://pub.dev/packages/args", "https://dart.dev/tools/dart-compile"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dart create, package:args and executables
- `dart create` has a `cli` template: a command-line application with basic argument parsing using `package:args`.
- `package:args`: create an `ArgParser`, define options with `addOption()` and flags with `addFlag()`; `abbr:` gives a one-letter form (`parser.addFlag('verbose', abbr: 'v')`), `defaultsTo:` and `allowed:` constrain values. Parse with `parser.parse(args)`; `parser.usage` gives help text; `CommandRunner` supports subcommands.
- `dart compile exe bin/myapp.dart -o <path>` produces a self-contained executable (machine code plus a small Dart runtime) for Windows, macOS or Linux; it is architecture-specific. It does not run build hooks.
- `dart pub global activate` installs a package's executables from pub.dev.
Verify: run the tool with `--help` and with an unknown flag.

## Checked
2026-11-03. Confirmed against dart.dev tools/dart-create (cli template), tools/dart-compile (exe subcommand, `-o`, architecture-specific, build hooks), tools/pub/cmd/pub-global and the package:args README (addOption, addFlag, abbr, defaultsTo, allowed, parse, usage, CommandRunner). Removed: exit code 64 convention, `--target-os` remark and the `bin/my_tool.dart` layout (not on the pages read).
Method: documentation only; no commands were run.
