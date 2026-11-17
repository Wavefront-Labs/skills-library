---
id: computing-software.messaging-and-integration.dapr.api-allowlist-denylist-sidecar-apis
name: api-allowlist-denylist-sidecar-apis
category: computing-software
field: messaging-and-integration
product: dapr
tags: [configuration, api-allowlist, api-denylist, attack-surface, zero-trust, http, grpc]
level: advanced
status: docs-checked
description: "Restrict which Dapr sidecar APIs an app can reach with spec.api.allowed or denied: name, version and protocol entries, precedence rules and the API name table."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/configuration/api-allowlist.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For zero trust networks or when the sidecar is exposed to outside traffic, enable only the APIs the app uses. Rules:

- No allowlist or denylist: every API is allowed.
- Only a denylist: everything except the listed APIs.
- Only an allowlist: only the listed APIs.
- Both: the denylist overrides the allowlist for APIs in both.

Allow only the state HTTP API (all other HTTP APIs blocked):

```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: myappconfig
  namespace: default
spec:
  api:
    allowed:
      - name: state
        version: v1.0
        protocol: http
```

For gRPC use `version: v1` and `protocol: grpc`. A denylist uses `api.denied` with the same entry shape, for example name `state`, version `v1.0`, protocol `http` to disable that one API.

Names and versions from the page: `invoke` (`v1.0` / gRPC `v1`), `state` (`v1.0`, `v1.0-alpha1` / `v1`, `v1alpha1`), `publish` (same pattern), `bindings` (`v1.0` / `v1`), `subscribe` (gRPC `v1alpha1` only), `secrets`, `actors`, `metadata`, `configuration` (`v1.0`, `v1.0-alpha1`), `lock` and `unlock` (`v1.0-alpha1`), `crypto` (`v1.0-alpha1`), `workflows` (`v1.0`), `conversation` (`v1.0-alpha1`), `healthz` (HTTP `v1.0` only) and `shutdown` (`v1.0` / `v1`).

Each entry carries a name, version and protocol. The page's examples say an HTTP state allowlist entry blocks all other HTTP APIs and a gRPC one blocks all other gRPC APIs. It does not say how alpha versions such as `v1.0-alpha1` are treated when only `v1.0` is listed.

## Checked

2026-11-08. Default and precedence rules, all four YAML shapes and the API name and version table confirmed on the Selectively enable Dapr APIs page. Changed: replaced an inference about alpha versions and cross-protocol effects with what the page states. Other claims unchanged.

Method: documentation only; every cited page read in full; no commands were run.
