---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-status-filter
name: woodpecker-status-filter
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [status, notifications, on-failure]
level: practitioner
status: docs-checked
description: "Run Woodpecker steps on failure or regardless of outcome with the status filter."
sources: ["https://woodpecker-ci.org/docs/usage/workflow-syntax", "https://woodpecker-ci.org/docs/usage/workflows"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker status filter

By default a step runs only when the workflow has succeeded so far, equivalent to `status: [success]`. The `status` filter overrides that. The only accepted values are `success` and `failure`.

Run a notification step whatever the outcome:

```yaml
steps:
  - name: notify
    image: alpine
    when:
      - status: [success, failure]
```

The filter is aware of other filters in the same entry. This runs on failure for tags, and on success or failure for pull requests:

```yaml
when:
  - event: tag
    status: [failure]
  - event: pull_request
    status: [success, failure]
```

If no entry matches, or all matching entries leave `status` unset, the default applies and the step runs on success only. In the example above that happens for any event other than `tag` or `pull_request`.

The same filter works at workflow level. A workflow that must run even if its dependencies failed should set `when: - status: [success, failure]`, otherwise it waits for all `depends_on` entries to finish successfully.

Steps that only post notifications often need no source code; combine them with `skip_clone: true`.

## Checked

2026-11-03. Confirmed against: workflow-syntax (status) and workflows (workflow-level status, skip_clone). Removed: nothing.

Method: documentation only; no commands were run.
