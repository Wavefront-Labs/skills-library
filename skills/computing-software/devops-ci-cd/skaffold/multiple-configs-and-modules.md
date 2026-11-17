---
id: computing-software.devops-ci-cd.skaffold.multiple-configs-and-modules
name: multiple-configs-and-modules
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [modules, multi-config, metadata-name, requires]
level: practitioner
status: docs-checked
description: "Split a monorepo into named configs in one skaffold.yaml and select them with --module."
sources:
  - "https://skaffold.dev/docs/design/config/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A single `skaffold.yaml` can define several Skaffold configurations separated by `---`. Configurations that set `metadata.name` are considered `modules` and can be activated by name.

```yaml
apiVersion: skaffold/v4beta14
kind: Config
metadata:
  name: cfg1
build:
  artifacts:
  - image: app1
---
apiVersion: skaffold/v4beta14
kind: Config
metadata:
  name: cfg2
requires:
- configs: [cfg1]
```

Running `skaffold dev` without a module flag executes actions from all the modules. `skaffold dev --module cfg1` activates only `cfg1` and skips independent modules.

`--module <name>` filters to the target but also includes the transitive closure of its dependency graph. The page's example: if `cfg1` imports `cfg2`, and `cfg2` imports `cfg3` and `cfg4`, then `--module cfg1` activates all four and runs them in dependency order. In the example above, selecting `cfg2` therefore also activates `cfg1`.

On ordering, the page says artifacts in a required config are built before those in the current config (provided the artifacts have dependencies defined), and deploys in required configs are applied before those in the current config.

`requires` can import configs by name, from another file with `path`, from git or from Google Cloud Storage; see the config dependency skill for details.

## Checked

2026-11-04. Read the whole Skaffold Pipeline page (multiple configuration, dependencies and profile propagation sections). Confirmed module definition, the `--module` behaviour and closure example, and the ordering rule including its proviso. Removed: the claim that unnamed configs cannot be addressed by `--module` (implied only), the team workflow suggestion, and the `skaffold diagnose --yaml-only --module` tip (not on the page).
Method: documentation only; no commands were run.
