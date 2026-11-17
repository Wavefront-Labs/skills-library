---
id: computing-software.devops-ci-cd.concourse-ci.static-vars-flags-and-validate-output
name: static-vars-flags-and-validate-output
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [vars, static-vars, var-flags, yaml-var, load-vars-from, validate-pipeline, instance-var]
level: practitioner
status: docs-checked
description: "Supply var values statically with -v, -y, -i and -l on fly set-pipeline and execute, understand precedence, and preview the rendered result with fly validate-pipeline --output."
sources:
  - https://concourse-ci.org/docs/vars/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Static values can be set by the `set_pipeline` and `task` steps (`vars`) and, on the CLI, by `fly set-pipeline` and `fly execute`:

- `-v` / `--var NAME=VALUE` sets a string.
- `-y` / `--yaml-var NAME=VALUE` parses VALUE as YAML.
- `-i` / `--instance-var NAME=VALUE` parses VALUE as YAML and sets an instance var.
- `-l` / `--load-vars-from FILE` loads a YAML mapping of names to values.

With `-l`, the `-y` and `-v` flags take precedence, so a vars file can be reused with a few hand-set overrides.

The distinction between `-v` and `-y` matters: in `get: examples` with `trigger: ((trigger))`, you need `-y trigger=true` so the field is the boolean `true` rather than the string `"true"`.

To test interpolation without submitting, `fly validate-pipeline` takes the same flags plus `--output`, printing the rendered pipeline:

```shell
fly validate-pipeline \
  -c pipeline.yml \
  -l vars.yml \
  -y trigger=true \
  -v branch=master \
  --output
```

A quoted dotted name is passed like `-v \"github.com\".private_key="$(cat private_key)"`, matching `(("github.com".private_key))` in the template.

Task step `vars` allow running one task file against several versions: `vars: { tag: 1.13 }` fills `tag: ((tag))` in an `image_resource`.

## Checked

Checked 2026-11-09 against the raw docs source of the Vars page (read in full, Static vars section): flags, precedence and the validate-pipeline --output examples match.

Method: docs-checked 2026-11-09 against concourse docs vars page (github.com/concourse/docs source); documentation only, no commands were run.
