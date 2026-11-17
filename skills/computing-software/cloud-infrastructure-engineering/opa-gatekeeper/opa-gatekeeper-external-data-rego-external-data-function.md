---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-external-data-rego-external-data-function
name: opa-gatekeeper-external-data-rego-external-data-function
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, external-data, rego, batching, provider, validation]
level: sme
status: docs-checked
description: "Call a Provider from Rego with the external_data built-in, batching keys into one request and handling per-key errors."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/externaldata.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper external data rego external data function

External data is a beta feature from Gatekeeper v3.11. For validation, Gatekeeper adds a custom OPA built-in function, `external_data`, to Rego. It takes a request object with `provider` (the Provider name) and `keys` (list of strings to send) and returns a response list of triples, one per key: `[key, value, error]`. Example response: `[["my-key","my-value",""],["another-key",42,""],["bad-key","","error message"]]`.

```rego
my_list := [img | img = input.review.object.spec.template.spec.containers[_].image]
response := external_data({"provider": "my-provider", "keys": my_list})
```

Guidance from the docs:
- Batch the keys into a single request to avoid multiple calls to the same provider.
- Each response entry carries its own error element; check it per key.
- Providers are in-cluster HTTP servers answering `ProviderRequest` with `ProviderResponse`; the docs recommend a provider timeout of at most 1 to 2 seconds. The `Provider` resource (`externaldata.gatekeeper.sh/v1beta1`) sets `url`, `timeout` in seconds and `caBundle`.
- Gatekeeper caches provider responses (v3.13 and later) with a default 3 minute TTL, configurable by `--external-data-provider-response-cache-ttl`; 0 disables the cache.

Mutation uses external data too, via `spec.parameters.assign.externalData` on `Assign` and `AssignMetadata`; for mutation Gatekeeper can batch requests via lazy evaluation. Limits: only string fields, and `ModifySet` does not support external data.

Why not `http.send`: Rego policies cannot use it for mutation, and it raises security concerns such as giving template authors access to the in-cluster network or enabling injection attacks. A provider template repository (gatekeeper-external-data-provider) and a dummy provider under `test/externaldata/dummy-provider` in the gatekeeper repository are the documented starting points.

## Checked

Method: docs-checked 2026-11-09 against the Gatekeeper website docs externaldata.md (raw markdown, relevant sections read). Removed unconfirmed claims: the v3.8.0 default for disabling http.send, the audit-only enforcement point advice, and per-provider batching across mutators.
