---
id: computing-software.devops-ci-cd.skaffold.skaffold-yaml-structure
name: skaffold-yaml-structure
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [skaffold-yaml, apiversion, config, schema]
level: intro
status: docs-checked
description: "The shape of a skaffold.yaml: apiVersion, kind, metadata, build, test, deploy, profiles and requires, plus path rules and modules."
sources:
  - "https://skaffold.dev/docs/design/config/"
  - "https://skaffold.dev/docs/references/cli/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A skaffold.yaml starts with an `apiVersion` and `kind: Config`. The docs page renders the current API version from a template, so look it up in the docs; `skaffold schema get <version>` prints the JSON schema for a version. Run `skaffold fix` to update an old file to a newer schema version.

```yaml
apiVersion: skaffold/v4beta7
kind: Config
metadata:
  name: my-app
build:
  artifacts:
  - image: app
    context: frontend
    docker:
      dockerfile: Dockerfile
deploy:
  helm:
    releases:
    - name: project
      chartPath: helm/project
      valuesFiles:
      - helm/project/dev-values.yaml
```

Components named on the docs page: `apiVersion`, `kind` (always `Config`), `metadata` (for example `name`), `build`, `test`, `deploy`, `profiles` (settings that override build, test and deploy when activated) and `requires` (other configs to import). The verify command's docs also show a top-level `verify` section.

File resolution rules from the docs:

- Paths in the file resolve relative to the current directory, not to the location of the config file.
- Files referenced from a build artifact resolve relative to that artifact's `context` directory (default: the current directory).
- Paths in an imported (required) config resolve relative to the directory of the imported file.
- The default file is `skaffold.yaml` in the current directory; override with `--filename`.

Print the effective configuration with `skaffold diagnose`; add `--yaml-only` (optionally with `--profile`) to print only the effective skaffold.yaml.

A file may hold several configs separated by `---`. Configs with a `metadata.name` are modules that you can activate by name with `--module`. `--module` also pulls in the transitive closure of the modules it requires.

Imports use `requires` with `configs` and `path`. Remote configs use `git` (`repo`, `path`, `ref`) or `googleCloudStorage` (`source`, `path`), cached under `~/.skaffold/remote-cache` unless `SKAFFOLD_REMOTE_CACHE_DIR` or `--remote-cache-dir` says otherwise. Profiles passed with `--profile` propagate to imported configs unless `--propagate-profiles=false`; `activeProfiles` with `name` and `activatedBy` gives finer control.

## Checked

2026-11-09: confirmed against the Skaffold docs page "Skaffold Pipeline" (source docs-v2/content/en/docs/design/config.md) and the CLI reference for `skaffold diagnose`, `fix` and `schema`. Removed the stated current API version (rendered by a template, not readable), the `manifests` and `portForward` sections, which that page does not mention, and the example using them.

Method: docs-checked 2026-11-09 against skaffold.dev design/config page and CLI reference (read as source markdown).
