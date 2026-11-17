---
id: computing-software.cloud-infrastructure-engineering.ansible.workflows-as-code-nodes-failure-paths-and-inventory
name: workflows-as-code-nodes-failure-paths-and-inventory
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, workflow-templates, workflow-job-template-node, workflow-failure-path, workflow-inventory]
level: advanced
status: docs-checked
description: "Build workflow job templates as code with nodes and success/failure/always edges, design failure paths, and set workflow-level inventory and limit."
sources: ["https://raw.githubusercontent.com/ansible/awx/devel/awx_collection/plugins/modules/workflow_job_template.py", "https://raw.githubusercontent.com/ansible/awx/devel/docs/workflow.md", "https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/con-controller-workflow-scenarios.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Workflows as code

```yaml
- ansible.controller.workflow_job_template:
    name: Release app
    organization: Platform
    inventory: Production          # used by node templates that prompt for inventory
    limit: app
    ask_limit_on_launch: true
    workflow_nodes:
      - identifier: sync
        unified_job_template: {name: infra-ansible, type: project, organization: {name: Platform}}
        related:
          success_nodes: [{identifier: deploy}]
      - identifier: deploy
        unified_job_template: {name: Deploy app, type: job_template, organization: {name: Platform}}
        related:
          success_nodes: [{identifier: smoke}]
          failure_nodes: [{identifier: rollback}]
      - identifier: smoke
        unified_job_template: {name: Smoke tests, type: job_template, organization: {name: Platform}}
        related:
          failure_nodes: [{identifier: rollback}]
          always_nodes: [{identifier: notify}]
      - identifier: rollback
        unified_job_template: {name: Rollback app, type: job_template, organization: {name: Platform}}
        related:
          always_nodes: [{identifier: notify}]
      - identifier: notify
        unified_job_template: {name: Post release summary, type: job_template, organization: {name: Platform}}
```
The module takes `workflow_nodes` as a list; each node has an `identifier`, a `unified_job_template`
(name and type, with organization to look up job templates and projects) and a `related` block with
`success_nodes`, `failure_nodes`, `always_nodes` (lists of node identifiers) and credentials.
`identifier` must be unique within its workflow; it is copied to the workflow job nodes, and clients use it for idempotent updates.
Other node settings include `all_parents_must_converge`.

## Failure paths
- `failure_nodes` run when the parent fails; `always_nodes` run whether it succeeds or fails; `success_nodes` only on success. Errored and cancelled jobs are treated as failures.
- A workflow job is marked failed if a spawned job fails and has no failure handler (a `failure` or `always` link). If a failure path exists, the workflow can finish successful even though a node failed. To keep a rolled-back release red, end the rollback path with a node that fails deliberately.
- A node with `all_parents_must_converge: true` runs only when all parents have met the criteria to reach it.

## Inventory and limit at workflow level
Workflow-level inventory applies to job templates with `ask_inventory_on_launch=true`; templates that do not prompt for inventory ignore it and use their own. If the workflow itself prompts for inventory, schedules and other callers can supply it.

## Gotchas
- A deleted template leaves the node with a null template, which is treated as failed and follows the failure path.
- Removing a template from a workflow reconnects its child nodes upstream with the same edge type (in the UI).

## Verify
- [ ] Launch the workflow in the UI or API and confirm the visualizer shows the expected edges and the failure path runs when the deploy fails.

## Checked

- Date: 2026-11-09. Sources: ansible/awx devel workflow_job_template.py and docs/workflow.md; ansible/aap-docs main (workflow scenarios).
- Confirmed: `workflow_nodes` structure with identifier, unified_job_template, related success/failure/always lists, all_parents_must_converge, workflow-level inventory/limit and their ask flags; failure-handler rules; error and cancel treated as failure; null template treated as failed; inventory prompt behaviour; upstream reconnection when a template is removed.
- Removed unconfirmed claims: workflow-level `limit` overriding node templates (module only documents the field), retry-by-second-instance and `until` retry advice, project syncs adding minutes, the `awx workflow_job_templates launch` CLI verification, "manage both in the same CaC repo" (kept only as general caution omitted).

Method: documentation and collection source read from cloned repositories; no commands were run against a controller.
