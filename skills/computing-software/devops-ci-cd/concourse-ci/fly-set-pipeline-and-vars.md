---
id: computing-software.devops-ci-cd.concourse-ci.fly-set-pipeline-and-vars
name: fly-set-pipeline-and-vars
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [fly, set-pipeline, validate-pipeline, format-pipeline, vars, load-vars-from, check-creds]
level: practitioner
status: docs-checked
description: "Set a pipeline with fly: --config, stdin, static --var and --load-vars-from values, nested fields, --check-creds, plus validate-pipeline --strict and format-pipeline --write."
sources:
  - https://concourse-ci.org/docs/pipelines/setting-pipelines/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`fly -t example set-pipeline --pipeline my-pipeline --config pipeline.yml` shows a diff and asks for confirmation. Passing `--config -` reads stdin, and that disables the confirmation prompt, so the pipeline is set automatically.

Vars in the YAML such as `private_key: ((private-repo-key))` can be filled statically so credentials stay out of the file:

```shell
fly -t example set-pipeline --pipeline my-pipeline --config pipeline.yml \
    --var "private-repo-key=$(cat id_rsa)"
fly -t example set-pipeline --pipeline my-pipeline --config pipeline.yml \
    --load-vars-from vars.yml
```

Nested fields work too: `((repo.uri))` and `(("github.com".private-repo-key))` can be provided by a nested `vars.yml` or by flags such as `--var "repo.uri=github.com"` and `--var "\"github.com\".private-repo-key=$(cat id_rsa)"`.

Vars you do not provide stay unresolved and are looked up at runtime. Add `--check-creds` to fill in the static ones and then try to resolve the rest server-side; if any fail to resolve, setting the pipeline fails.

Two local helpers:
- `fly validate-pipeline --config pipeline.yml` validates without submitting. Errors fail the command, warnings do not; `--strict` fails on both.
- `fly format-pipeline --config pipeline.yml` prints a canonical form (keys in normal order, `name` first). `--write` or `-w` updates the file in place.

## Checked

2026-11-04. Commands, flags and examples confirmed on the Setting Pipelines page.

Method: documentation only; no commands were run.
