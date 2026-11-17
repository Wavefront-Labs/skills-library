---
id: computing-software.devops-ci-cd.concourse-ci.fly-resource-management-commands
name: fly-resource-management-commands
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [fly, check-resource, pin-resource, unpin-resource, disable-resource-version, clear-resource-cache]
level: practitioner
status: docs-checked
description: "Manage resources with fly: check-resource with --from, pin-resource with --comment, unpin, enable and disable versions as key-value pairs, and clear-resource-cache by version."
sources:
  - https://concourse-ci.org/docs/resources/managing-resources/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All take `-t example` and a `pipeline/resource` value.

- `fly check-resource --resource my-pipeline/my-resource` forces an immediate check. `--from ref:abcdef` checks from a particular version, inclusive, to collect versions older than the current ones, since a newly configured resource only starts from the latest. The `ref:` prefix is resource-dependent; the bosh-io-release resource might use `version:11.2`.
- `fly pin-resource --resource my-pipeline/my-resource --version ref:bceaf` pins a version. The version is a key-value pair: `ref:` for git, `digest:sha256:94be7d7b` for a registry resource. Add `--comment "Some reason"`, which shows in the UI. Use it to hold an external dependency that breaks in a new release, or to run with older inputs. The UI pin button generates a default comment with your username and a timestamp, which you can edit.
- `fly unpin-resource --resource my-pipeline/my-resource` removes the pin.
- `fly enable-resource-version` and `fly disable-resource-version` take `--resource` and `--version`, are idempotent, and have a check mark button equivalent in the UI.
- `fly clear-resource-cache -r my-pipeline/my-resource` invalidates all caches for that resource immediately; they are garbage collected asynchronously and later builds start with empty caches. `-v ref:abcdef` clears one version only.

Instanced pipelines use `--resource group/var1:value1/resource`.

## Checked

2026-11-04. Commands, flags and notes confirmed on the Managing Resources page; instanced form on the Grouping Pipelines page.

Method: documentation only; no commands were run.
