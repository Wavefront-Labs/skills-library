---
id: computing-software.devops-ci-cd.nomad.job-run
name: job-run
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, job-run, run, submit-job, check-index, detach, preserve-counts, preserve-resources, eval-priority, var-file, exit-codes, cli]
level: practitioner
status: docs-checked
description: "Submit or update a Nomad job with nomad job run: monitor, exit codes 0 1 2, check-index, detach, preserve-counts, preserve-resources, var-file and ACLs."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/commands/job/run.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nomad job run

Alias: `nomad run`. Submits a new job or updates an existing one.

```
nomad job run [options] <job file>
```
`<job file>` is a path, `-` for stdin, or a URL (downloaded with go-getter). If the job file sets a region, it overrides `-region` and `$NOMAD_REGION`.

## Behaviour and exit codes
By default the command monitors the evaluation, placement and (for service jobs) the deployment until finished or failed; `batch` and `system` jobs create no deployments.
- `0` submitted and scheduled
- `2` placement problems (unsatisfiable constraints, resource exhaustion)
- `1` anything else, including deployment failure, connection or internal errors

## ACLs
Needs `submit-job` in the job's namespace. CSI volume mounts also need `csi-mount-volume` for the volume's namespace; host volumes need `host_volume` capability for that volume.

## Options
- `-check-index <n>` - register or update only if the server-side job modify index equals `n`. `0` means "only if the job does not exist"; non-zero ensures you update from a known state. Pairs with `nomad job plan` (`computing-software.devops-ci-cd.nomad.job-plan`). A mismatch prints `Enforcing job modify index ...: job exists with conflicting job modify index` and `Job not updated`.
- `-detach` - return immediately with an evaluation ID (inspect with `nomad eval status`).
- `-eval-priority` - override evaluation priority (default is the job's priority).
- `-preserve-counts` - keep existing group counts on update (so a manual or autoscaled count is not reset).
- `-preserve-resources` - keep existing task resources so autoscaling changes are not overwritten.
- `-output` - print the JSON that would be sent to the API without submitting.
- `-json`, `-hcl2-strict` (default true), `-var key=value`, `-var-file=<path>`, `-policy-override` (override soft mandatory Sentinel policies), `-vault-namespace`, `-consul-namespace` (Enterprise), `-verbose`, `-ui`.

## Tips
- Scripts that need to wait should use the monitor; pipelines that only submit should use `-detach` and check the evaluation.
- Deployment status in the monitor shows Desired/Placed/Healthy/Unhealthy and the Progress Deadline from the `update` block.

## Checked

2026-11-03. Confirmed against the commands/job/run page and commands/job/plan page (HashiCorp web-unified-docs, Nomad v1.10.x): parameters, defaults, option and flag names, exit codes and examples. Removed: nothing; no unsupported claim found.

Method: documentation only; no commands were run.
