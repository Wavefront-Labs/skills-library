---
id: computing-software.cybersecurity-defensive.pomerium.reverse-tunnel-setup
name: reverse-tunnel-setup
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [reverse-tunnel, upstream-tunnel, ssh-policy-rego, reverse-port-forward, ssh-r]
level: advanced
status: docs-checked
description: "Expose a service that Pomerium cannot reach by having an authenticated SSH client register as the upstream via reverse port-forwarding."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/reverse-tunneling.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Any HTTP or SSH route can send upstream traffic through an authenticated SSH client. Pomerium does not connect to the upstream; clients connect to Pomerium and register as upstream endpoints while they stay authenticated.

Setup:
1. Complete native SSH setup steps 1-3 (SSH address, host keys, User CA key). SSH routes themselves are not required.
2. Enable the runtime flag:

```yaml
runtime_flags:
  ssh_upstream_tunnel: true
```

3. Add `upstream_tunnel` to the route. A second policy, `ssh_policy`, controls who may register as upstream. `ssh_policy_rego` goes inside `upstream_tunnel` and takes raw Rego policies:

```yaml
routes:
  - from: ssh://tunnel.example.com
    to: ssh://localhost:8080
    upstream_tunnel:
      ssh_policy_rego:
        - |
          allow := true
```

The `allow := true` policy always allows; replace it with a real policy.

Client: `ssh -R 0 pomerium.example.com`. Reverse tunneling works only when connecting without a route name (the internal CLI). Connecting to a route (`ssh -R ... route@pomerium`) sends port-forward requests to the upstream SSH server instead.

Compatible with HTTP and SSH routes; TLS, gRPC and other TCP protocols pass through. UDP is unsupported. See reverse-tunnel-r-syntax.

## Checked

2026-11-04. Read the Reverse Tunneling page: concept, setup steps 1-3, the ssh_upstream_tunnel runtime flag, ssh_policy and ssh_policy_rego nesting, client command, route-versus-internal-CLI rule and compatibility notes all confirmed. Nothing removed.

Method: documentation only; no commands were run.
