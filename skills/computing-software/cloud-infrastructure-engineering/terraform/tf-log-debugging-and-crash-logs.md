---
id: computing-software.cloud-infrastructure-engineering.terraform.tf-log-debugging-and-crash-logs
name: tf-log-debugging-and-crash-logs
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, tf-log, debug-logging, crash-log, trace-logging, tf-log-path, tf-log-core, tf-log-provider, troubleshooting, provider-debugging, api-errors]
level: practitioner
status: docs-checked
description: "Turn on TF_LOG/TF_LOG_PROVIDER/TF_LOG_PATH at the right level, read provider API request logs, handle crash.log panics, and scrub logs before attaching them to a bug report."
sources: ["https://developer.hashicorp.com/terraform/internals/debugging", "https://developer.hashicorp.com/terraform/cli/config/environment-variables", "https://developer.hashicorp.com/terraform/plugin/log/managing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TF_LOG debugging and crash logs

**Goal:** when a plan/apply fails with an opaque error ("Error: error creating X:
InvalidParameter"), get the actual HTTP request/response the provider sent, or the
Go stack trace behind a panic, without flooding the terminal.

## 1. Environment variables
| Variable | Values | Effect |
|---|---|---|
| `TF_LOG` | `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`, `JSON` | all loggers (Terraform, SDKs, providers); overrides every other logging variable |
| `TF_LOG_CORE` | same | the Terraform binary only; does not include providers |
| `TF_LOG_PROVIDER` | same | all providers and provider SDKs; the one you usually want |
| `TF_LOG_PATH` | file path | write logs to a file (created if missing, appended if present) instead of stderr |
| `TF_LOG_PROVIDER_<NAME>` | same | one provider only, e.g. `TF_LOG_PROVIDER_AWS=DEBUG`; only providers that log with `tflog` |
| `TF_LOG_SDK` / `TF_LOG_SDK_PROTO` | same | provider SDKs and the plugin-go protocol layer; rarely needed |

`TF_LOG=JSON` outputs logs at the TRACE level in a parseable JSON encoding, which HashiCorp
does not treat as a stable interface. `TF_LOG_PROVIDER` overrides provider-specific variables
such as `TF_LOG_PROVIDER_AWS`. HashiCorp recommends `TF_LOG=TRACE` when reporting bugs. Before
v0.15.0, levels other than `TRACE` may not be reliable. Never write logs to stdout: the
plugin system uses it as a communication channel.

## 2. The useful recipe
```bash
TF_LOG_PROVIDER=DEBUG TF_LOG_PATH=./tf-debug.log terraform plan
grep -n "error" tf-debug.log | head -50
```
- `DEBUG` logs can include additional details about behaviour; whether API requests and
  responses appear depends on the provider, so check the provider's docs. That is where
  a more specific error message than the CLI summary often lives.
- `TRACE` is the most verbose level and typically includes low-level execution steps;
  expect large files on large states.
- Add `-parallelism=1` when hunting a single resource's failure; interleaved logs
  from 10 goroutines are hard to read.
- Narrow further with `-target` for the failing address (diagnostic use only).

## 3. Reading a provider log
Search for the resource's name or the failing attribute. Plain-text lines are prefixed
with a timestamp and the level in square brackets (`YYYY-MM-DDTHH:MM:SS.SSSZ [Level] Message`).
Where the provider logs requests, compare the request with what the console/CLI would send;
the mismatch is usually a value Terraform rendered differently than you expected (empty
string vs null, list order, JSON whitespace).

## 4. Crash logs
If Terraform or a provider panics, keep the full stack trace and the log. Do not trust
that state is unchanged: run `terraform state list` and `terraform plan` to confirm
before retrying. If the panic names a provider package, report it to that provider's
issue tracker; upgrading the provider or pinning the previous version are the usual workarounds.

## 5. Before you attach a log to an issue
Logs can contain tokens, account IDs, resource names, state values and sometimes
secrets passed as attributes. Scrub:
```bash
sed -E 's/(Authorization: )[^ ]+/\1<REDACTED>/; s/[0-9]{12}/<ACCOUNT>/g' tf-debug.log > tf-debug-clean.log
```
and read it once more yourself. `TF_LOG=JSON` output is easier to filter with `jq`, but its
format can change at any time.

## 6. Logs in CI
Set `TF_LOG_PATH` to an artifact path and `TF_LOG_PROVIDER=INFO` permanently; bump
to `DEBUG` by re-running with a pipeline variable. Avoid leaving `TRACE` on: it is the
most verbose level and fills artifact storage.

## Gotchas
- `TF_LOG` without `TF_LOG_PATH` dumps everything to stderr mixed with plan output.
- `TF_LOG_PROVIDER_<NAME>` does not affect logs written with legacy `log.Print*` functions;
  for remaining SDKv2 logs use `TF_LOG` or `TF_LOG_PROVIDER`.
- `TF_LOG` overrides all other logging variables, so setting it defeats per-provider filtering.
- Windows PowerShell: `$env:TF_LOG="DEBUG"; $env:TF_LOG_PATH="tf.log"; terraform plan`.

## Verify
- [ ] `TF_LOG_PROVIDER=DEBUG TF_LOG_PATH=x.log terraform plan` produces a log file with provider entries.
- [ ] After a crash, `terraform plan` runs clean before you retry apply.
- [ ] Any log you share has no tokens, account IDs or secret attribute values.

## Checked
- 2026-10-28. Confirmed against the Terraform "Enable Terraform logs" page and HashiCorp's "Managing Log Output" page (`TF_LOG` values and precedence, `JSON` at TRACE level and not stable, `TF_LOG_CORE`, `TF_LOG_PROVIDER`, `TF_LOG_PROVIDER_<NAME>`, `TF_LOG_PATH` create/append and stderr default, never write to stdout, v0.15.0 note, line format, TRACE recommendation for bug reports) and the CLI environment-variables page.
- Removed: the sample AWS log line, HTTP-request-logging claims for AWS/Azure/Google, `crash.log` file behaviour and message text, "hundreds of MB", SDK redaction claim, the init and backend logging claim, HCP remote-run advice and the unrecognised-value rule (not in the fetched pages).
Method: documentation only; no commands were run.
