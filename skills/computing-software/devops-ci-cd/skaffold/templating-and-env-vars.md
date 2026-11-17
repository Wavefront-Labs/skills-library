---
id: computing-software.devops-ci-cd.skaffold.templating-and-env-vars
name: templating-and-env-vars
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [templating, go-template, sprig, env, skaffold-env]
level: practitioner
status: docs-checked
description: "Use Go template expressions and environment variables in selected skaffold.yaml fields, and inspect the result."
sources:
  - "https://skaffold.dev/docs/environment/templating/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Skaffold uses Go `text/template` plus Sprig functions, and environment variables are available as `{{.NAME}}`.

```yaml
build:
  artifacts:
  - image: app
    docker:
      buildArgs:
        VERSION: "{{.VERSION}}"
  tagPolicy:
    envTemplate:
      template: "{{.IMAGE_NAME}}:{{.VERSION}}"
deploy:
  kubectl:
    defaultNamespace: "{{.NS}}"
```

Fields that support templating include `docker.buildArgs`, `ko.env`, `ko.flags`, `ko.labels`, `ko.ldflags`, `envTemplate.template`, Helm release fields (`chartPath`, `name`, `namespace`, `repo`, `setValueTemplates`, `version`, `valuesFiles`), `kubectl.defaultNamespace`, `kustomize.defaultNamespace`, and `portForward` `namespace` and `resourceName`. The docs say this list is not exhaustive.

Available variables: all environment variables passed to the Skaffold process at startup, plus `IMAGE_NAME` for the `envTemplate` tagger. Helm deployments also get `IMAGE_NAME`, `IMAGE_TAG`, `IMAGE_DIGEST`, `IMAGE_DOMAIN` and `IMAGE_REPO_NO_DOMAIN` for the first declared artifact, `IMAGE_NAME_<artifact-name>`-style variables per named artifact (with `/` and `-` changed to `_`), and numbered forms such as `IMAGE_TAG2`. Skaffold also adds a `cmd` template function that runs an external command, which combines with Sprig functions in pipelines.

Variables can come from the shell or from a `skaffold.env` file in the project root (`KEY=value` lines, never overriding existing variables). Flags can be set there too with the `SKAFFOLD_` prefix, such as `SKAFFOLD_NAMESPACE=mynamespace`; a command line flag wins over the file.

Render supported templated fields to inspect the result with:

```bash
skaffold diagnose --enable-templating
```

## Checked

2026-11-09: confirmed against the Skaffold docs pages "Templated Fields" and "Load environment variables from a file" (source docs-v2/content/en/docs/environment/templating.md and env-file.md) and the CLI reference (`skaffold diagnose --enable-templating`). Removed the claim that other fields are not templated (the docs say the list is not exhaustive) and unverified YAML quoting and secrets advice.

Method: docs-checked 2026-11-09 against skaffold.dev templating and env-file pages and CLI reference (read as source markdown).
