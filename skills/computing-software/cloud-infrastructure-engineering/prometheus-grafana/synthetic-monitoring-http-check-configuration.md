---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.synthetic-monitoring-http-check-configuration
name: synthetic-monitoring-http-check-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [synthetic-monitoring, http-check-config, synthetic-http-assertions, tls-validation, grafana-cloud]
level: practitioner
status: docs-checked
description: "Configure Grafana Synthetic Monitoring HTTP checks: probes, frequency, timeout, status codes, regex assertions, TLS, auth, secrets, metrics."
sources: ["https://grafana.com/docs/grafana-cloud/testing/synthetic-monitoring/create-checks/checks/http/", "https://github.com/grafana/terraform-provider-grafana/blob/main/docs/resources/synthetic_monitoring_check.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Synthetic Monitoring HTTP checks

**Goal:** a check that fails when users would see a problem, and only then.

## Settings (from the HTTP check page)
- Create: Testing & synthetics > Synthetics > Create new check, type API Endpoint, request type HTTP; Save schedules,
  Test runs it once.
- Common: Enabled, Job name (becomes the `job` label), Target (the `instance` label), Probe locations (the `probe`
  label), Frequency 10 to 3600 seconds, Timeout 1 to 60 seconds, Custom labels.
- HTTP: request method, body, headers, compression algorithm (the response must carry a matching header and be
  compressed with it, or the check fails), proxy URL and proxy connect headers, Publish full set of metrics (default
  false, to limit active series).
- Default User-Agent is `synthetic-monitoring-agent/<version> (...)`; override it by adding a User-Agent request header.
- TLS: Disable target certificate validation, Server name, CA certificate, Client certificate, Client key.
- Authentication: bearer or basic header. Synthetic Monitoring secrets can hold basic-auth passwords, bearer tokens, CA
  certificates, client certificates and client keys (every selected probe must support secrets); not usernames, custom
  headers or proxy connect headers.
- Validation: valid status codes (default 2xx), valid HTTP versions, SSL option (require or reject; default ignore), and
  regex validations on a header or the body using Go syntax. A regex check fails on a match unless invert match is
  selected, which fails on no match; header checks can allow a missing header.
- Advanced: IP version (V4, V6, or Any, which prefers IPv6 and does not retry another version if the connection
  fails), Follow redirects, Cache busting query parameter name.
- Limit: request body is capped at 64KB.
- Useful metrics: `probe_success`, `probe_duration_seconds`, `probe_http_status_code`, `probe_failed_due_to_regex`,
  `probe_ssl_earliest_cert_expiry`, `sm_check_info` (only this metric carries the frequency label).

## As code
```hcl
data "grafana_synthetic_monitoring_probes" "main" {}

resource "grafana_synthetic_monitoring_check" "health" {
  job       = "checkout-http"
  target    = "https://example.com/health"
  enabled   = true
  probes    = [data.grafana_synthetic_monitoring_probes.main.probes.London,
               data.grafana_synthetic_monitoring_probes.main.probes.Frankfurt]
  frequency = 60000            # milliseconds in Terraform
  timeout   = 5000
  labels    = { team = "payments" }
  settings {
    http {
      method                          = "GET"
      valid_status_codes              = [200]
      fail_if_not_ssl                 = true
      fail_if_body_not_matches_regexp = ["ok"]
    }
  }
}
```
Other attributes seen in the provider page: `no_follow_redirects`, `bearer_token`, `basic_auth`, `headers`,
`valid_http_versions`, `tls_config`, `fail_if_header_matches_regexp` (with `allow_missing`).

## Verify
- [ ] Temporarily set an impossible body regex and confirm the check fails with `probe_failed_due_to_regex`, then revert.

## Checked

2026-11-08. Confirmed against the Synthetic Monitoring HTTP check page and the provider's
grafana_synthetic_monitoring_check page (raw from terraform-provider-grafana; the registry page was unreadable).
Frequency units in Terraform are inferred from the provider's traceroute example (`frequency = 120000`). Removed as
unconfirmed: the guidance table (3+ probes, 60 s typical), the PromQL alert example and the private-probe advice.
Method: documentation only; no commands were run.
