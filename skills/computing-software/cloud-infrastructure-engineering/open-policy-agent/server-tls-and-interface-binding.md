---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.server-tls-and-interface-binding
name: server-tls-and-interface-binding
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [tls, https, opa-run, addr, certificate-reload]
level: practitioner
status: docs-checked
description: "Serve the OPA API over HTTPS with --tls-cert-file and --tls-private-key-file, reload certs with --tls-cert-refresh-period, and control listeners with --addr."
sources:
  - https://www.openpolicyagent.org/docs/security
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: encrypt traffic to the OPA server and expose only the listeners you intend.

Flags:
- `--tls-cert-file=<path>` and `--tls-private-key-file=<path>` enable HTTPS. Giving only one makes OPA exit immediately with a non-zero status.
- `--tls-cert-refresh-period=<duration>` re-checks the files for changes (for example `30s`, `5m`, `24h`); the default `0s` disables refresh.
- `--tls-ca-cert-file=<path>` supplies the CA used to validate client certificates for TLS authentication.

With TLS on, OPA ignores plain HTTP. To allow both, add another listener with `--addr`:

```
opa run --server \
  --log-level debug \
  --tls-cert-file public.crt \
  --tls-private-key-file private.key \
  --addr https://0.0.0.0:8181 \
  --addr http://localhost:8282
```

Development certificate (self-signed, not for production without understanding the risks):

```
openssl genrsa -out private.key 2048
openssl req -new -x509 -sha256 -key private.key -out public.crt -days 1
```

`curl http://localhost:8181/v1/data` is then refused, while `curl -k https://localhost:8181/v1/data` works (`-k` skips verification of the self-signed cert).

Binding: by default OPA binds to `localhost`, so it is not exposed to other machines. Keep that default when OPA is a sidecar. If remote access is needed, set `--addr 0.0.0.0:8181` and pair it with TLS plus the authorisation from server-authn-and-authz.

Check: with TLS enabled, confirm plain HTTP to the TLS port fails and HTTPS returns the data document.

## Checked

TLS flags, the refresh default, the multiple --addr example, the self-signed certificate commands and the localhost default were confirmed against the Security page.

Method: docs-checked 2026-11-09 against the OPA docs security page (docs/docs/security.md in the OPA repository, full file read).
