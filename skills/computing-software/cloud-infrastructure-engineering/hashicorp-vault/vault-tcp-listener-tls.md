---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-tcp-listener-tls
name: vault-tcp-listener-tls
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, tcp-listener, tls-listener, tls-reload]
level: practitioner
status: docs-checked
description: "Configure Vault listener TLS (minimum 1.2), client certificates, cipher suites and header limits, and reload certificates with SIGHUP."
sources: ["https://developer.hashicorp.com/vault/docs/configuration/listener/tcp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The listener defaults to 127.0.0.1:8200 with TLS required. Disabling TLS needs an explicit `tls_disable = true`, which makes communication insecure.

```hcl
listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_cert_file = "/etc/vault.d/tls/tls.crt"
  tls_key_file  = "/etc/vault.d/tls/tls.key"
  tls_min_version = "tls12"
  tls_require_and_verify_client_cert = false
  max_token_header_size = 8192
}
```

Gotchas: `tls_cipher_suites` only affects TLS 1.2 and below, and `tls_prefer_server_cipher_suites` is deprecated and ignored. Certificates reload on `SIGHUP` or `tls_reload_interval` only from the same file paths; changing the paths needs a restart. `tls_disable_client_certs` and `tls_require_and_verify_client_cert` cannot both be true. `redact_*` options also affect CLI and UI output.

## Checked

2026-11-03. Confirmed against the Vault TCP listener configuration page (developer.hashicorp.com): parameters, defaults, constraints and examples. Removed: the openssl/kill Verify step, the multiple-listener `api_addr`/`cluster_addr` advice, the file ownership advice and the separate-listener paragraph (not on the page).

Method: documentation only; no commands were run.
