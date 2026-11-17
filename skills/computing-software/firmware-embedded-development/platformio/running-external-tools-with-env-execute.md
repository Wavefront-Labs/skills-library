---
id: computing-software.firmware-embedded-development.platformio.running-external-tools-with-env-execute
name: running-external-tools-with-env-execute
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [env-execute, verboseaction, code-generation, protobuf-nanopb, scons-command, subprocess, extra-scripts, platformio, firmware-embedded-development]
level: advanced
status: draft
description: "Run external tools from PlatformIO scripts: env.Execute vs env.Command, VerboseAction, generating sources before compile (nanopb, assets), exit-code handling and dependencies."
sources:
  - https://docs.platformio.org/en/latest/scripting/examples/index.html
  - https://docs.platformio.org/en/latest/scripting/actions.html
  - https://scons.org/doc/production/HTML/scons-user/ch19.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running external tools with env.Execute

## env.Execute: run now
`env.Execute(cmd)` runs immediately while the script is being read (before SCons builds anything)
and returns the exit code (0 = success).
```python
Import("env")
rc = env.Execute(env.VerboseAction(
    "python $PROJECT_DIR/tools/gen_regs.py --out $PROJECT_DIR/src/gen/regs.h",
    "Generating register map"))
if rc != 0:
    env.Exit(1)            # fail the build explicitly
```
Good for one-off generation that must exist before the source scan (headers your code includes).
`VerboseAction(cmd, msg)` prints `msg` normally and the full command with `-v`.

## env.Command: run as a build step with dependencies
Regenerates only when inputs change, and SCons knows outputs:
```python
Import("env")
protos = env.Glob("$PROJECT_DIR/proto/*.proto")
gen = env.Command(
    target=["$PROJECT_DIR/src/gen/msgs.pb.c", "$PROJECT_DIR/src/gen/msgs.pb.h"],
    source=protos,
    action=env.VerboseAction(
        "python -m nanopb.generator.nanopb_generator -D $PROJECT_DIR/src/gen -I $PROJECT_DIR/proto $SOURCES",
        "nanopb $SOURCES"),
)
env.Depends("$BUILD_DIR/src/main.cpp.o", gen)    # ensure generation before compiling users
```
Caveat: PlatformIO collects `src/` files before such targets run, so first-time generated `.c`
files may be missed. Common fix: generate in a PRE script with `env.Execute` when outputs are
missing or older than inputs (compare mtimes), and use `env.Command` only for non-source artefacts.

## Running tools after build
Use `env.AddPostAction("$BUILD_DIR/${PROGNAME}.elf", env.VerboseAction("...", "msg"))` (see post-build
actions) rather than `Execute`, so they run after linking and only when the ELF changes.

## Tools from packages
```python
tool = env.PioPlatform().get_package_dir("tool-openocd")
env.Execute(f'"{tool}/bin/openocd" --version')
```
Or `pio pkg exec -p <package> -- <cmd>` from the shell.

## Gotchas
- `env.Execute` runs on every invocation, including IDE indexing; guard with
  `if not env.IsIntegrationDump():` (documented in the scripting examples).
- Use `sys.executable` / `$PYTHONEXE` for Python tools so the PIO venv is used.
- Paths with spaces: quote in command strings or pass lists to `subprocess` instead.

## Verify
- [ ] Changing an input file regenerates outputs; unchanged inputs do not.
- [ ] A failing generator stops the build with a non-zero exit.
