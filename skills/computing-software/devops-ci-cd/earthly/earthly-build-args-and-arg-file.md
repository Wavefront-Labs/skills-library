---
id: computing-software.devops-ci-cd.earthly.earthly-build-args-and-arg-file
name: earthly-build-args-and-arg-file
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, build-arg, arg-file, env-file, earthly-build-args, dotenv]
level: practitioner
status: docs-checked
description: "Pass build args to earthly targets in target, artifact and image forms, and store local settings in an .arg or .env file in the directory earthly runs from."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthly-command/earthly-command.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Passing build args and using .arg / .env files

Goal: override `ARG` values from the command line or from files.

## Command line
Overrides are `--<build-arg-key>=<build-arg-value>`, given after the target reference:
```
earthly +some-target --NAME=john --SPECIES=human
earthly --artifact +some-target/some-artifact ./dest/path --NAME=john --SPECIES=human
```
Image form takes them the same way: `earthly --image <target-ref> --<key>=<value>`.
Env var form: `EARTHLY_BUILD_ARGS="<build-arg-key>=<build-arg-value>,<build-arg-key>=<build-arg-value>,..."`.

The deprecated flag `--build-arg <key>[=<value>]` still exists; if `<value>` is omitted it takes the value of the environment variable of the same name. Prefer the `--<key>=<value>` syntax.

## Scope
Overrides apply only to the target called directly and other targets referenced from the same Earthfile. They do not apply to targets referenced from other directories or repositories.

## .arg file
A `.arg` file in the directory where `earthly` is executed (not necessarily where the Earthfile is):
```
# an example build arg
MY_SETTING=a setting which contains spaces
```
One variable per line, no surrounding quotes (quotes would become part of the value), `#` lines are comments, blank lines allowed.

## .env file
Flag options can also be set via env vars, and those can be put in an `.env` file with the same syntax:
```
EARTHLY_ALLOW_PRIVILEGED=true
EARTHLY_VERBOSE=true
```

## Gotcha
Keep `.arg` contents minimal: they are for settings specific to the local environment and can make builds inconsistent across systems and hard to reproduce.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: earthly-command/earthly-command.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
