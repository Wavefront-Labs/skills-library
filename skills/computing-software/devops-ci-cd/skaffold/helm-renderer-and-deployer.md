---
id: computing-software.devops-ci-cd.skaffold.helm-renderer-and-deployer
name: helm-renderer-and-deployer
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [helm, releases, setvaluetemplates, post-renderer]
level: advanced
status: docs-checked
description: "Use Helm with Skaffold: helm template for rendering, helm install for deploying, and wiring built images into chart values."
sources:
  - "https://skaffold.dev/docs/deployers/helm/"
  - "https://skaffold.dev/docs/environment/templating/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Skaffold has two Helm integrations: the renderer (`manifests.helm`) uses `helm template`, and the deployer (`deploy.helm`) uses `helm install`. The `helm` binary must be installed; Skaffold does not install it. For deploys Skaffold also uses its own binary as a Helm `--post-renderer`, mainly to inject the `run-id` label it uses for status checking and to swap a placeholder for the built image.

```yaml
build:
  artifacts:
  - image: my-registry/app
deploy:
  helm:
    releases:
    - name: my-release
      chartPath: charts/app
      setValueTemplates:
        image.repository: "{{.IMAGE_REPO_my_registry_app}}"
        image.tag: "{{.IMAGE_TAG_my_registry_app}}@{{.IMAGE_DIGEST_my_registry_app}}"
      setValues:
        replicaCount: 2
```

The artifact `image` must be set in `build.artifacts` and must match the name used in `setValueTemplates`.

Template variables per artifact: `IMAGE_FULLY_QUALIFIED_<name>`, `IMAGE_REPO_<name>`, `IMAGE_TAG_<name>`, `IMAGE_DIGEST_<name>`, `IMAGE_DOMAIN_<name>` and `IMAGE_REPO_NO_DOMAIN_<name>`.

In the artifact name used inside the template, the characters `/`, `-`, `.` and `:` must be written as `_`. So `my-registry/app` is written `my_registry_app`.

Image reference strategies: `fqn` (default; set one key to `{{.IMAGE_FULLY_QUALIFIED_<name>}}`), `helm` (separate `repository` and `tag` keys) and `helm+explicitRegistry` (separate `registry`, `repository` and `tag`, using `IMAGE_DOMAIN_` and `IMAGE_REPO_NO_DOMAIN_`).

`setValues` binds a Helm key to a literal value; `setValueTemplates` binds a key to a templated value from environment variables and Skaffold's generated values. `artifactOverrides` and `imageStrategy` are no longer needed with the latest schemas (Skaffold v2.0.0 onward).

Several release fields support templating, including `chartPath`, `name`, `namespace`, `repo`, `version`, `setValueTemplates` and `valuesFiles`. `skipBuildDependencies` controls whether chart dependencies are built with `helm dep build`; when false, `skaffold dev` does not watch the chart's `charts` subfolder, to avoid a build loop.

Keep the values Skaffold sets to a minimum: image coordinates and a few literals. When a chart value does not change after a rebuild, compare the rendered image field and check the variable name; a hyphen not converted to an underscore is the usual cause.

## Checked

2026-11-04. Read the whole Skaffold Helm page and the Templated Fields page. Confirmed render versus deploy commands, the post-renderer, variables, sanitising rule, strategies, `setValues` versus `setValueTemplates`, the artifactOverrides note and `skipBuildDependencies`. Removed: the unverified tip to use `skaffold render` to inspect chart output, and the claim that wrong names "leave the old image in place" (the page says nothing about that). Note: the page's strategy sections still mention `artifactOverrides` after saying it is no longer needed.
Method: documentation only; no commands were run.
