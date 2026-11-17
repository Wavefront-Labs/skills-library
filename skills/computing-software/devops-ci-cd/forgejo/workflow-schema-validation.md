---
id: computing-software.devops-ci-cd.forgejo.workflow-schema-validation
name: workflow-schema-validation
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [schema-validation, forgejo-runner-validate, validate-repository, pre-commit]
level: practitioner
status: docs-checked
description: "Find and prevent workflow schema errors using the UI, runner logs, forgejo-runner validate and a pre-commit hook."
sources:
  - https://forgejo.org/docs/latest/user/actions/troubleshooting/
  - https://forgejo.org/docs/latest/user/actions/advanced-features/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since Forgejo Runner v8.0.0, workflows and actions are validated against a schema and fail to run if they do not pass. Where errors show:

- When browsing a workflow in the web interface (Forgejo v13.0.0 and above).
- In the Actions list, by hovering the warning sign beside a failing workflow (v13.0.0 and above).
- In the logs of a run, in the Set up job step, for an action used by the workflow (all versions).
- In the Complete job step for an action used by an action, two levels of indirection (all versions).

Validate from the CLI with Forgejo Runner v9.0.0 and above: `forgejo-runner validate --repository https://example.com/my/repo`.

To automate it, the advanced features page provides a pre-commit hook. In `.pre-commit-config.yaml`:

```
repos:
  - repo: https://code.forgejo.org/forgejo/runner
    rev: v11.1.1
    hooks:
      - id: forgejo-runner-validate
```

If the logs shown in the web UI are incomplete, look at the Forgejo Runner's own logs.

## Checked

Date: 2026-11-07
Confirmed against the "Forgejo Actions | Troubleshooting" page (read in full): schema validation since Forgejo Runner v8.0.0, the four places errors show with their version gates, `forgejo-runner validate --repository` from Forgejo Runner v9.0.0, and the runner-logs advice. The `.pre-commit-config.yaml` snippet (repo, `rev: v11.1.1`, hook id `forgejo-runner-validate`) was confirmed on the "Forgejo Actions | Advanced features" page (pre-commit hook section; the rest of that page was also read), which is now listed in `sources`.
Corrected: added the advanced features page to `sources`; nothing else needed changing.
Method: documentation only; no commands were run.
