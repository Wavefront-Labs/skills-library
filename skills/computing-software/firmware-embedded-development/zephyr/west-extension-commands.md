---
id: computing-software.firmware-embedded-development.zephyr.west-extension-commands
name: west-extension-commands
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [west-extension, west-commands-yml, westcommand, custom-west-command, west, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Add a custom west command (e.g. west sign or west release) from your manifest repo: west-commands.yml, a WestCommand subclass, argument parsing, and discovery."
sources:
  - https://docs.zephyrproject.org/latest/develop/west/extensions.html
  - https://docs.zephyrproject.org/latest/develop/west/manifest.html
  - https://github.com/zephyrproject-rtos/west/blob/main/src/west/commands.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# West extension commands

## 1. Declare in the manifest
In your manifest repository's `west.yml`:
```yaml
manifest:
  self:
    path: app
    west-commands: scripts/west-commands.yml
```
(A project in `projects:` can export commands the same way with its own `west-commands:` key,
a path relative to the project root.)

## 2. Describe the command
`scripts/west-commands.yml`:
```yaml
west-commands:
  - file: scripts/west_release.py
    commands:
      - name: release
        class: Release
        help: build, sign and package firmware for release
```

## 3. Implement
`scripts/west_release.py`:
```python
from textwrap import dedent
from west.commands import WestCommand

class Release(WestCommand):
    def __init__(self):
        super().__init__(
            'release',
            '',   # help: ignored for extensions (the yml help is used)
            description=dedent('''Builds each listed board and collects the images.'''))

    def do_add_parser(self, parser_adder):
        p = parser_adder.add_parser(self.name, description=self.description)
        p.add_argument('-o', '--out', default='dist', help='output directory')
        p.add_argument('--dry-run', action='store_true')
        return p

    def do_run(self, args, unknown_args):
        self.inf(f'workspace: {self.topdir}')
        for board in ('nrf52840dk/nrf52840', 'nucleo_h743zi'):
            cmd = ['west', 'build', '-p', 'auto', '-b', board, '-d', f'build/{board.replace("/", "_")}', 'app']
            if args.dry_run:
                self.inf(' '.join(cmd))
            else:
                self.check_call(cmd)
```
`self.topdir`, `self.manifest` (the parsed manifest) and `self.config` are available. Use
`self.inf/wrn/err/die` for output (the module-level `west.log` is deprecated);
`self.check_call` runs a subprocess and raises on failure. Pass `accepts_unknown_args=True` to
the constructor if `do_run` should receive unknown arguments instead of west rejecting them.

## 4. Discover
```bash
west --help        # lists "extension commands from project manifest (path: app)"
west release --dry-run
```
West loads only `west-commands.yml` for help output; your Python file is imported only when the
command is actually run (so `west update` on an untrusted manifest does not import it).

## Gotchas
- The class name in `west-commands.yml` defaults to the command name if `class:` is omitted.
- If the command does not show, check the `west-commands` path in `west.yml` (relative to the
  project root) and run `west manifest --validate`. The schema is `west-commands-schema.yml`
  in the west repository.
- Extension commands with the same name as a built-in command are ignored.
- Set `commands.allow_extensions` to `false` to disable extensions entirely.
- Dependencies must be installed in the workspace's Python environment; document them in a
  `requirements.txt` next to the script.

## Verify
- [ ] `west --help` lists the command on a fresh `west init -l` + `west update` workspace.
- [ ] `west <cmd> -h` shows the arguments.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2) and west 1.5.0 source (commit 2026-10-20). Confirmed the three-step recipe, west-commands.yml schema and class default (extensions page), WestCommand constructor and self.topdir/manifest/config/check_call/inf/wrn/err/die (west/commands.py), west manifest --validate, and that same-named built-in commands win. Fixed: west.log is deprecated (use self.inf), help positional arg is ignored for extensions; removed the unconfirmed warn-and-skip and sys.path claims.
Method: documentation only; no commands were run.
