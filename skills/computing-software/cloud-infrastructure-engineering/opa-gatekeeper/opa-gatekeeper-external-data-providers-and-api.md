---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-external-data-providers-and-api
name: opa-gatekeeper-external-data-providers-and-api
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, external-data, provider, providerrequest, providerresponse, caching, mutation]
level: sme
status: docs-checked
description: "Replace http.send with Gatekeeper external data Providers: why, the v1beta1 API, response format, timeouts and caching."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/externaldata.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper external data providers and api

External data (beta since v3.11) lets Gatekeeper query in-cluster providers that front image registries, directories and similar sources. It exists because OPA `http.send` cannot be used in mutation, and has security concerns: untrusted template authors could reach the in-cluster network and trusted ones must write Rego carefully to avoid injection attacks. Providers restrict reachable hosts, let Gatekeeper escape strings, share patterns such as tag-to-digest, enable caching and batching, and decouple data access from policy.

A provider is an HTTP server answering a `ProviderRequest` with a `ProviderResponse` containing items with `Key`, `Value` and `Error`; system failures go in `SystemError`. Keep provider responses within roughly 1-2 seconds. For the mutating webhook the effective timeout is the smaller of the remaining webhook deadline and the Provider `spec.timeout` (or default); with 1s left and a 10s timeout, the request is capped near 1s.

Gatekeeper controls caching and which values are significant for caching, which raises cache hit likelihood. Community providers listed include ratify, cosign-gatekeeper-provider, GitHub artifact attestations and JFrog evidence providers; trivy, tag-to-digest, aad and Kubernetes API providers are samples, unsupported.

## Checked

2026-11-04. Confirmed against externaldata.md (motivation, benefits, providers, v1beta1 API, timeouts, response fields). Removed or corrected: the v3.13 per-surface response caching claim (not on the page).

Method: documentation only; no commands were run.
