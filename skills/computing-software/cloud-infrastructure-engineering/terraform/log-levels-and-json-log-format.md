---
id: computing-software.cloud-infrastructure-engineering.terraform.log-levels-and-json-log-format
name: log-levels-and-json-log-format
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, log-levels, json-logging, tf-log, tf-log-json, trace, debug, info, warn, error, log-parsing, jq]
level: practitioner
status: gated
description: "Pick the right TF_LOG level (TRACE/DEBUG/INFO/WARN/ERROR/JSON), know what each actually prints, and parse TF_LOG=JSON output with jq to isolate provider HTTP calls."
sources: ["https://developer.hashicorp.com/terraform/internals/debugging", "https://developer.hashicorp.com/terraform/cli/config/environment-variables#tf_log"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log levels and JSON log format

**Goal:** get the lines you need from `TF_LOG` without drowning in the ones you
do not.

## 1. Levels
| `TF_LOG=` | You get |
|---|---|
| `ERROR` | only failures (nothing on a clean `plan`: 0 lines) |
| `WARN` | warnings (0 lines on a clean `plan`) |
| `INFO` | lifecycle milestones: Terraform and Go version, `CLI args`, backend operation start/finish, provider process start and exit (17 lines for a `plan` with one `null` resource) |
| `DEBUG` | adds provider RPC boundaries and plugin handshake detail (79 lines for the same plan) |
| `TRACE` | everything, including graph and provider protocol messages and, for providers that log them, HTTP traffic (589 lines) |
| `JSON` | TRACE-level content, one JSON object per line (522 lines, 62 debug, 17 info, 443 trace) |
Any other non-empty value that is not a level name (e.g. `TF_LOG=1`, `true`) gave the same 589 lines as TRACE; `TF_LOG=off` gave 0.
`TF_LOG_CORE` and `TF_LOG_PROVIDER` set the level per side (core TRACE alone: 436 lines, provider TRACE alone: 153; together 589 = `TF_LOG=TRACE`).
(Counts are Terraform 1.17.0 on Windows with the `null` provider; they vary by config and platform. `TF_LOG_PATH` unset sends the log to stderr.)

Practical defaults: `DEBUG` to see *which* call hangs; `TRACE` with
`TF_LOG_PROVIDER` to see the HTTP bodies for one provider; `JSON` when you will
grep/jq.

## 2. JSON format
```bash
TF_LOG=JSON TF_LOG_PATH=tf.json.log terraform plan
head -1 tf.json.log
{"@level":"info","@message":"Terraform version: 1.17.0","@timestamp":"2026-10-22T10:02:45.511991+10:00"}
```
Fields: `@level`, `@message`, `@timestamp` on every line; `@module` only on provider-side lines (seen: `provider`, `provider.stdio`,
`provider.terraform-provider-null_v3.3.2_x5.exe`, `sdk.proto`, `sdk.framework`); **core lines have no `@module` at all** (369 of 522 lines).
Structured extras seen: `@caller`, `tf_rpc`, `tf_req_id`, `tf_provider_addr`, `tf_resource_type`, `tf_proto_version`,
`tf_attribute_path`, `tf_req_duration_ms`. HTTP-specific fields such as `tf_http_res_status_code` come from providers that log HTTP
traffic with terraform-plugin-log and were not produced by the `null` provider (gated: unconfirmed, source is paywalled or blocked).

## 3. jq recipes
```bash
# all HTTP responses from the AWS provider with status >= 400
jq -c 'select(.tf_http_res_status_code? >= 400) | {t:.["@timestamp"], rpc:.tf_rpc, type:.tf_resource_type, status:.tf_http_res_status_code, body:.tf_http_res_body}' tf.json.log
# RPC lines (parenthesise the "and"; without the parentheses jq errors "boolean (false) cannot be matched")
jq -r 'select(.tf_rpc? and (.["@message"]|test("Calling|Called"))) | "\(.["@timestamp"]) \(.tf_rpc) \(.tf_resource_type // "")"' tf.json.log
# core-only lines (no @module key; startswith on the missing key would error)
jq -c 'select(has("@module")|not)' tf.json.log
# messages at warn or above
jq -c 'select(.["@level"]=="warn" or .["@level"]=="error")' tf.json.log
```
Correlate a request/response pair by `tf_req_id`.

## 4. Redaction
TRACE/JSON logs include request and response bodies: credentials in headers are
usually masked by providers, but **response bodies** (secrets, connection
strings) are not. Treat log files as sensitive; delete after use; never attach
unredacted to an issue.

## Gotchas
- `TF_LOG` without `TF_LOG_PATH` writes to **stderr**, interleaved with UI; in
  CI pipe stderr to a file.
- Providers using the old SDK log at whatever level they were compiled with;
  `TF_LOG_PROVIDER=DEBUG` may still show TRACE-ish noise from them.
- `TF_LOG=JSON` is a level name; `-json` on the command is a different thing (UI
  stream).
- Setting `TF_LOG` globally in a shell profile slows every command and fills
  disks; export it per invocation.
- OpenTofu 1.13.2: same `TF_LOG`/`TF_LOG_PATH` variables and `JSON` level, same layout (core lines without `@module`; the provider module is
  `provider.terraform-provider-null.exe`), so `startswith("tofu")` matches nothing.

## Verify
- [ ] `TF_LOG=INFO terraform plan 2>&1 >/dev/null | wc -l` is small (17 here) and `TRACE` is in the hundreds (589); `terraform version` is much quieter (5 and 17).
- [ ] `jq -c 'select(.tf_http_res_status_code?)' tf.json.log | head` shows provider HTTP status codes.

## Checked
- Terraform 1.17.0 and OpenTofu 1.13.2 on Windows with `hashicorp/null` (one resource): line counts per level, `1`/`true`/`off` handling, `TF_LOG_CORE`/`TF_LOG_PROVIDER` split, JSON first line and field inventory, level mix in the JSON file, absence of `@module` on core lines, the jq error from the unparenthesised `and` recipe and its parenthesised form, the `startswith` error on lines with no `@module`, OpenTofu module names.
- The AWS HTTP-status recipe (`tf_http_res_status_code`, `tf_http_res_body`) and the `tf_req_id` request/response correlation of HTTP calls were not run (no HTTP-logging provider or AWS account). The level-meaning descriptions beyond the counts above, the `JSON` since-0.15 label (removed), the old-SDK logging note and the redaction advice are stated from documentation or experience and were not tested (gated: unconfirmed, source is paywalled or blocked). The reason is that no cloud provider was available.
