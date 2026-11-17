---
id: computing-software.devops-ci-cd.argo-workflows.workflow-restrictions
name: workflow-restrictions
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [workflow-restrictions, template-referencing, strict-mode, user-override-allowlist, secure-mode]
level: advanced
status: docs-checked
description: "Force Workflows to use WorkflowTemplates with templateReferencing Strict or Secure, the allowed override fields and WORKFLOW_USER_OVERRIDE_ALLOWLIST."
sources: ["https://argo-workflows.readthedocs.io/en/latest/workflow-restrictions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workflow restrictions
Administrators can limit what users run via `workflowRestrictions` in `workflow-controller-configmap`:

```yaml
data:
  workflowRestrictions: |
    templateReferencing: Strict
```

- `Strict`: only Workflows that use `workflowTemplateRef` are processed, so arbitrary Workflows are disallowed.
- `Secure`: Strict, plus the referenced WorkflowTemplate must not change between operations; if it changes under a running Workflow, that Workflow errors out.

Under either mode the submitted Workflow may set only allow-listed fields on top of the template: `arguments`, `entrypoint`, `shutdown`, `suspend`, `activeDeadlineSeconds`, `priority`, `ttlStrategy`, `podGC`, `volumeClaimGC`, `archiveLogs`, `workflowMetadata`, `workflowTemplateRef`, `metrics`, `artifactGC`. Anything else (for example `serviceAccountName`, `securityContext`, `volumes`, `hostNetwork`, `podSpecPatch`, extra `templates`) makes the Workflow error, so these sensitive settings must live in the WorkflowTemplate.

Extend the list with the controller environment variable `WORKFLOW_USER_OVERRIDE_ALLOWLIST`, a comma-separated list of `WorkflowSpec` field names in YAML/JSON form, e.g. `podSpecPatch,volumes`. An unknown name fails controller startup, surfacing typos. The nested `artifactGC.podSpecPatch`, `artifactGC.serviceAccountName` and `artifactGC.podMetadata` stay blocked regardless.

Page rationale: the restriction stops submitters overriding security-sensitive fields defined in the template. Put those fields in the WorkflowTemplate, and let submitters supply only the allow-listed ones.

## Checked

2026-11-08. Read the Argo Workflows workflow restrictions page in full (raw markdown) and confirmed Strict and Secure modes, the allow-listed fields, WORKFLOW_USER_OVERRIDE_ALLOWLIST behaviour, blocked nested artifactGC fields, and the configmap example. Nothing removed.

Method: documentation only; no commands were run.
