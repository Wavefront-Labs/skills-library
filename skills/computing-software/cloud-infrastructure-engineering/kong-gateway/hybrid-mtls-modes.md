---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.hybrid-mtls-modes
name: hybrid-mtls-modes
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, cluster-mtls, pki, cluster-cert, hybrid-mode, gen-cert]
level: advanced
status: docs-checked
description: "Hybrid cluster_mtls modes shared, pki and pki_check_cn: which certs each needs (cluster_cert, cluster_ca_cert, cluster_server_name) and kong hybrid gen_cert."
sources:
  - https://developer.konghq.com/gateway/hybrid-mode/
  - https://developer.konghq.com/gateway/cli/reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cluster_mtls modes

`cluster_mtls` defaults to `shared`; other values are `pki` and `pki_check_cn`.

- **shared:** control plane and data plane present the same `cluster_cert` and `cluster_cert_key` pair. `cluster_server_name` is ignored and `kong_clustering` is used.
- **pki:** each data plane gets its own certificate issued by the cluster CA in `cluster_ca_cert`. `cluster_ca_cert` is required on the data plane, and `cluster_server_name` must match the CN or SAN of the control plane certificate.
- **pki_check_cn:** like `pki`, and also checks the data plane certificate's common name against `cluster_allowed_common_names`.

Generate a shared pair with the CLI:

```bash
kong hybrid gen_cert [<cert> <key>]
```

Defaults are `./cluster.crt` and `./cluster.key`; `-d, --days` defaults to 1095.

If the CP certificate comes from a well-known CA, set `lua_ssl_trusted_certificate=system` on the DP and leave `cluster_ca_cert` empty.

`cluster_cert`, `cluster_cert_key` and `cluster_ca_cert` are startup-critical: if a vault reference for any of them fails to resolve, the DP will not start.

## Checked

2026-11-04. Confirmed against the Hybrid mode page and the CLI reference: the three modes and their certificate rules, `cluster_allowed_common_names`, `kong hybrid gen_cert` defaults and the 1095-day default, the well-known CA note and the startup-critical warning. Nothing removed.
Method: documentation only; no commands were run.
