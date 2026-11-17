---
id: computing-software.cybersecurity-defensive.dex.dex-grpc-api-enable
name: dex-grpc-api-enable
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [grpc, api, tls, configuration]
level: advanced
status: docs-checked
description: "Expose the Dex gRPC API with the grpc block: addr, tlsCert, tlsKey, tlsClientCA and reflection. It is off by default."
sources:
  - https://dexidp.io/docs/configuration/api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dex offers a gRPC service for programmatic changes to its state, such as creating clients or managing local password users. It is aimed at management apps and not expected to be used by most installations. It is off by default.

Enable it in the config:

```yaml
grpc:
  addr: 127.0.0.1:5557
  tlsCert: /etc/dex/grpc.crt
  tlsKey: /etc/dex/grpc.key
  tlsClientCA: /etc/dex/client.crt
  reflection: true
```

- `addr`: listen address. It cannot be the same as an HTTP(S) service address.
- `tlsCert`, `tlsKey`: server certificate. If TLS credentials are not provided, Dex runs in plaintext mode.
- `tlsClientCA`: CA used for client certificate auth.
- `reflection`: enables gRPC reflection.

Gotcha: the API provides no authentication or authorization beyond TLS client auth, so provide TLS credentials and `tlsClientCA`.

Dex ships no `dexctl` command-line tool; the maintainers say CLIs are hard to version and expose another interface that can never change. The API is gRPC only, since v2 moved away from REST.

## Checked

2026-11-08: Read the Dex API page in full. Confirmed the off-by-default grpc block and each field, the plaintext fallback without TLS credentials, the no-auth-beyond-TLS-client-auth statement, the dexctl note and the move from REST to gRPC. Removed the network binding advice and the reflection check, which that page does not state.
Method: documentation only; no commands were run.
