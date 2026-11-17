---
id: computing-software.devops-ci-cd.backstage.techdocs-generator-config
name: techdocs-generator-config
category: computing-software
field: devops-ci-cd
product: backstage
tags: [techdocs-generator, run-in-docker, mkdocs-config, backstage]
level: advanced
status: docs-checked
description: "Configure how TechDocs generates sites using runIn, dockerImage, pullImage and MkDocs options."
sources:
  - https://backstage.io/docs/features/techdocs/configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

When the backend builds docs (`techdocs.builder: 'local'`), the generator settings sit under `techdocs.generator`.

```yaml
techdocs:
  builder: 'local'
  generator:
    runIn: 'docker'
    dockerImage: 'custom-registry/techdocs'
    pullImage: false
    mkdocs:
      omitTechdocsCorePlugin: false
      legacyCopyReadmeMdToIndexMd: false
      defaultPlugins: ['techdocs-core']
```

- `runIn` is `docker` or `local`. With `local`, MkDocs and `mkdocs-techdocs-core` must be installed where the backend runs, which avoids Docker-in-Docker.
- `dockerImage` picks the generator image, and `pullImage` controls whether it is pulled before each run. Registry credentials go under `pullOptions.authconfig`.
- `defaultEngine` selects the documentation engine.
- `mkdocs.disableExternalFonts` and `mkdocs.omitTechdocsCorePlugin` adjust the generated MkDocs config.
- `mkdocs.dangerouslyAllowAdditionalKeys` and `dangerouslyAllowAdditionalPlugins` list extra `mkdocs.yml` keys or plugins to permit. The names are a warning: they let repository authors influence what runs during the build.

Choose `local` when you run Backstage in your own custom Docker setup and want to avoid a Docker-in-Docker situation; otherwise the default is `docker`.

To skip Docker in a container image, install Python and run `pip3 install mkdocs-techdocs-core` (pin a version for reproducibility), then set `runIn: local`.

## Checked

2026-11-03. Confirmed on the TechDocs configuration page: `techdocs.generator.runIn` options `docker` and `local` and the Docker-in-Docker reason for `local`, `dockerImage`, `pullImage` (disable pulling the image), `pullOptions.authconfig` for private registries, `defaultEngine`, the `mkdocs` keys `omitTechdocsCorePlugin`, `legacyCopyReadmeMdToIndexMd`, `disableExternalFonts`, `defaultPlugins`, `dangerouslyAllowAdditionalKeys` and `dangerouslyAllowAdditionalPlugins`, and `pip3 install mkdocs-techdocs-core` from the how-to guides. Removed: the backend-restart sentence, which the page does not state; the docker versus local advice now follows the page.

Method: documentation only; no commands were run.
