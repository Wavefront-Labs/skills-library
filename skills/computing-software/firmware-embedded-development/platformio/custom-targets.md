---
id: computing-software.firmware-embedded-development.platformio.custom-targets
name: custom-targets
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [extra-scripts, custom-target, addcustomtarget, pio-run-t, project-tasks, always-build, platformio, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Add project-specific PlatformIO targets (pio run -t <name>) with env.AddCustomTarget: provisioning, erase, flash filesystem plus app, factory images."
sources:
  - https://docs.platformio.org/en/latest/scripting/custom_targets.html
  - https://docs.platformio.org/en/latest/core/userguide/cmd_run.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom PlatformIO targets

**Goal:** team tasks (provision serial numbers, flash a factory image, run a host tool) as
`pio run -t <target>` commands, listed by `pio run --list-targets`.

## Defining a target
```python
# platformio.ini: extra_scripts = scripts/targets.py
Import("env")

env.AddCustomTarget(
    name="provision",
    dependencies="$BUILD_DIR/${PROGNAME}.bin",       # built first; None = no dependencies
    actions=[
        "$PYTHONEXE scripts/provision.py --port $UPLOAD_PORT --fw $SOURCE",
    ],
    title="Provision device",
    description="Write serial number and keys, then flash firmware",
    always_build=True)                               # default; run even if dependencies are built
```
Signature: `AddCustomTarget(name, dependencies, actions, title=None, description=None,
always_build=True)`. `actions` is one command string or a list mixing command strings and Python
callables. Names should be ASCII (a-z, 0-9, `_`, `-`); keep `title` to 1-2 words. Title and
description are shown by PlatformIO Core and the IDE.

Run: `pio run -e board -t provision` (add `--upload-port <port>` to set `$UPLOAD_PORT`).

## More examples
- Command shortcut: `env.AddCustomTarget("sysenv", None, 'python -c "import os; print(os.environ)"')`.
- Python callback as a target:
  ```python
  host = env.GetProjectOption("custom_ping_host")   # custom_* option in platformio.ini

  def ping_callback(*args, **kwargs):
      env.Execute("ping " + host)

  env.AddCustomTarget("ping", None, ping_callback)
  ```
- Target depending on firmware: `env.AddCustomTarget("ota", "$BUILD_DIR/${PROGNAME}.elf",
  "ota_script --firmware-path $SOURCE")`.
- Do not duplicate built-in targets: `monitor` and `envdump` are built in, and `upload`,
  `uploadfs` and `size` are named built-ins (`erase` is documented for ESP32).

## Variables seen in the documented examples
`$BUILD_DIR`, `$PROGNAME`, `$SOURCE`, `$PYTHONEXE`, `$UPLOAD_PORT`, `$PIOENV`, `$PROJECT_DIR`.
List what is defined with `pio run -t envdump`.

## Gotchas
- `always_build=False` means the target is not called when its declared dependencies are already
  built; leave the default `True` for side-effect tasks.
- Long-running Python in `actions` blocks the caller; print progress.

## Verify
- [ ] The target appears in `pio run --list-targets`.
- [ ] Target works from a clean checkout on Windows and Linux (no hard-coded paths or
      shell-isms).

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19), scripting/custom_targets
and core/userguide/cmd_run pages. Confirmed: `AddCustomTarget` signature and argument semantics,
`always_build` behaviour, the `$BUILD_DIR/${PROGNAME}.elf` and `$SOURCE` forms, callback and
`GetProjectOption` example, `--list-targets`, built-in `monitor` and `envdump` targets. Removed
as unconfirmed: the IDE Project Tasks panel claim, the erase-then-flash chain, the `compiledb`
mention, the "runs once then never" claim and the Windows `COM5` example.
Method: documentation only; no commands were run.
