---
id: computing-software.cloud-infrastructure-engineering.portainer.portainer-app-templates-json-format
name: portainer-app-templates-json-format
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [app-templates, json, custom-templates, stacks]
level: practitioner
status: docs-checked
description: "Write custom Portainer app template JSON, including template types and required fields, and publish it by URL in Settings."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/advanced/app-templates/format.md
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/admin/settings/general.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Custom app templates are a JSON file that you host and reference by URL under Settings, App Templates (or via the `--templates` flag). The file is an object with `"version": "2"` and a `templates` array; each element is one template.

Key fields:

- `type` (integer, required): 1 container, 2 Swarm stack, 3 Compose stack. Type 3 is limited to the version 2 stack format, a docker/libcompose limitation.
- `title` (string, required).
- `description` (string, required).
- `image` (string, required for container templates): the Docker image.
- `administrator-only` (boolean, optional): true limits the template to admins.

Container templates also accept optional fields: `name`, `logo`, `registry`, `command`, `env`, `network`, `volumes`, `ports`, `labels`, `privileged`, `interactive`, `restart_policy`, `hostname`, `note`, `platform` and `categories`. Stack templates (types 2 and 3) use `repository` instead of `image`, plus `administrator_only`, `name`, `logo`, `env`, `note`, `platform` and `categories`. Note the stack format spells it `administrator_only` with an underscore, while the container format uses a hyphen.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Removed a padding sentence; clarified that `image` applies to container templates. Field names and required flags confirmed against the format page.

Method: documentation only; no commands were run.
