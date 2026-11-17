---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-ha-active-standby
name: vault-ha-active-standby
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, vault-ha, standby, request-forwarding]
level: practitioner
status: docs-checked
description: "Understand Vault HA active/standby, request forwarding, api_addr and load balancer health checks via sys/health."
sources: ["https://developer.hashicorp.com/vault/docs/concepts/ha", "https://developer.hashicorp.com/vault/api-docs/system/health", "https://developer.hashicorp.com/vault/docs/commands/status"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
One node grabs a lock in the data store and becomes active; all others are standbys that forward requests to it (request forwarding is on by default since 0.6.2).

```sh
curl -s -o /dev/null -w '%{http_code}\n' https://vault:8200/v1/sys/health
curl -s -o /dev/null -w '%{http_code}\n' 'https://vault:8200/v1/sys/health?standbyok=true'
vault status | grep -E 'HA|Active'
```

Default health codes: 200 initialised, unsealed and active; 429 unsealed and standby; 472 DR secondary; 473 performance standby; 474 standby that cannot reach the active node; 501 not initialised; 503 sealed; 530 removed. `standbyok=true` makes a standby return the active code (it does not apply to performance standbys; `perfstandbyok` covers those). Codes can be changed with parameters such as `standbycode`.

Gotchas: `api_addr` must be a full URL including scheme, set per node when clients reach nodes directly. If the only access is through a load balancer, every node's `api_addr` is the load balancer address; that can cause a redirect loop and is not recommended when it can be avoided. Clients sending `X-Vault-No-Request-Forwarding` with any non-empty value are redirected with a 307 to the active node's `api_addr`, which is also the fallback when forwarding fails. A 429 can occasionally be returned by a DR secondary or performance standby during cluster instability.

## Checked

2026-11-03. Confirmed on the HA concepts, sys/health API and vault status pages: lock-based active node, request forwarding default since 0.6.2, `X-Vault-No-Request-Forwarding` and the 307 redirect, `api_addr` as a full URL and the load balancer redirect-loop warning, the default status codes, `standbyok`, `perfstandbyok`, `HA Mode` in `vault status`. Removed: the data-store bottleneck claim, load balancer routing advice and the failover-within-seconds Verify step.

Method: documentation only; no commands were run.
