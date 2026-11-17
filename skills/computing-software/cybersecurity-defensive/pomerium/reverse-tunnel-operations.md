---
id: computing-software.cybersecurity-defensive.pomerium.reverse-tunnel-operations
name: reverse-tunnel-operations
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [tunnel-tui, systemd-user-service, tunnel-high-availability, tunnel-health-checks, ssh-n]
level: advanced
status: docs-checked
description: "Operate Pomerium reverse tunnels: read the status TUI, run the client as a systemd user service, and use health checks and multiple clients for availability."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/reverse-tunneling.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**TUI panels** (shown when interactive, `-R` set and no command; `-N` disables it): Active Connections (route, downstream IP, Rx/Tx bytes, duration); Client Requests (how each `-R` was parsed; dynamic ports show as `D` plus a random number); Port Forward Status (`ACTIVE` or `INACTIVE`, health `HEALTHY`, `DEGRADED`, `UNHEALTHY` when health checks are on); Logs.

**Availability**
- Envoy health checks are routed through the tunnel so it can fail fast.
- Several clients can register for the same route and Envoy load-balances across them.
- Multiple `to` addresses balance across upstreams through connected clients (dynamic forwarding only); both can combine.

**Run as a service** (`~/.config/systemd/user/reverse-tunnel-client.service`):

```
[Unit]
Description=Pomerium SSH Reverse Tunnel Client

[Service]
Type=forking
ExecStart=/usr/bin/ssh -vyfN -R 0 pomerium.example.com
Restart=on-failure
TimeoutSec=60s
```

`-v` verbose, `-y` log to syslog, `-f` fork after authentication (signals readiness for `Type=forking`), `-N` no command.

**Login**: without an active session the service waits. Get the sign-in URL from the journal, or run `ssh pomerium.example.com -- whoami` and sign in; the service then authenticates automatically.

Health check traffic makes debug logs noisy. OpenSSH escape sequences (`man 1 ssh`) can change forwards without restart.

## Checked

2026-11-04. Read the Reverse Tunneling page: TUI panels and columns, health checks through the tunnel, multi-client load balancing, the systemd unit and flag meanings, login behaviour and escape commands all confirmed. Nothing removed.

Method: documentation only; no commands were run.
