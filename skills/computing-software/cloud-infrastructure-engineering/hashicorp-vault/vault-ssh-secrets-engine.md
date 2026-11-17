---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-ssh-secrets-engine
name: vault-ssh-secrets-engine
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, ssh-secrets, ssh-ca, signed-certificates]
level: practitioner
status: docs-checked
description: "Configure Vault SSH signed certificates for short-lived user access, trusting the CA key on servers, plus the host-signing mount."
sources: ["https://developer.hashicorp.com/vault/docs/secrets/ssh", "https://developer.hashicorp.com/vault/docs/secrets/ssh/signed-ssh-certificates"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The SSH engine has two modes: signed SSH certificates and one-time SSH passwords. Dynamic SSH keys were removed in Vault 1.13.

```sh
vault secrets enable -path=ssh-client-signer ssh
vault write ssh-client-signer/config/ca generate_signing_key=true
vault write ssh-client-signer/roles/my-role -<<"EOH"
{
  "algorithm_signer": "rsa-sha2-256",
  "allow_user_certificates": true,
  "allowed_users": "*",
  "allowed_extensions": "permit-pty,permit-port-forwarding",
  "default_extensions": { "permit-pty": "" },
  "key_type": "ca",
  "default_user": "ubuntu",
  "ttl": "30m0s"
}
EOH
vault write -field=signed_key ssh-client-signer/sign/my-role public_key=@$HOME/.ssh/id_rsa.pub > signed-cert.pub
ssh-keygen -Lf signed-cert.pub
```

- Servers trust the CA by setting `TrustedUserCAKeys` in `sshd_config` to the CA public key file.
- Sign a user public key with the role; the output is a certificate used with `ssh -i signed-cert.pub -i ~/.ssh/id_rsa user@host`.
- Host keys can be signed by a separate mount (for example `ssh-host-signer`) whose role sets `allow_host_certificates`; clients then trust it through a `@cert-authority` line in `known_hosts`.

## Checked
2026-11-03. Confirmed on the SSH secrets engine page (two modes, removal of dynamic keys in 1.13, `generate_signing_key=true`, role fields, `-field=signed_key` signing, `TrustedUserCAKeys`, `ssh-keygen -Lf`, separate host-signer mount with `allow_host_certificates`). Removed: the "reload sshd" step, signing-key protection advice, the `ssh ops@host` Verify step and the closing paragraph.
Method: documentation only; no commands were run.
