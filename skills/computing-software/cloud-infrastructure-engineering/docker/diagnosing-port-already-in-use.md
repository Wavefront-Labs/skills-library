---
id: computing-software.cloud-infrastructure-engineering.docker.diagnosing-port-already-in-use
name: diagnosing-port-already-in-use
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, port-conflict, address-in-use, port-already-allocated, port-publishing, winnat, excluded-port-range, ss, lsof, compose-ports]
level: practitioner
status: docs-checked
description: "Fix 'port is already allocated' and 'bind: address already in use' on Linux, macOS and Windows: find the owner, Hyper-V excluded ranges, stale docker-proxy, Compose port design."
sources: ["https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/topics/", "https://docs.docker.com/engine/network/port-publishing/", "https://docs.docker.com/reference/cli/docker/container/ls/", "https://man7.org/linux/man-pages/man8/ss.8.html", "https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/error-10013-wsaeacces-is-returned"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing "address already in use"

## Read the error: who owns the port?
| Message | Owner |
|---|---|
| `Bind for 0.0.0.0:8080 failed: port is already allocated` | Docker's Desktop troubleshooting page lists two causes for this and the "address is already in use" form: another application using the port, or a previous container not stopped properly and still bound |
| `listen tcp:0.0.0.0:8080: bind: address is already in use` | same two causes |
| Windows socket error 10013 (WSAEACCES) on bind | Microsoft documents this for excluded port ranges; see below |

## Another container
```bash
docker ps --filter publish=8080
```
The `publish` / `expose` filter shows containers that publish a given port (`<port>[/<proto>]`).
Common: an old Compose project with a different project name still running the same stack
(`docker compose ls`).

## A host process
```bash
sudo ss -ltnup 'sport = :8080'            # Linux: listening (-l), TCP (-t), UDP (-u), numeric (-n), process (-p)
```
Windows, per Docker's Desktop troubleshooting page: use `resmon.exe` (Network, Listening
Ports) or `netstat -aon | find /i "listening "` and read the PID in the rightmost column;
then stop that process or choose another port.

## Windows excluded port ranges
Nothing is listening, yet the bind is refused (WSAEACCES, error 10013):
```powershell
netsh interface ipv4 show excludedportrange protocol=tcp
```
Per Microsoft, use a port outside the default dynamic range (49,152 to 65,535) that is not
listed as excluded, or reserve your own port as excluded (admin):
```powershell
netsh int ipv4 add excludedportrange protocol=tcp startport=8080 numberofports=1
```

## Design Compose ports so clashes do not happen
```yaml
services:
  web:
    ports:
      - "127.0.0.1:${WEB_PORT:-8080}:80"   # per-developer override via .env
  db:
    ports:
      - "5432"                              # container port only; Docker picks the host port, see: docker compose port db 5432
```
- Do not publish ports that only other containers use; they talk over the network by
  service name.
- Bind to `127.0.0.1` on dev machines to keep the port off other interfaces (the port-publishing
  docs describe `-p 127.0.0.1:8080:80` for loopback-only publishing).
- Two clones of the same repo need different project names (`COMPOSE_PROJECT_NAME`) and ports.

## Verify
```bash
docker compose up -d && docker compose port web 80
ss -ltn | grep 8080
```

## Checked
Date: 2026-10-26. Documentation: docker/docs main (last commit 2026-10-23): Desktop troubleshooting topics, `docker ps` filters, port publishing; Microsoft support article on WSAEACCES and excluded ports; man7 ss(8). Confirmed: both error messages and causes, `publish` filter, ss options and `sport = :PORT` filter, netstat/resmon steps, excluded-port-range command, default dynamic range, loopback publishing. Removed as unconfirmed: the mapping of each message to a distinct owner, lsof and PowerShell Get-NetTCPConnection lines, AirPlay ports, dual-stack and leftover docker-proxy claims, `net stop winnat`, `netsh ... set dynamic` command.
Method: documentation only; no commands were run.
