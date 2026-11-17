---
id: computing-software.devops-ci-cd.backstage.techdocs-extensions-howto
name: techdocs-extensions-howto
category: computing-software
field: devops-ci-cd
product: backstage
tags: [techdocs-mermaid, plantuml, mkdocs-plugins, backstage]
level: advanced
status: docs-checked
description: "Add diagrams and plugins to TechDocs, including PlantUML, Mermaid options and extra MkDocs plugins."
sources:
  - https://backstage.io/docs/features/techdocs/how-to-guides
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The TechDocs how-to guides cover extending the build.

Other MkDocs plugins: install the plugin in the generator environment, then list it in `mkdocs.yml`. With CI generation, add the `pip install` step to the workflow. When the Backstage backend builds the docs, the plugin must exist in the generator image or local Python environment, and extra plugins can need to be permitted by `techdocs.generator.mkdocs.dangerouslyAllowAdditionalPlugins`.

```yaml
techdocs:
  generator:
    mkdocs:
      dangerouslyAllowAdditionalPlugins:
        - my-custom-plugin
```

Diagrams:

- PlantUML can be embedded in Markdown or referenced from a file.
- Mermaid support can come from Kroki, the `markdown-inline-mermaid` extension, or the `backstage-plugin-techdocs-addon-mermaid` addon.

Other guides in the same page:

- Enabling iframes, custom elements and extra URI protocols in the reader.
- Customising the TechDocs home and reader pages.
- Implementing your own TechDocs APIs.
- A hybrid build strategy, where some entities build locally and others externally.
- Adding documentation setup to software templates, so new projects start with `mkdocs.yml` and `docs/index.md`.
- Disabling external fonts, with `theme.font: false` in `mkdocs.yml`.

## Checked

2026-11-03. Confirmed on the TechDocs How-to guides page: guides for the TechDocs home page and APIs, enabling iframes, custom elements and extra URI protocols, PlantUML, Mermaid (Kroki, `markdown-inline-mermaid`, `addon-mermaid`), the hybrid build strategy, adding docs to software templates (`mkdocs.yml` and `docs/index.md`), and `theme.font: false` with `theme.name: material`. On the configuration page: `dangerouslyAllowAdditionalPlugins` and that plugins must be installed locally or in the Docker image. Removed: the trusted-hosts remark.

Method: documentation only; no commands were run.
