---
id: computing-software.cybersecurity-defensive.splunk.elastic-cross-cluster-search-security
name: elastic-cross-cluster-search-security
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [elastic-security, cross-cluster-search, ccs, remote-clusters, elasticsearch, multi-region, data-views]
level: advanced
status: docs-checked
description: "Configure Elasticsearch cross-cluster search for Elastic Security across regions or tenants: remote clusters, API-key security model, data views and rule limits."
sources: ["https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cross-cluster-search.html", "https://www.elastic.co/guide/en/elasticsearch/reference/current/remote-clusters-api-key.html", "https://www.elastic.co/guide/en/security/current/rules-cross-cluster-search.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cross-cluster search for security

Use CCS when data must stay in regional clusters but the SOC needs one view and detection rules.

## Set up remote clusters
- API-key based model (8.10+): on the remote cluster create a cross-cluster API key with
  `search` access to the indices you need; on the local cluster add the remote with
  that key (remote cluster server port defaults to 9443). The older certificate-based model needs
  matching roles on both sides.
- `GET _remote/info` shows connected status.
- Proxy mode for clusters behind load balancers.

## Use
- Index patterns: `<remote_cluster>:logs-*` alongside local patterns. Create data views and Security default indices
  (Advanced settings `securitySolution:defaultIndex`) including remote patterns.
- Detection rules: query rules can include remote patterns; the rule's API key user needs remote
  privileges. Alerts are written on the local cluster.

## Design choices
- Keep detections local to each cluster when latency or outage would make central rules miss data;
  aggregate alerts centrally via CCS on the security alerts indices.
- `skip_unavailable` is true by default since 8.15, so a regional outage does not fail every search; monitor for it or you will have silent gaps.

## Gotchas
- Version compatibility: remote must be within supported versions (generally same major or last
  minor of previous); check the documented compatibility matrix before upgrading either side.
- Field mapping conflicts across clusters break aggregations.
- ES|QL CCS support and some features lag regular search; check version notes.

## Verify
Run a search over `*:logs-*` returning hits from each remote; a test rule with a remote
pattern creates an alert from a remote event.

## Checked

Date: 2026-10-28

- Confirmed (Elasticsearch CCS and remote cluster pages): API key and TLS certificate security models (certificate model needs matching roles on both clusters), remote cluster port default 9443, skip_unavailable default true since 8.15, ccs_minimize_roundtrips is false by default for async search, remote cluster version rule (previous minor, or newer minor in the same major).
- Removed (not found): 9300 transport port, Elastic Cloud proxy-mode claim, specific index patterns for alerts, the synchronous ccs_minimize_roundtrips default.
Method: documentation only; no commands were run.

