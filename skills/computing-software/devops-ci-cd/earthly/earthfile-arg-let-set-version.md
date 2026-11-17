---
id: computing-software.devops-ci-cd.earthly.earthfile-arg-let-set-version
name: earthfile-arg-let-set-version
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, earthfile, arg, let, set, version, project, required, global]
level: practitioner
status: docs-checked
description: "Declare Earthfile ARG (--required, --global, dynamic form), LET and SET variables, and the VERSION and PROJECT commands that open an Earthfile."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthfile/earthfile.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ARG, LET, SET, VERSION, PROJECT

## VERSION and PROJECT
`VERSION [options...] <version-number>` must be the first command of an Earthfile (mandatory since Earthly 0.7). It selects the feature set; different versions can be mixed across Earthfiles in one project. Feature flags (e.g. `VERSION --try 0.8`) opt in to experimental features and give up compatibility guarantees, so avoid them in critical workflows.

`PROJECT <org-name>/<project-name>` ties the Earthfile to an Earthly Cloud project (for cloud secrets and build logs). It is only allowed in the base recipe, applies to the whole Earthfile and cannot contain args that need expanding.

## ARG
- Constant form: `ARG [--required] <name>[=<default-value>]`; no default means empty string.
- Dynamic form: `ARG [--required] <name>=$(<default-value-expr>)`, evaluated at run time with `/bin/sh -c` in the build environment.

Scope is the current target or function recipe, from the declaration onward. Override from the CLI with `earthly <target-ref> --<name>=<override-value>` or from another target:
```Dockerfile
BUILD +binary --NAME=john
COPY (+binary/bin --NAME=john) ./
FROM +docker-image --NAME=john
```
- `--required`: value must be supplied and can have no default (`ARG --required NAME`), avoiding an accidental `""`.
- `--global`: visible to all targets in the Earthfile; only allowed in base targets. Avoid it for fast-changing values (git sha, branch, PR number) since any change re-executes all targets without cache. Declare args as deep and late as possible.

## LET and SET
`LET <name>=<value>` declares a variable that cannot be overridden; it may shadow an `ARG`. `SET <name>=<value>` changes a variable declared with `LET`; it cannot change an `ARG`. To change an arg, first redeclare it with `LET someVar = "$someVar"`.
```Dockerfile
ARG --global mode = dev
foo:
    LET buildArgs = --mode development
    IF [ "$mode" = "prod" ]
        SET buildArgs = --mode production --optimize
    END
```

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: earthfile/earthfile.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
