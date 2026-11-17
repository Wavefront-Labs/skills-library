---
id: computing-software.systems-network-administration.wireshark.windows-pktmon-and-container-capture
name: windows-pktmon-and-container-capture
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, pktmon, container-capture, docker, kubernetes, nsenter, etl2pcapng, windows-capture]
level: practitioner
status: verified
description: "Capture where Npcap/tcpdump are not installed: Windows pktmon to pcapng, and inside containers or Kubernetes pods via nsenter, docker netshoot or kubectl debug."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/pktmon/pktmon
  - https://github.com/nicolaka/netshoot
  - https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows pktmon and container captures

## Windows without installing anything (pktmon, in-box since Windows 10 build 19041/2004; also on Server 2019 and later)
```powershell
pktmon filter add -i 10.1.1.10 -p 443          # optional filters
pktmon start --capture --pkt-size 0 --file-name <TEMP_DIR>\cap.etl
# reproduce the issue
pktmon stop
pktmon etl2pcap <TEMP_DIR>\cap.etl --out <TEMP_DIR>\cap.pcapng
pktmon filter remove
```
All of these ran on Windows 11 (`-i` and `-p` are the documented IP and port filter options). `pktmon list` prints the
network adapters with their component IDs (`pktmon list --all` includes the rest of the stack).
- pktmon sees packets at several stack components (NIC, vSwitch, filter drivers), so the same packet appears many
  times: three UDP datagrams produced 18 records. Avoid it at capture time with `pktmon start --capture --comp nics`
  (3 records) or convert one layer with `etl2pcap --component-id <id>` (id 122, `tcpip.sys`, gave 3 records; id 58,
  the QoS packet scheduler, gave 6). The converted pcapng has a single interface named `unknown` and no per-packet
  comment, so you cannot separate components inside Wireshark.
- Packet drops are not converted by default; add `--drop-only` to see only drops.
- `--pkt-size 0` = full packets (default 128 bytes).
- Loopback traffic to 127.0.0.1 produced no pktmon records in my test; use Npcap's loopback adapter for that.
- Older systems: `netsh trace start capture=yes tracefile=<TEMP_DIR>\t.etl` (both options are in `netsh trace start help`),
  then convert with `etl2pcapng` (github.com/microsoft/etl2pcapng, repository exists).

## Docker container
Containers rarely have tcpdump. Join the container's network namespace from the host:
```bash
# <PID> = the container's main process ID as seen on the host (docker inspect shows it)
sudo nsenter -t <PID> -n tcpdump -i eth0 -w /tmp/web.pcap
# or a throwaway tools container sharing its namespace
docker run --rm --net container:web nicolaka/netshoot tcpdump -i eth0 -w - > web.pcap
```
`nsenter -t PID -n` enters the target process's network namespace (nsenter manual page); Docker's `--network
container:<name|id>` attaches a container to another container's network stack (Docker networking docs), and the
netshoot README uses `docker run -it --net container:<container_name> nicolaka/netshoot`. The commands are assembled from those documented options.
## Kubernetes pod
```bash
kubectl debug -it pod/web-7d9f --image=nicolaka/netshoot --target=web -- tcpdump -i eth0 -w /tmp/p.pcap
kubectl cp web-7d9f:/tmp/p.pcap ./p.pcap -c <debug-container-name>
```
Ephemeral containers are stable since Kubernetes v1.25 (kubernetes.io debug page) and are created through a dedicated
`ephemeralcontainers` API handler. `kubectl debug` has `-i`, `-t`, `--image`, `--target` and takes `-- COMMAND`, and
`kubectl cp` has `-c` (checked with kubectl 1.30.3 `--help`); the two commands above are
assembled from those documented options.

## Verify
- [ ] pcapng opens in Wireshark with the expected traffic, without duplicates (pktmon) or from the right namespace (containers).

## Checked
Run on Windows 11 with the in-box pktmon: `filter add -i/-p`, `start --capture --pkt-size 0 --file-name`, `stop`,
`etl2pcap --out`, `--component-id`, `--drop-only` and `--comp nics` all worked as described (UDP datagrams to 192.0.2.1:
18 records by default, 3 with `--comp nics`, 3 for component 122); `pktmon etl2pcap` reported 9 dropped, 0 converted
packets for traffic to a closed loopback port; `capinfos -I` showed one interface. Microsoft's pktmon page confirms
build 19041 and Server 2019. Docker, nsenter and Kubernetes flags were checked against the Docker, nsenter, Kubernetes and kubectl documentation.
