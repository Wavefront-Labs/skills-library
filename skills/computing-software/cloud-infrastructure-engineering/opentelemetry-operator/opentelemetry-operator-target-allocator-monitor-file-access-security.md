---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-target-allocator-monitor-file-access-security
name: opentelemetry-operator-target-allocator-monitor-file-access-security
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, denyfsaccessthroughsms, arbitrary-file-access, bearertokenfile, multi-tenant, privilege-escalation]
level: sme
status: docs-checked
description: "Prevent tenants from reading the collector service account token through ServiceMonitor bearerTokenFile and relabelings by restricting selectors or setting denyFSAccessThroughSMs."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/target-allocator/security.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/target-allocator/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ServiceMonitor file access escalation

Risk: by default, anyone who can create a Service or Pod Monitor that your TargetAllocator selects can read arbitrary single-line files from the collector's pod, including its service account token or mounted secrets, and have them sent to an address they choose. File paths in `bearerTokenFile` and `tlsConfig` (`caFile`, `certFile`, `keyFile`) resolve against the collector's own filesystem at scrape time. Combined with `relabelings`, a monitor can set `__address__` to an attacker service, so the token is sent there.

This is allowed by default to match prometheus-operator's `arbitraryFSAccessThroughSMs` default, and common setups rely on it, for example scraping the API server or kubelet with `bearerTokenFile` pointing at the service account token. It matters in multi-tenant clusters: creating a ServiceMonitor is namespaced and widely granted (the built-in `edit` ClusterRole includes it), the collector's service account is usually more privileged, and `serviceMonitorNamespaceSelector: {}` selects every namespace.

Two mitigations, combinable:
1. Restrict selection: scope `serviceMonitorNamespaceSelector`, `podMonitorNamespaceSelector`, `probeNamespaceSelector` and `scrapeConfigNamespaceSelector` to trusted namespaces instead of `{}`.
2. Reject file references: `prometheusCR.denyFSAccessThroughSMs: true` (standalone allocators use `deny_fs_access_through_sms: true`). Scrape configs generated from endpoints that reference a file are dropped, a warning naming the job and field is logged, and other endpoints of the same monitor are unaffected.

Trade-off: enabling deny breaks monitors that legitimately use file credentials, including API server and kubelet scraping, so move those to secret-based credentials or leave the setting off.

## Checked

Method: docs-checked 2026-11-09 against the Target Allocator security page (read in full) and the OpenTelemetryCollector API reference entry for denyFSAccessThroughSMs.
