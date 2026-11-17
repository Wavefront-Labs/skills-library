---
id: computing-software.cloud-infrastructure-engineering.knative.func-language-packs
name: func-language-packs
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [language-packs, func-repository, templates, func-tastic, runtimes]
level: advanced
status: docs-checked
description: "Extend func with extra runtimes and templates from Git repositories or locally installed language packs."
sources:
  - https://knative.dev/docs/functions/language-packs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add runtimes, function signatures and templates beyond the built-in ones.

Language packs extend Knative Functions to support additional runtimes, function signatures, operating systems and installed tooling. They are distributed through Git repositories or as a directory on the local file system. The upstream language pack contract documents their layout.

External Git repository: when creating a function you can name a repository as the template source. The Knative Extensions organization keeps example templates in a `func-tastic` repository. The page warns this repository is deprecated and will be archived.

```bash
func create myfunc -l nodejs -t metacontroller --repository https://github.com/knative-extensions/func-tastic
```

Install locally with the `func repository` command, giving the pack a name:

```bash
func repository add knative https://github.com/knative-extensions/func-tastic
```

After that, use the name as a prefix in the template argument:

```bash
func create -t knative/metacontroller -l nodejs my-controller-function
```

In these examples `-l nodejs` gives the runtime and `-t` names the template (`metacontroller`, or `knative/metacontroller` once the repository is added under the name `knative`). The function-creation page documents `-l`; for `-t` and `--repository`, see the func_create reference in the knative/func repository.

## Checked

2026-11-04. Confirmed against the Language packs page (knative/docs source): purpose of language packs, distribution through Git repositories or a local directory, the func-tastic deprecation warning, the `func create ... --repository` example, `func repository add knative <url>` and the `knative/metacontroller` prefix example. The `-t` and `--repository` flags appear only in these examples; the func_create reference was not read, so the skill now says to consult it instead of stating what the flags mean. Nothing else removed.

Method: documentation only; no commands were run.
