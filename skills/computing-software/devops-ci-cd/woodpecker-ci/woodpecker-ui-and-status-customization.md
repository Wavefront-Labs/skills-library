---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-ui-and-status-customization
name: woodpecker-ui-and-status-customization
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [custom-css, status-context, white-labeling]
level: advanced
status: docs-checked
description: "Customize the Woodpecker UI with CSS and JS files and change forge status check names."
sources: ["https://woodpecker-ci.org/docs/administration/configuration/server"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker UI and status context customization

UI customization: point the server at files on its filesystem (baked into the image or mounted from a ConfigMap on Kubernetes). They must be UTF-8 and are independent; either or both can be set.

```ini
WOODPECKER_CUSTOM_CSS_FILE=/usr/local/www/woodpecker.css
WOODPECKER_CUSTOM_JS_FILE=/usr/local/www/woodpecker.js
```

Typical uses are banner messages, logos or environment hints (white-labeling).

Status names on the forge: `WOODPECKER_STATUS_CONTEXT` (default `ci/woodpecker`) is the prefix of statuses published to the forge. Change it if several Woodpecker instances build one repository. `WOODPECKER_STATUS_CONTEXT_FORMAT` is a Go template, default:

```text
{{ .context }}/{{ .event }}/{{ .workflow }}{{if not (eq .axis_id 0)}}/{{.axis_id}}{{end}}
```

Supported variables: `context`, `event`, `workflow`, `owner`, `repo`.

Bitbucket build keys are limited to 40 characters. If a job exceeds that, shorten the key by changing these two variables.

Other server toggles: `WOODPECKER_ENABLE_SWAGGER` (default true) serves the Swagger UI for the API, and `WOODPECKER_DISABLE_VERSION_CHECK` hides the version check in the admin UI.

## Checked

2026-11-03. Read the Woodpecker server configuration page and confirmed the UI and status customization variables and defaults. Nothing removed. 

Method: documentation only; no commands were run.
