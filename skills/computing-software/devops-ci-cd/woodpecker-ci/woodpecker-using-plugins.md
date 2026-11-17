---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-using-plugins
name: woodpecker-using-plugins
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [plugins, settings, plugin-index]
level: intro
status: docs-checked
description: "Use Woodpecker plugins as pre-defined steps configured with settings."
sources:
  - https://woodpecker-ci.org/docs/usage/plugins/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Using Woodpecker plugins

Plugins are pipeline steps that perform pre-defined tasks such as deploying code, publishing artifacts or sending notifications. They are configured with `settings` and pulled automatically from the container registry the agent is configured with.

```yaml
steps:
  - name: build
    image: golang
    commands:
      - go build
  - name: publish
    image: woodpeckerci/plugin-s3
    settings:
      bucket: my-bucket-name
      source: some-file-name
      target: /target/some-file
```

Isolation: plugins are ordinary steps sharing the workspace volume, so they can see your source tree. To limit them, the workspace base is always mounted at `/woodpecker` and the working directory is adjusted. You cannot combine a plugin with `commands` or `entrypoint`; that fails. Using `environment` is possible, but then the step is no longer treated as a plugin internally, so it cannot read plugin-filtered secrets and is not privileged without explicit configuration.

Find official plugins in the Woodpecker plugin index linked from the plugins page. Drone plugins are generally supported but may need adjustments.

## Checked

2026-11-08. Read the Woodpecker Plugins overview page (woodpecker-ci.org/docs/usage/plugins/overview) in full and confirmed the settings example, registry pulling, isolation rules and the Drone note. Removed the plugin index URL (the page names the index without a path) and the credentials advice (not on that page).

Method: documentation only; no commands were run.
