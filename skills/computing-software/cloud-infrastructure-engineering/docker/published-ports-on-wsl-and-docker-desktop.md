---
id: computing-software.cloud-infrastructure-engineering.docker.published-ports-on-wsl-and-docker-desktop
name: published-ports-on-wsl-and-docker-desktop
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, port-publishing, wsl-port-forwarding, wsl2, docker-desktop, localhost-forwarding, windows]
level: practitioner
status: docs-checked
description: "Reach published container ports on Windows: Docker Desktop vs dockerd in a WSL distro, localhostForwarding, mirrored networking, portproxy and Hyper-V firewall."
sources: ["https://learn.microsoft.com/en-us/windows/wsl/networking", "https://learn.microsoft.com/en-us/windows/wsl/wsl-config", "https://docs.docker.com/desktop/features/networking/", "https://docs.docker.com/desktop/settings-and-maintenance/settings/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Published ports on WSL and Docker Desktop

Two different setups behave differently.

## A. Docker Desktop
Desktop's backend process listens on the host port you publish and forwards connections
into the VM over a shared-memory channel. By default `docker run -p` listens on all host
interfaces (`0.0.0.0`); you can restrict it (`-p 127.0.0.1:8080:80`), and a Desktop network
setting can make binding default to localhost.
```bash
docker run -d -p 8080:80 nginx
```
Open `http://localhost:8080`. Outbound container traffic and inbound published ports all go
through the `com.docker.backend` process, so host firewall or endpoint-security rules should
target that process.

## B. Docker Engine installed inside a WSL distro (no Desktop)
Ports bound in the WSL 2 VM reach Windows through WSL localhost forwarding:
```ini
# %UserProfile%\.wslconfig
[wsl2]
localhostForwarding=true          # default true: wildcard/localhost ports reachable via localhost:port
networkingMode=mirrored           # Windows 11 22H2 or later
```
`localhostForwarding` is ignored when `networkingMode=mirrored`. Run `wsl --shutdown` after
editing `.wslconfig`.

In NAT mode, connections from other machines do not reach the distro directly. Microsoft's
documented workaround is a port proxy (the VM address comes from `wsl hostname -I`, and the
app must listen on `0.0.0.0`, not `127.0.0.1`):
```powershell
netsh interface portproxy add v4tov4 listenport=4000 listenaddress=0.0.0.0 connectport=4000 connectaddress=<address from wsl hostname -I>
```
Mirrored mode avoids this. For inbound LAN connections to a mirrored distro, the Hyper-V
firewall may need an allow rule:
```powershell
Set-NetFirewallHyperVVMSetting -Name '{40E0AC32-46A5-438A-A0B2-2B479E8F2E90}' -DefaultInboundAction Allow
```
On Windows 11 22H2+ with WSL 2.0.9+ the Hyper-V firewall is on by default, and the
`.wslconfig` key `firewall` (default true) lets Windows Firewall rules filter WSL traffic.

## Troubleshooting
| Symptom | Check |
|---|---|
| Works in WSL, not in the Windows browser | `localhostForwarding`, IPv4 vs IPv6 (`127.0.0.1` vs `localhost`), service bound to loopback inside the container |
| "port already allocated" on Windows | another process owns the port; see the port-conflict skill |
| LAN clients cannot connect | publish on `0.0.0.0`, then host firewall rule for `com.docker.backend` (Desktop) or portproxy/Hyper-V firewall (WSL engine) |

## Gotchas
- Docker Desktop's WSL integration and a separate dockerd in the same distro make `docker`
  ambiguous; pick one.

## Checked
Date: 2026-10-26. Documentation: MicrosoftDocs/WSL networking and wsl-config pages; docker/docs main
(2026-10-23) Desktop networking page. Confirmed: publish and bind behaviour,
`com.docker.backend`, `localhostForwarding` default and mirrored interaction, mirrored needs
Windows 11 22H2, `firewall` key default, portproxy form, `hostname -I`, Hyper-V firewall
command and default. Removed as unconfirmed: the excluded-port-range `netsh` check,
`New-NetFirewallRule` example, "random ports fail after reboot" row.
Method: documentation only; no commands were run.
