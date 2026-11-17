---
id: computing-software.cloud-infrastructure-engineering.terraform.redacting-secrets-from-terraform-logs
name: redacting-secrets-from-terraform-logs
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, log-redaction, tf-log, secrets, bug-report, crash-log]
level: practitioner
status: docs-checked
description: "Capture the smallest Terraform log with TF_LOG settings, redact credentials and identifiers, and scan the result with gitleaks before attaching it to an issue or vendor ticket."
sources: ["https://developer.hashicorp.com/terraform/internals/debugging", "https://github.com/gitleaks/gitleaks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redacting Terraform logs

Detailed logs can contain provider credentials, tokens, `Authorization` headers, user_data scripts, passwords from
plans, private keys, state snippets, account IDs and internal hostnames. Treat every log as sensitive until scrubbed.

## Capture as little as possible
Terraform's logging is controlled by environment variables (Terraform "Enable Terraform logs" page):
- `TF_LOG` enables detailed logs on stderr; levels in decreasing verbosity are `TRACE`, `DEBUG`, `INFO`, `WARN`,
  `ERROR`. Setting it to `JSON` logs at TRACE or higher in a JSON encoding that is not a stable interface.
- `TF_LOG_CORE` and `TF_LOG_PROVIDER` enable logging separately for Terraform itself and for provider plugins, with
  the same levels.
- `TF_LOG_PATH` appends the log to a file; `TF_LOG` must still be set for any logging to happen.

Minimise first: reproduce with the smallest configuration and enable only the part you need (for example
`TF_LOG_PROVIDER=DEBUG` for one provider). Less log means less to redact.

## Process
1. **Mechanical redaction.** The patterns below are examples to adapt to your own logs, not a complete list:
```bash
sed -E \
  -e 's/(Authorization: )[^\r\n]+/\1REDACTED/g' \
  -e 's/("?(password|client_secret|token|Token|SessionToken)"?[:=] *"?)[^",} ]+/\1REDACTED/g' \
  -e 's/\b[0-9]{12}\b/111122223333/g' \
  tf.log > tf.redacted.log
```
2. **Scan the result** with a secret scanner. Gitleaks scans files and directories with its `dir` command
   (`gitleaks dir [path]`, `--report-path` writes a report); the older `detect` and `protect` commands are deprecated
   since v8.19.0 but still available:
```bash
gitleaks dir tf.redacted.log --report-path leaks.json
```
3. **Manual pass** for what scanners miss: internal hostnames, customer names, IP addresses, multi-line values such as
   PEM keys or heredoc user_data that line-based `sed` cannot match, and base64 blobs (kubeconfig, user_data).
4. **Share carefully.** HashiCorp's docs ask you to include the detailed log in bug reports using a service such as
   gist, rather than pasting it inline.

## Prefer what not to capture
- Share only the relevant part of a plan rather than all of it; delete sensitive fields from any JSON you share.
- Map each real value (account ID, hostname) to one consistent placeholder so the log stays useful.

## Verify
- [ ] The scanner reports no findings on the redacted file.
- [ ] Original logs are deleted from shared runners and laptops after the ticket is filed.

## Checked
Confirmed 2026-11-08 against the Terraform "Enable Terraform logs" page (TF_LOG levels and JSON, TF_LOG_CORE,
TF_LOG_PROVIDER, TF_LOG_PATH, gist advice) and the gitleaks README (`dir` command, `--report-path`, detect and protect
deprecated in v8.19.0). Removed: AWS access key prefix pattern, private key regex, `TF_LOG_SDK_PROTO_DATA_DIR`,
`terraform show -json | jq` deletion filters and the GitHub issue template reference (page returned 404).
Method: docs-only read of cited pages, 2026-11-08
