---
id: computing-software.cloud-infrastructure-engineering.openbao.ssh-signed-certificates
name: ssh-signed-certificates
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, ssh, signed-certificates, trusted-user-ca-keys, host-certificates]
level: advanced
status: docs-checked
description: "Use OpenBao as an SSH CA: enable the engine, generate the CA, sign user and host keys, and configure sshd to trust it."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/secrets/ssh/signed-ssh-certificates.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSH signed certificates

## CA

```
bao secrets enable -path=ssh-client-signer ssh
bao write ssh-client-signer/config/ca generate_signing_key=true
```

Or supply `private_key` and `public_key`. Do not add a password to the private key; OpenBao cannot decrypt it.

## Client role keys

`allow_user_certificates`, `allowed_users` (`*`), `allowed_extensions` (e.g. `permit-pty,permit-port-forwarding`), `default_extensions`, `key_type` `ca`, `default_user`, `ttl` (e.g. `30m0s`).

## Host role keys

Extend the mount's maximum TTL first with `bao secrets tune -max-lease-ttl=87600h ssh-host-signer`. Role: `key_type=ca`, `algorithm_signer=rsa-sha2-256`, `ttl=87600h`, `allow_host_certificates=true`, `allowed_domains="localdomain,example.com"`, `allow_subdomains=true`.

## Sign and inspect

```
bao write -field=signed_key ssh-client-signer/sign/my-role public_key=@$HOME/.ssh/id_rsa.pub > signed-cert.pub
bao write ssh-host-signer/sign/hostrole cert_type=host public_key=@/etc/ssh/ssh_host_rsa_key.pub
ssh-keygen -Lf ~/.ssh/signed-cert.pub
```

## sshd_config

```
TrustedUserCAKeys /etc/ssh/trusted-user-ca-keys.pem
HostKey /etc/ssh/ssh_host_rsa_key
HostCertificate /etc/ssh/ssh_host_rsa_key-cert.pub
LogLevel VERBOSE
```

`LogLevel VERBOSE` helps annotate errors on first setup. Set host cert mode with `chmod 0640`.

## Checked

2026-11-04. Read the OpenBao signed SSH certificates page in full. Confirmed: mount and CA commands, the no-password private key warning, client and host role parameters, signing commands, `ssh-keygen -Lf`, `sshd_config` directives, `LogLevel VERBOSE` troubleshooting and the `0640` mode. Added from the page: the `bao secrets tune -max-lease-ttl` step before the host role. Removed: nothing.
Method: documentation only; no commands were run.
