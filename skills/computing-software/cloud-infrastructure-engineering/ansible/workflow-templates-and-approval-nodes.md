---
id: computing-software.cloud-infrastructure-engineering.ansible.workflow-templates-and-approval-nodes
name: workflow-templates-and-approval-nodes
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, awx, automation-controller, workflow-templates, workflow, workflow-job-template, approval-nodes, workflow-approval, convergence, on-success, on-failure, always, nested-workflows, set-stats, workflow-artifacts, inventory-sync-node, project-sync-node, workflow-visualizer, release-pipeline, change-management]
level: advanced
status: docs-checked
description: "Chain jobs in AWX/controller workflows: success/failure/always edges, convergence, approval nodes with timeouts, passing data with set_stats artifacts, nesting."
sources: ["https://raw.githubusercontent.com/ansible/awx/devel/docs/workflow.md", "https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/con-controller-workflow-scenarios.adoc", "https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/ref-controller-workflows-extra-variables.adoc", "https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/con-controller-overview-workflow-enhancements.adoc", "https://raw.githubusercontent.com/ansible/awx/devel/awx_collection/plugins/modules/workflow_job_template.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workflow templates and approval nodes

**Goal:** a release is one button: sync inventory, deploy to stage, test, human approval,
deploy to prod, notify; with failures routed to rollback and data passed between steps.

## 1. Anatomy
A workflow is a graph of nodes; each node is a job template, project update, inventory update,
approval, or another workflow job template. Edges from a node: `success_nodes`, `failure_nodes`,
`always_nodes`. The graph must be acyclic (cycles are rejected with a 400-level response). Each node
has an `identifier`, unique within its workflow, that makes create/update idempotent; if you omit
it the server assigns a random UUID4.

Convergence: a node with several parents runs when any parent satisfies its edge, or, with
`all_parents_must_converge: true`, only when all parents have met the criteria.
Root nodes are always "ALWAYS" and cannot be edited.

Workflow-level launch settings: `extra_vars` (can have a survey), `inventory`, `limit`, `scm_branch`.
Nodes can carry their own launch configuration for the job they spawn. If both the workflow job
and the node specify the same prompt, the workflow job's value wins; if the node's job template
does not allow that prompt (for example `ask_inventory_on_launch` is false), the prompt is ignored
and the template default is used. Job templates with `ask_inventory_on_launch=true` use the
workflow-level inventory; others use their own.

```
[sync inventory] -success-> [deploy stage] -success-> [smoke test] -success-> [APPROVAL] -success-> [deploy prod]
                                 |-failure-> [notify + rollback]               |-failure (denied/timeout)-> [notify denied]
```

## 2. Approval nodes
An approval node pauses the workflow until someone with permission gives a yes or no. Timeout
defaults to 0, meaning no expiration; in the collection's node `timeout` is in seconds. Who can
approve: superusers, workflow admins, organization admins, and users explicitly given the approver
role. Viewing approvals needs read access to the workflow job template. Approval events appear in
the activity stream. Treat a deny or timeout as the failure path.

## 3. Passing data between nodes
Playbooks publish values with `set_stats`; they become `artifacts` on the job and flow to
descendant nodes as extra variables.
```yaml
- ansible.builtin.set_stats:
    data: {release_build: "{{ build_id }}"}
```
Keep the default `per_host: false` or artifacts will not work. Artifacts accumulate along a branch
and a child overrides a parent's value of the same name. At a convergence node `set_stats` data is
merged in an undefined way, so use unique keys. Workflow extra vars are combined with each job
template's variables and take precedence over them (the three extra levels in the precedence list
are workflow template extra vars, workflow survey defaults and workflow launch extra vars).

## 4. Patterns
- Put project and inventory sync nodes first.
- One workflow plus a prompted (or workflow-level) inventory lets you reuse it across environments.
- Nest workflows to reuse sub-pipelines; artifacts from the sub-workflow pass downstream, and recursion is detected and the child marked failed.
- Nodes that fail with no failure or always link make the whole workflow fail; a node failure that has a failure/always handler does not fail the workflow.

## Gotchas
- Cancelled or errored spawned jobs are treated like failures for path selection.
- Deleting a spawned job while its workflow runs is blocked.
- Do not `set_stats` secrets.
- Simultaneous workflow runs (`allow_simultaneous`) are off by default.

## Verify
- [ ] Trigger the workflow: stage deploys, the approval appears for approvers, denying it takes the failure path.
- [ ] A `set_stats` value from node 1 is visible as an extra var in a later node.
- [ ] The visualizer shows the intended edges.

## Checked

- Date: 2026-11-09. Sources: ansible/awx devel docs/workflow.md and awx_collection workflow_job_template.py; ansible/aap-docs main (workflow scenarios, workflow extra variables, workflow enhancements).
- Confirmed: node types, edge types, DAG rule, identifier semantics, all_parents_must_converge, launch configuration fields and prompt precedence, inventory prompt behaviour, approval roles, timeout default 0 and seconds in the module, artifacts and `per_host`, undefined merge at convergence, nesting and recursion handling, failure-handler rules.
- Removed unconfirmed claims: `aggregate: true` on set_stats, relaunch re-running from the start with no resume, labels/webhook/concurrent-jobs workflow settings, the `infra.aap_configuration` example, "artifacts override workflow extra vars" precedence stated as absolute, prompted fields frozen at save time, sliced-template and approval incompatibility, schedule queueing behind a pending approval, notification-template attachment to approvals, the `/workflow_approvals/<id>/approve/` endpoint.

Method: documentation and collection source read from cloned repositories; no commands were run against a controller.
