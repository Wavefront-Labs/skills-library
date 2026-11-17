---
id: computing-software.cloud-infrastructure-engineering.terraform.memory-exhaustion-on-large-terraform-plans
name: memory-exhaustion-on-large-terraform-plans
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, out-of-memory, memory-usage, oom-killed, large-state-performance, graph-size, ci-runner-memory]
level: practitioner
status: docs-checked
description: "Diagnose and fix Terraform running out of memory on large plans: measuring peak RSS, provider vs core memory, huge states and expressions, parallelism and runner sizing."
sources:
  - https://developer.hashicorp.com/terraform/internals/debugging
  - https://developer.hashicorp.com/terraform/cloud-docs/agents/requirements
  - https://developer.hashicorp.com/terraform/cli/commands/plan
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Memory exhaustion on large plans

Symptoms: CI job killed (exit 137 is the usual shell code for SIGKILL), a Go `out of memory` crash, or a provider plugin that dies mid-run (often OOM-killed, which the OS log shows).

## Measure
```bash
/usr/bin/time -v terraform plan -lock=false -out=tfplan   # look at "Maximum resident set size"
dmesg -T                                                   # look for OOM-killer lines: terraform or terraform-provider-* ?
ps -o pid,rss,cmd -C terraform                             # during the run; repeat for the provider process names
```
Terraform core and each provider plugin are separate processes, so total memory is core plus every provider instance (one per provider configuration or alias).

## Causes and fixes
| Cause | Fix |
|---|---|
| Many provider configurations (aliases per region/account) | split roots per account/region rather than configuring dozens of providers in one root |
| Very large state (tens of thousands of resources, big attributes) | split state; avoid storing large blobs inline |
| Huge expressions: `setproduct`/`flatten` over thousands of items, giant `jsondecode` inputs | precompute outside Terraform, reduce data loaded with `file()`/`templatefile()` |
| Large plan with many changes | plan smaller scopes |
| High `-parallelism` | `-parallelism=n` limits concurrent operations while walking the graph (default 10); lower it |
| Old Terraform/provider versions | upgrade; release notes of newer versions may include memory fixes |

## Runner sizing
- Self-hosted HCP Terraform agents: the agent requirements page gives at least 2 GB of system memory and 4 GB of free disk as a reference, and says to monitor and adjust memory, CPU and disk for the workspaces each agent serves (add roughly 250 MB if request forwarding is enabled).
- Containers: set the memory limit explicitly and leave headroom above the measured peak.

## Debug detail
Setting `TF_LOG` (levels TRACE, DEBUG, INFO, WARN, ERROR) writes detailed logs to stderr, and `TF_LOG_CORE` / `TF_LOG_PROVIDER` enable core or provider logging separately; measure memory by bisection: `-target` subsets or temporarily splitting providers to see what drives it.

## Verify
- [ ] Peak RSS recorded per large root; runners sized with headroom.
- [ ] Biggest offenders split or slimmed; plan runs without OOM over repeated runs.

## Checked
2026-11-01. Confirmed on the HashiCorp pages: the HCP Terraform agent requirements (2 GB memory, 4 GB disk, roughly 250 MB extra for request forwarding, monitor and adjust) the debugging page's `TF_LOG`, `TF_LOG_CORE` and `TF_LOG_PROVIDER` variables, and on the plan page `-out`, `-target`, `-lock=false` and `-parallelism` (default 10).
Removed: the exact error strings, a provider version/binary name, the GOMEMLIMIT recipe, the per-provider memory estimate and the 30% headroom figure, since no fetched page states them.
Method: documentation only; no commands were run.
