---
id: computing-software.cloud-infrastructure-engineering.terraform.plugin-sdk-logs-tf-log-sdk-and-proto
name: plugin-sdk-logs-tf-log-sdk-and-proto
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, tf-log-sdk, sdk-proto-logs, tf-log, debug-logging, provider-debugging]
level: practitioner
status: docs-checked
description: "Isolate provider-internal logs with TF_LOG_SDK, TF_LOG_SDK_PROTO, TF_LOG_SDK_FRAMEWORK and TF_LOG_PROVIDER_<NAME>, and know which variable overrides which."
sources: ["https://developer.hashicorp.com/terraform/plugin/log/managing", "https://developer.hashicorp.com/terraform/internals/debugging", "https://github.com/hashicorp/terraform-plugin-log"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plugin SDK log variables

Providers built on terraform-plugin-go / framework / SDKv2 use terraform-plugin-log,
which honours extra environment variables on top of `TF_LOG` / `TF_LOG_PROVIDER`.

| Variable | Scope |
|---|---|
| `TF_LOG_PROVIDER=TRACE` | all providers and provider SDKs; overrides the provider-specific and SDK variables below |
| `TF_LOG_PROVIDER_AWS=DEBUG` | one provider (`TF_LOG_PROVIDER_{PROVIDER_NAME}`); only providers that log with the `tflog` package |
| `TF_LOG_SDK=TRACE` | all SDKs used in the run; only logs written with terraform-plugin-log |
| `TF_LOG_SDK_PROTO=TRACE` | protocol layer for providers built on terraform-plugin-go; overrides `TF_LOG_SDK` |
| `TF_LOG_SDK_FRAMEWORK=TRACE` | terraform-plugin-framework; overrides `TF_LOG_SDK` |
| `TF_LOG_SDK_HELPER_SCHEMA=TRACE` | terraform-plugin-sdk/v2 `helper/schema`; overrides `TF_LOG_SDK` |
| `TF_LOG_SDK_MUX=TRACE` | terraform-plugin-mux; overrides `TF_LOG_SDK` |

`TF_LOG` overrides all of these. Levels are `OFF`, `ERROR`, `WARN`, `INFO`, `DEBUG`, `TRACE`;
`OFF` turns off that logger. Before Terraform v0.15.0, levels other than `TRACE` may not be reliable.

## Recipes
Quiet core, verbose single provider (do not set `TF_LOG` or `TF_LOG_PROVIDER` too: they
override the provider-specific variable):
```bash
export TF_LOG_CORE=OFF TF_LOG_PROVIDER_AWS=DEBUG TF_LOG_PATH=aws.log
terraform plan
```
Protocol layer only, for one resource:
```bash
export TF_LOG_SDK_PROTO=TRACE TF_LOG_PATH=proto.log
terraform apply -target=aws_lb_listener.https
```
If `TF_LOG_PATH` is unset, logs go to stderr; if the file exists, new output is appended.

## Gotchas
- Provider-specific variables do not affect logs written with legacy `log.Print*`
  functions; for remaining SDKv2 logs use `TF_LOG` or `TF_LOG_PROVIDER`.
- `TF_LOG_PROVIDER` only affects Terraform CLI runs, not provider acceptance tests.
- Treat trace logs as sensitive before sharing them.

## Verify
- [ ] The log contains protocol-layer entries for the operations of interest.
- [ ] Unrelated providers are silent in the log.

## Checked
- 2026-10-28. Confirmed against HashiCorp's "Managing Log Output" page (variable table and precedence, `TF_LOG_SDK_MUX`, levels and `OFF`, v0.15.0 note, `TF_LOG_PATH` stderr default and append behaviour, acceptance-test note) and the Terraform "Enable Terraform logs" page.
- Removed: `TF_LOG_SDK_PROTO_DATA_DIR` and its output-directory recipe, `TF_LOG_SDK_HELPER_RESOURCE`, the RPC names, the inconsistent-plan error strings, the `@module=sdk.proto` check and the OpenTofu claim (not in the fetched pages). Corrected the first recipe: `TF_LOG_PROVIDER=OFF` would override `TF_LOG_PROVIDER_AWS`.
Method: documentation only; no commands were run.
