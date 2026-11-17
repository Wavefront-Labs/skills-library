---
id: computing-software.cloud-infrastructure-engineering.google-cloud.debugging-gcloud-with-log-http-and-diagnostics
name: debugging-gcloud-with-log-http-and-diagnostics
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gcloud, gcloud-debugging, gcloud-info-diagnostics, gcloud-log-http, gcloud-verbosity, gcloud-feedback]
level: practitioner
status: docs-checked
description: "Debug failing gcloud commands: --log-http to see API calls, --verbosity=debug, gcloud info and --run-diagnostics, log files, and mapping errors to the REST method."
sources: ["https://cloud.google.com/sdk/gcloud/reference", "https://cloud.google.com/sdk/gcloud/reference/info"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging gcloud with --log-http and diagnostics

## Ladder
1. **Which identity, project, config?**
   ```bash
   gcloud info --format="value(config.account)"
   gcloud auth list; gcloud config configurations list
   ```
   `gcloud info` shows the account, project and the directory paths for logs. Most "permission
   denied" reports are the wrong account or project, a named configuration selected with
   `--configuration` or `CLOUDSDK_ACTIVE_CONFIG_NAME`, or `--impersonate-service-account` in effect.
   `--project` also decides which project gets API-enablement checks and quota; `--billing-project`
   overrides that for quota and billing.
2. **What API call is made?**
   ```bash
   gcloud compute instances list --log-http
   ```
   `--log-http` logs all HTTP server requests and responses to stderr (it overrides the `core/log_http`
   property for that invocation). Read the error body for the reason and the missing permission or
   state. Redact tokens before sharing.
3. **More detail:** `--verbosity=debug`. The levels are `debug`, `info`, `warning` (default), `error`,
   `critical` and `none`.
4. **Environment checks:** `gcloud info --run-diagnostics` checks network connectivity and hidden
   properties. For certificate failures behind a proxy with a custom CA, add
   `--check-certs=<HOSTNAME>`, for example `compute.googleapis.com`.
5. **Logs:** `gcloud info` prints the log directory; `gcloud info --show-log` prints the contents of
   the last log file. `gcloud info --anonymize` minimises personal information in what you share.

## Gotchas
- `--impersonate-service-account` makes every API request in that invocation as the service account (or a delegation chain), and needs `iam.serviceAccounts.getAccessToken` (for example via `roles/iam.serviceAccountTokenCreator`). It overrides the `auth/impersonate_service_account` property, so check that property with `gcloud config get auth/impersonate_service_account`.
- `--log-http` output goes to stderr; redirect `2>&1` to capture it with stdout.
- `--quiet` overrides `core/disable_prompts` (same as `CLOUDSDK_CORE_DISABLE_PROMPTS=1`); avoid it while debugging, because prompts can explain defaults.

## Verify
- [ ] You can name the exact REST method and the missing permission/state from the response body.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the gcloud reference page (wide flags: `--log-http`, `--verbosity` levels and default,
`--impersonate-service-account`, `--quiet`, `--billing-project`, `--project`, `--configuration`) and the
`gcloud info` page (`--run-diagnostics`, `--check-certs`, `--show-log`, `--anonymize`). Removed: the grep
filter on log output, the yaml field list, log directory locations by OS, the table of error reasons,
`gcloud components update`, the `GOOGLE_APPLICATION_CREDENTIALS` and `CLOUDSDK_CORE_PROJECT` claims and the
sdk troubleshooting source (404).
