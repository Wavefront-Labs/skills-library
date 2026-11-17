---
id: computing-software.cybersecurity-defensive.pomerium.ssh-jump-host-mode
name: ssh-jump-host-mode
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [jump-host, proxyjump, direct-tcpip, runtime-flags, ssh-upstream-tunnel]
level: advanced
status: docs-checked
description: "Enable Pomerium's SSH jump-host mode with the ssh_allow_direct_tcpip runtime flag and understand which policy criteria still apply."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/native-ssh-access.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In jump-host mode Pomerium acts as a virtual jump host: the client authenticates to Pomerium, then connects directly to the upstream, which authenticates the user itself (ProxyJump support).

- Disabled by default; enable with the runtime flag `ssh_allow_direct_tcpip`.
- Upstream servers do not need to trust Pomerium's User CA.
- Policy still applies, except `ssh_username`, `ssh_username_matches_claim` and `ssh_username_matches_email`, which do not apply. `ssh_publickey` and `ssh_ca` still apply.

Runtime flags for SSH:
- `ssh_routes_portal`: lets users pick a destination when SSHing to Pomerium without a route.
- `ssh_allow_direct_tcpip`: jump-host mode.
- `ssh_upstream_tunnel`: enables the `upstream_tunnel` route option (reverse tunneling).

See the Pomerium Runtime Flags reference for how to set them.

## Checked

2026-11-04. Read the Native SSH Access page: jump-host behaviour, exempt criteria, the three SSH runtime flags and the disabled-by-default note all confirmed. Removed the config.yaml example and an unsourced closing remark; the page only links to the Runtime Flags reference.

Method: documentation only; no commands were run.
