---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-workflow-labels
name: woodpecker-workflow-labels
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [labels, agent-selection, platform]
level: advanced
status: docs-checked
description: "Select Woodpecker agents for a workflow with labels and the platform label."
sources: ["https://woodpecker-ci.org/docs/usage/workflow-syntax", "https://woodpecker-ci.org/docs/administration/configuration/agent", "https://woodpecker-ci.org/docs/administration/configuration/server"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker workflow labels

An agent takes a workflow only if every label on the workflow matches the agent's labels. Add labels as a key-value map:

```yaml
labels:
  location: europe
  weather: sun
  hostname: ""

steps:
  - name: build
    image: golang
```

Only agents with `location=europe` or `location=*` match. A label with an empty value (like `hostname` above) is ignored.

Agents have at least four default labels: `platform=agent-os/agent-arch`, `hostname=my-agent`, `backend=docker` (the backend type) and `repo=*`. An `*` is a wildcard, so `repo=*` matches any repo. Extra agent labels come from `WOODPECKER_AGENT_LABELS`.

Every workflow carries `repo=your-user/your-repo-name`. Selecting a platform is done through a label in `GOOS/GOARCH` form:

```yaml
labels:
  platform: linux/arm64
```

Rules:

- Labels with the `woodpecker-ci.org` prefix are managed by Woodpecker and cannot be set in the pipeline.
- Administrators can additionally restrict agents with server-side agent filters, so a workflow may be skipped even when labels match.
- `WOODPECKER_DEFAULT_WORKFLOW_LABELS` supplies defaults for workflows without labels.

## Checked

2026-11-03. Confirmed against: workflow-syntax (labels, default agent labels, platform), agent configuration (WOODPECKER_AGENT_LABELS) and server configuration (WOODPECKER_DEFAULT_WORKFLOW_LABELS). Removed: nothing.

Method: documentation only; no commands were run.
