---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-token-formats-and-types
name: k3s-token-formats-and-types
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, server-token, agent-token, secure-token-format]
level: practitioner
status: docs-checked
description: "Understand K3s secure versus short tokens, and the server, agent and bootstrap token types and where they are stored."
sources:
  - https://docs.k3s.io/cli/token
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tokens secure the node join process and encrypt confidential data in the datastore. They authenticate the cluster to the joining node and the node to the cluster.

Formats:

- Secure (preferred): `K10<cluster CA hash>::<credentials>`. The joining node downloads the CA bundle from /cacerts with TLS verification off, hashes it with SHA256 (for custom CAs, the SHA256 of the DER encoding of the root cert, the fingerprint), compares it with the token, validates the server certificate against that bundle, and only then sends credentials.
- Short: only the password or bearer token. The node implicitly trusts the server CA bundle, so the first connection may be open to man-in-the-middle.

Types:

- Server: --token / K3S_TOKEN. If none is given, the first server creates a random one. Always written in secure format to /var/lib/rancher/k3s/server/token. It can join servers and agents, and anyone holding it effectively has full admin access. It is also the PBKDF2 passphrase encrypting bootstrap data, so back it up with the datastore.
- Agent: --agent-token / K3S_AGENT_TOKEN. Defaults to the server token; static, never expires; set on all servers; written to /var/lib/rancher/k3s/server/agent-token (a link to the server token if unset).
- Bootstrap: dynamically generated, expiring agent tokens.

Unless custom CA certificates are used, the first server can only start with the short format, since the CA hash is unknown until the CA is generated.

## Checked

2026-11-03: read docs.k3s.io cli/token. Confirmed: the K10 secure format and TLS bootstrapping steps, the short format, the server, agent and bootstrap token types and file locations, PBKDF2 use, and the first-server short-token rule.

Method: documentation only; no commands were run.
