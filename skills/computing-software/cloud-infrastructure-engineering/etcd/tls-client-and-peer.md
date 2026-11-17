---
id: computing-software.cloud-infrastructure-engineering.etcd.tls-client-and-peer
name: tls-client-and-peer
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [tls, security, cert-file, key-file, trusted-ca-file, client-cert-auth, peer-tls, auto-tls, certificates]
level: advanced
status: docs-checked
description: "Enable TLS for client and peer traffic with --cert-file, --key-file, --trusted-ca-file, --client-cert-auth and the peer-* equivalents."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/security/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

etcd supports TLS for client-to-server and peer-to-peer connections, configured separately.

Client:

```bash
etcd --cert-file=/path/to/server.crt --key-file=/path/to/server.key   --client-cert-auth --trusted-ca-file=/path/to/ca.crt   --advertise-client-urls https://host:2379 --listen-client-urls https://host:2379
```

- `--cert-file`, `--key-file`: server certificate and key.
- `--client-cert-auth`: check all incoming HTTPS requests for a client certificate signed by the trusted CA; requests without a valid one fail. If authentication is enabled, the certificate provides credentials for the user named by its Common Name field. `--key-file` must be unencrypted.
- `--trusted-ca-file`: trusted certificate authority.
- `--auto-tls`: use automatically generated self-signed certificates for client connections; this encrypts traffic but does not authenticate.

Peer: `--peer-cert-file`, `--peer-key-file`, `--peer-client-cert-auth`, `--peer-trusted-ca-file`, `--peer-auto-tls`, with `https://` in the peer URLs. The peer certificate is used both for listening on the peer address and for sending requests to other peers. Since v3.2.0 the server checks peer certificates against the remote address: with IP SANs the remote IP must match one, and with only DNS names a forward lookup of those names must match the remote IP.

Other flags: `--tls-min-version` (minimum supported TLS version), `--cipher-suites` (comma-separated list; an empty value is auto-populated by Go; clients must use one of the listed suites) and `--peer-cert-allowed-cn` (only peers whose certificate has the matching Common Name are authenticated).

Since v3.2.0, TLS certificates are reloaded on every client connection, so expired certificates can be replaced by overwriting the files without stopping etcd servers.

## Checked

2026-11-03. Confirmed on the v3.5 security model page: --cert-file, --key-file (unencrypted), --client-cert-auth and the Common Name credential rule, --trusted-ca-file, --auto-tls, the peer-* flags, --cipher-suites, --tls-min-version, --peer-cert-allowed-cn, certificate reload on every client connection since v3.2.0, and the v3.2.0 IP and DNS SAN checks for peers. Removed: the TLS 1.2 default, --tls-max-version, --client-crl-file, --cert-allowed-cn, the server-and-client usage claim and the passwordless user-name statement, none of which the page states in that form.

Method: documentation only; no commands were run.
