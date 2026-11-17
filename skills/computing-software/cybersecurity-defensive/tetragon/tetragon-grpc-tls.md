---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-grpc-tls
name: tetragon-grpc-tls
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [grpc-tls]
level: advanced
status: docs-checked
description: "Enable TLS or mTLS on the Tetragon gRPC TCP listener with Helm, choose certificate provisioning, and connect with tetra."
sources:
  - "https://tetragon.io/docs/installation/grpc-tls/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secure the gRPC API with TLS

Tetragon serves gRPC on an always-on unix socket (`/var/run/tetragon/tetragon.sock`, protected by file permissions) and an optional TCP listener for off-host clients. TLS applies only to the TCP listener and is silently ignored when `--server-address` is a `unix://` socket. Exposing TCP without client verification lets unprivileged users with network access modify Tetragon's configuration.

## Enable TLS (Helm, auto-provisioned)

```shell
helm upgrade --install tetragon cilium/tetragon -n kube-system \
  --set tetragon.grpc.address=0.0.0.0:54321 \
  --set tetragon.grpc.tls.enabled=true
```

The chart generates a CA and a server certificate with wildcard SAN `*.tetragon-grpc.cilium.io`, stored in a Secret mounted at `/var/lib/tetragon/tls/`. Add `--set tetragon.grpc.tls.requireClientCert=true` for mTLS; mint client certificates from the same CA.

## Provisioning (`tetragon.grpc.tls.auto.method`)

- `helm` (default): Helm renders the Secret; rotation needs `helm upgrade`.
- `cronJob`: `cilium-certgen` rotates on `auto.schedule`; a bootstrap Job seeds the Secret.
- `certmanager`: set `auto.certManagerIssuerRef` to your Issuer/ClusterIssuer.

Bring your own: set `tetragon.grpc.tls.auto.enabled=false` and `tetragon.grpc.tls.server.existingSecret=my-tetragon-grpc-tls`. The Secret needs `tls.crt`, `tls.key`, and `ca.crt` (required with `requireClientCert=true`).

## Connect with tetra

```shell
tetra \
  --server-address tetragon.example.com:54321 \
  --tls-ca-cert-files ca.crt \
  --tls-cert-file client.crt \
  --tls-key-file client.key \
  --tls-server-name node.tetragon-grpc.cilium.io \
  getevents
```

Drop the cert and key flags for TLS-only mode. `--tls-server-name` alone uses the system CA bundle. `--tls-skip-verify` is for local development only and excludes `--tls-ca-cert-files`.

## Standalone (container or systemd)

```shell
echo "0.0.0.0:54321"             > /etc/tetragon/tetragon.conf.d/server-address
echo "/etc/tetragon/tls/tls.crt" > /etc/tetragon/tetragon.conf.d/server-tls-cert-file
echo "/etc/tetragon/tls/tls.key" > /etc/tetragon/tetragon.conf.d/server-tls-key-file
# mTLS also needs server-tls-require-client-cert (true) and server-tls-client-ca-files
```

The agent watches the TLS files with `fsnotify` and reloads atomically; no restart is needed on in-place updates.

## Checked

Date: 2026-11-07

gRPC TLS page read in full; every claim matched, no change.

Method: documentation only; no commands were run.
