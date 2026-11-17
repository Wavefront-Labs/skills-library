---
id: computing-software.cloud-infrastructure-engineering.terraform.reading-provider-http-request-traces
name: reading-provider-http-request-traces
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, http-trace, api-request-logs, tf-log-provider, aws-provider, debug-logging]
level: practitioner
status: docs-checked
description: "Capture provider-only logs with TF_LOG_PROVIDER and TF_LOG_PATH, and tune AWS provider retries when API calls are throttled."
sources:
  - https://developer.hashicorp.com/terraform/internals/debugging
  - https://registry.terraform.io/providers/hashicorp/aws/latest/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading provider HTTP traces

## Capture
Terraform logs go to `stderr` when `TF_LOG` is set. Core and provider plugins can be logged separately:
```bash
export TF_LOG=TRACE TF_LOG_CORE=OFF TF_LOG_PROVIDER=DEBUG TF_LOG_PATH=./tf-provider.log
terraform plan
```
- Levels, in decreasing verbosity: `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`.
- `TF_LOG_CORE` and `TF_LOG_PROVIDER` take the same levels but only activate a subset of the logs.
- `TF_LOG_PATH` appends the log to a file, and the debugging page states that `TF_LOG` must still be set for any logging to be enabled.
- `TF_LOG=JSON` writes TRACE-level logs as JSON, but that format is not a stable interface and may change without warning.

Then open the log file and search it for the failing request, status code and any request ID the cloud API returns. What a provider writes for each HTTP call differs per provider and version, so read a sample of your own log first rather than relying on fixed line patterns.

## Throttling (AWS provider)
The AWS provider has a `max_retries` argument: the maximum number of times an API call is retried when AWS throttles requests or a transient failure occurs. It can also be set with the `AWS_MAX_ATTEMPTS` environment variable, and `retry_mode` (or `AWS_RETRY_MODE`) selects how retries are attempted. Terraform's own `-parallelism` flag limits concurrent operations.

## Secrets
Debug logs can contain request and response data. Treat the log file as sensitive, redact it before sharing it (the debugging page suggests attaching logs to bug reports), and delete it after the investigation.

## Verify
- [ ] The failing request, its status and any request ID are identified in the log.
- [ ] The log file is redacted or deleted after the investigation.

## Checked

Method: documentation only; no commands were run. Checked 2026-11-09 against the Terraform debugging page (TF_LOG levels, TF_LOG_CORE, TF_LOG_PROVIDER, TF_LOG_PATH requiring TF_LOG, JSON warning) and the AWS provider index docs (`max_retries`, `AWS_MAX_ATTEMPTS`, `retry_mode`, `AWS_RETRY_MODE`). Removed as not on those pages: the per-provider log line patterns and request ID header names (AWS, AzureRM, Google), the grep and awk commands, the status-code interpretation table (403, 429, 409, eventual consistency), and the claim that TRACE adds bodies for some providers. The AzureRM provider docs link was dropped from sources because nothing from it remains.
