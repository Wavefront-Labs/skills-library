---
id: computing-software.software-engineering.wails.cli-init-and-remote-templates
name: cli-init-and-remote-templates
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, cli, templates, security]
level: practitioner
status: docs-checked
description: "Use wails init flags and remote GitHub templates safely, given that templates run frontend commands from wails.json on your machine."
sources: [https://wails.io/docs/reference/cli]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# wails init flags and remote templates

Goal: generate projects with the right options, and treat third-party templates as untrusted code.

## Method

`wails init` flags: `-n name` (mandatory), `-d dir` (default: project name), `-g` init git, `-l` list templates, `-q` quiet, `-t template` (default `vanilla`; a default template name or a GitHub URL), `-ide vscode|goland`, `-f` force build application.

Remote template: `wails init -n test -t https://github.com/leaanthony/testtemplate[@v1.0.0]` (optional version suffix). Community templates are listed in the community docs.

## Security
The Wails project does not maintain or take liability for third-party templates. `wails build` and `wails dev` run the `frontend:install`, `frontend:build`, `frontend:dev`, `frontend:dev:install`, `frontend:dev:build` and `frontend:dev:watcher` commands from wails.json without asking; package.json scripts also run. Using a remote template equals running its author's code with your permissions. Review `wails.json`, `package.json` and referenced scripts before the first build. `wails init` prints the commands found in wails.json when a remote template is used.

## Related skills
- computing-software.software-engineering.wails.init-project
- computing-software.software-engineering.wails.wails-json-config

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: CLI reference (reference/cli).

Corrected or removed: Spelled out -f as "force build application", the wording in the flag table.

Method: documentation only; no commands were run.
