---
id: computing-software.cloud-infrastructure-engineering.openbao.transit-seal
name: transit-seal
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, transit-seal, auto-unseal, key-name, orphan-token]
level: advanced
status: docs-checked
description: "Auto-unseal OpenBao with another cluster's transit engine: required parameters, env vars, token policy and token lifetime traps."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/configuration/seal/transit.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transit seal

Activate with a `seal "transit"` block or `BAO_SEAL_TYPE=transit`.

```hcl
seal "transit" {
  address    = "https://openbao.example.com:8200"
  key_name   = "seal-key"
  mount_path = "transit/"
}
```

## Parameters (env var)

Required: `address` (`BAO_ADDR`), `token` (`BAO_TOKEN`), `key_name` (`VAULT_TRANSIT_SEAL_KEY_NAME`), `mount_path` (`VAULT_TRANSIT_SEAL_MOUNT_PATH`).

Optional: `namespace` (`BAO_NAMESPACE`), `disable_renewal` (default `"false"`, `VAULT_TRANSIT_SEAL_DISABLE_RENEWAL`), `tls_ca_cert` (`BAO_CACERT`), `tls_client_cert` (`BAO_CLIENT_CERT`), `tls_client_key` (`BAO_CLIENT_KEY`), `tls_server_name` (`BAO_TLS_SERVER_NAME`), `tls_skip_verify` (`BAO_SKIP_VERIFY`), `disabled`.

`disabled = true` only when migrating from an auto seal; otherwise false. `disable_renewal` suits a token managed by another tool such as OpenBao Agent.

## Token policy

The token needs `update` on the transit key's encrypt path and decrypt path under the mount path and key name.

## Warnings

- Set the token with the environment variable rather than in the config file (strongly recommended).
- The token should probably be an orphan token, otherwise the seal breaks when the parent expires or is revoked.
- Prefer a periodic token without an explicit max TTL, or it eventually cannot renew.
- `tls_skip_verify` is highly discouraged.
- Never disable or delete old transit keys; older data needs them after rotation.

## Checked

2026-11-04. Read the OpenBao transit seal page in full. Confirmed: activation by block or `BAO_SEAL_TYPE`, required and optional parameters with their environment variables, `disable_renewal`, `disabled`, the token policy paths, orphan and periodic token advice, `tls_skip_verify` warning and the key rotation note. Softened: orphan token and environment variable advice to the page's wording.
Method: documentation only; no commands were run.
