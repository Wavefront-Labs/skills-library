---
id: computing-software.cloud-infrastructure-engineering.etcd.auth-tokens-and-jwt
name: auth-tokens-and-jwt
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [auth-token, jwt, simple-token, token-ttl, bcrypt-cost, authentication, auth-design]
level: advanced
status: docs-checked
description: "Choose and configure authentication tokens: simple vs jwt, --auth-token-ttl, --bcrypt-cost and how clients present them."
sources:
  - "https://etcd.io/docs/v3.5/learning/design-auth-v3/"
  - "https://etcd.io/docs/v3.5/op-guide/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

v3 authentication is per connection, not per request. A client first creates a gRPC connection only to authenticate with a user ID and password (`Authenticate` RPC); the reply is a token on success or an error. That connection cannot carry the new token (gRPC cannot add per-RPC credentials after the connection is created), so the client opens a new connection and associates the token with it, for example with `grpc.WithPerRPCCredentials()`.

Token types are set with `--auth-token` in the form `type,var1=val1,var2=val2,...` (default `simple`):

- `simple`: not cryptographically signed, and servers must statefully track the token-user correspondence. The design page says it is not designed for production and is meant for development testing. Known issue: simple tokens are resolved without a linearizable check, so a member may return an "invalid auth token" error if it has not finished processing a previous authentication; the suggested workaround is a client retry.
- `jwt`: cryptographically signed and verified, stateless (the token carries metadata such as username and revision). The design page says to use JWT for production. Variables: `sign-method` (ES256, ES384, ES512, HS256, HS384, HS512, RS256, RS384, RS512, PS256, PS384 or PS512), `pub-key` (path to the public key that verifies tokens), `priv-key` (path to the private key that signs them) and `ttl` (token TTL).

Related flags: `--auth-token-ttl` (default 300) is the time in seconds of the auth token TTL. `--bcrypt-cost` (default 10) is the cost/strength of the bcrypt algorithm that hashes auth passwords; valid values are between 4 and 31.

Why `Authenticate` is costly: bcrypt checking is computationally expensive by design, nearly 100ms on an ordinary x64 server. Doing it in the state machine apply phase would limit the cluster to almost 10 `Authenticate` requests per second, so v3 checks passwords in the API layer, parallelised outside Raft, and retries if the auth store revision changed during the check.

Design notes: auth metadata is stored in Raft-managed storage like other etcd data, and each request is permission checked in the apply phase of the state machine against the latest auth store revision. Permissions are granted on an exact key or a key range, so permission on a nonexistent key can be granted.

Applications may also set a pre-signed JWT directly on the client, without calling `Authenticate`. The server validates the signature with its configured public key and grants access based on the username in the token. Updating the token requires creating a new client. The `AuthStatus` RPC lets a client learn whether auth is enabled and the current `authRevision` even without a valid token.

## Checked

2026-11-08. Read in full: etcd v3 authentication design page and v3.5 Configuration options page. Confirmed token types and caveats, the --auth-token variables and sign methods, the --auth-token-ttl and --bcrypt-cost defaults and range, bcrypt cost figures, the direct-JWT flow and AuthStatus. Removed: the gRPC metadata key name, simple-token refresh-on-use and restart/member-specific claims, the example ttl value, the error message string for stale auth revisions, the interval-tree claim, the cache-tokens advice and the key-rotation advice (not on the pages read).
Method: documentation only; no commands were run.
