---
id: computing-software.cloud-infrastructure-engineering.terraform.http-data-source
name: http-data-source
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, http-data-source, hashicorp-http, api-lookup, retry, postcondition]
level: practitioner
status: docs-checked
description: "Fetch values from HTTP APIs with the hashicorp/http data source: methods, headers, retry, CA settings, status-code postconditions, and parsing the response body."
sources: ["https://raw.githubusercontent.com/hashicorp/terraform-provider-http/main/docs/data-sources/http.md", "https://ip-ranges.amazonaws.com/ip-ranges.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The `http` data source

```hcl
data "http" "ip_ranges" {
  url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
  request_headers = {
    Accept = "application/json"
  }
  retry {
    attempts     = 3
    min_delay_ms = 500
  }
  lifecycle {
    postcondition {
      condition     = self.status_code == 200
      error_message = "ip-ranges returned HTTP ${self.status_code}."
    }
  }
}

locals {
  cloudfront_cidrs = [
    for p in jsondecode(data.http.ip_ranges.response_body).prefixes :
    p.ip_prefix if p.service == "CLOUDFRONT"
  ]
}
```

## Arguments worth knowing
- `url` (required): `http` or `https`. The data source warns if the result is not UTF-8.
- `method`: `GET`, `HEAD` or `POST`; `POST` is only intended for read-only URLs such as submitting a search.
  `request_body` is a string.
- `request_headers`: map of header names to values.
- `ca_cert_pem`, `client_cert_pem`, `client_key_pem`: PEM strings for custom CA and client certificates.
- `insecure`: disables verification of the server's certificate chain and hostname; defaults to `false`.
- `request_timeout_ms`.
- `retry { attempts, min_delay_ms, max_delay_ms }`: by default there are no retries. Retries happen on client errors
  (for example connection errors) and 5xx responses except 501. `attempts = 2` means up to 3 tries in total.
- Read-only: `status_code`, `response_body`, `response_body_base64`, `response_headers`, `id` (the URL). `body` is
  deprecated; use `response_body`.

## Status codes and conditions
The provider docs show checking `self.status_code` in a `lifecycle` `postcondition` on the data source, or in a
`precondition` on a resource that uses it. Pre and postconditions need Terraform v1.2.0 or later. Check the code
yourself rather than assuming a non-success response fails the plan.

## Trust
`https` verifies only the server certificate's chain of trust; the docs warn that data from servers you do not control
should be treated as untrustworthy.

## Uses
- Published IP ranges for allow-lists: the AWS file has a `prefixes` list whose entries carry `ip_prefix` and
  `service` (for example `CLOUDFRONT`).
- Fetch a public key or a release manifest.

## Gotchas
- `jsondecode` fails on non-JSON bodies such as HTML error pages; the status-code postcondition guards against that.
- Do not put secrets in `request_headers` without considering that the data source arguments and response are
  recorded by Terraform; prefer short-lived tokens.

## Verify
- [ ] `terraform console`: `length(local.cloudfront_cidrs)` is greater than 0.
- [ ] Pointing at a 404 URL fails with your postcondition message, not a JSON parse error.

## Checked
Confirmed 2026-11-08 against the hashicorp/http data source doc (arguments, retry behaviour, methods, postcondition
and Terraform 1.2.0 note, trust warning) and the AWS ip-ranges.json file (`prefixes`, `ip_prefix`, `service`
`CLOUDFRONT`). Removed: the "provider v3+" and "non-2xx do not error since v3" claims, per-plan runtime, state
contents and plan-time unknown URL claims, and the JWKS and `check` block uses (not on the cited pages).
Method: docs-only read of cited pages, 2026-11-08
