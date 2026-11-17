---
id: computing-software.cybersecurity-defensive.pomerium.troubleshoot-upstream-errors
name: troubleshoot-upstream-errors
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [no-healthy-upstream, upstream-timeout, cors-troubleshooting, shared-secret, envoy-shared-memory]
level: practitioner
status: docs-checked
description: "Diagnose common Pomerium failures: upstream error codes, shared secret mismatch, certificate and gRPC errors, startup after a user change, and CORS 401s."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/troubleshooting.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Upstream errors**
- `no_healthy_upstream`: upstream unreachable; check its config, firewall, DNS and load-balancer health checks.
- `upstream_max_stream_duration_reached`: default timeout is 10 seconds; adjust per the Connections page.
- `upstream_per_try_timeout`, `upstream_response_timeout`, `upstream_reset_before/after_response_started`: review timeouts.
- `via_upstream`: the upstream set the code; read its logs.

**Core**
- Shared secret mismatch: `Unauthenticated` or invalid JWT logs; make the secret identical on all services, matching the Databroker.
- "certificate signed by unknown authority" between services: add the CA via the certificate authority setting or the system trust store.
- RPC DeadlineExceeded: Proxy cannot reach Authorize; use an internally routable URL because many cloud load balancers do not pass gRPC.
- Exit on startup after changing the run user: delete `/dev/shm/envoy_shared_memory_*` and `/tmp/pomerium-envoy-admin.sock`, then restart.
- Ingress errors: `kubectl describe ingress/<name>` events.
- CLI tools with Let's Encrypt: use `fullchain.pem`, not `cert.pem`.

**Enterprise directory sync**: raise Polling Min Delay above a full sync duration and Max Delay to about twice that.

**CORS 401 between `app.` and `api.` subdomains** (cookies are not sent cross-domain). Options: serve the API under a `prefix: /api` route on the app domain; set `cookie_http_only: false` and send `X-Pomerium-Authorization`; set `cookie_domain` to the parent domain with `credentials: 'include'` (not if some subdomains bypass Pomerium); or add `depends_on` for the API host. The API route may need `cors_allow_preflight: true`.

## Checked

2026-11-04. Confirmed against the Troubleshooting page: upstream error codes and the 10-second default, shared secret mismatch, unknown-authority and DeadlineExceeded fixes, shared memory and admin socket cleanup, ingress events, fullchain.pem, directory sync polling delays, and the four CORS options. Replaced the unconfirmed setting name certificates with the page's wording (certificate authority setting).

Method: documentation only; no commands were run.
