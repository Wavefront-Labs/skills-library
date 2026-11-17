---
id: computing-software.cloud-infrastructure-engineering.terraform.profiling-slow-terraform-plans
name: profiling-slow-terraform-plans
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, slow-plan, tf-log, plan-performance, log-timestamps, provider-timing, parallelism]
level: practitioner
status: docs-checked
description: "Find why a Terraform plan is slow using TF_LOG output: capture split core and provider logs, read timestamps, spot throttling, and fix the dominant cost."
sources:
  - https://developer.hashicorp.com/terraform/internals/debugging
  - https://developer.hashicorp.com/terraform/cli/config/environment-variables
  - https://developer.hashicorp.com/terraform/cli/commands/plan
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Profiling slow plans with log timestamps

## Capture
```bash
export TF_LOG=trace TF_LOG_PATH=plan-trace.log
time terraform plan -out=tfplan
```
- `TF_LOG` takes TRACE, DEBUG, INFO, WARN or ERROR (decreasing verbosity); `JSON` outputs TRACE and above in a parseable encoding. HashiCorp warns that the JSON encoding is not a stable interface and may change without warning, so do not build long-lived tooling on it.
- `TF_LOG_CORE` and `TF_LOG_PROVIDER` enable logging separately for Terraform itself and for provider plugins; they take the same levels.
- `TF_LOG_PATH` appends to a file, but logging only happens when `TF_LOG` (or the core/provider variables) is set. Unset `TF_LOG` or set it to `off` to stop.
- Logs appear on stderr unless a path is set.

## Split the time
Use the timestamps on each line to find large gaps and the phase they belong to: startup and config loading, refresh of resources, data source reads, and plan calculation. Count repeated provider calls by pattern with your own grep. Log line formats are not documented by HashiCorp, so inspect your own log before writing a parser (judgement).

## Fix the dominant cost
| Finding | Option |
|---|---|
| Refresh of very many resources | `-refresh=false` or `-minimal-refresh` trade accuracy for speed (see warnings in the plan docs); split roots only for a graph or blast-radius reason |
| Concurrency too low for the API | `-parallelism=n` (default 10); raise carefully |
| Throttling or retries in the log | lower `-parallelism`; ask for a quota increase (judgement) |
| Slow `init` or provider downloads | `plugin_cache_dir` / `TF_PLUGIN_CACHE_DIR` |
| Registry timeouts | `TF_REGISTRY_CLIENT_TIMEOUT` (default 10s) can be raised in exceptional circumstances |
| Remote backend writes during apply | `TF_STATE_PERSIST_INTERVAL` (minimum 20 seconds for remote backends) |

## Practical loop
1. Profile once with trace; find the dominant phase.
2. Fix the biggest cost; re-measure with `time terraform plan`.
3. Record plan duration per root (judgement).

Trace logs can contain secrets such as tokens and request bodies: do not upload them publicly without redaction.

## Verify
- [ ] The dominant phase is identified with numbers.
- [ ] After the fix, plan time is measured again and recorded.

## Checked
2026-11-09

Method: read the Terraform debugging, environment variables and plan command pages (fetched as text). Removed as unsupported by those pages: the specific grep and jq recipes over provider log lines, `PlanResourceChange` and other gRPC call names, `AWS_EC2_METADATA_DISABLED` and AWS retry-mode advice, and the AWS provider `max_retries` source (its provider page was not read).
