---
id: computing-software.firmware-embedded-development.esphome.esphome-external-components
name: esphome-external-components
category: computing-software
field: firmware-embedded-development
product: esphome
tags: [esphome, external-components, git-components, local-components, refresh, github, custom-components]
level: advanced
status: docs-checked
description: "Pull community or local components into ESPHome with external_components: git and local sources, the components filter, ref, refresh interval and credentials."
sources: ["https://esphome.io/components/external_components/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Esphome external components

`external_components` imports community or personal components and can override bundled ones. Writing your own components is covered on the separate developer site.

Per entry:
- `source` with `type`: `local` or `git`.
- git: `url` (required), `ref` (branch or tag; default branch if omitted), `username`, `password`, `path` (when the code is not in `components` or `esphome/components`).
- local: `path` (required); relative paths resolve against the folder holding your YAML, so `my_components` is found beside the config.
- `components`: list to load from that source (all by default).
- `refresh`: how often git sources are checked for updates, default `1day`; no effect for local.

Git layout: source components live in a `components` folder or an `esphome/components` folder, the latter making it easy to share from a forked ESPHome repository. URLs can be remote (`http:` or `https:`) or local (`file:` with an absolute path). A shorthand `github://` form exists, including one for pull requests on the ESPHome repository.

During validation ESPHome clones the repository into the hidden `.esphome` folder and loads components from that copy. The clone path depends on repository and ref name, so different refs are updated independently. After the `refresh` time passes, the repository is checked with a git pull.

Credentials: use `username` and `password` with `!secret`; they are not a comprehensive security measure because they are stored in clear text inside the `.esphome` directory.

## Checked

2026-11-04. Prose, option names, defaults and ranges were compared with https://esphome.io/components/external_components/ (fetched this batch). Nothing needed removing.

Method: documentation only; no commands were run.
