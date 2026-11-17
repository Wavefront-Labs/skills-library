---
id: computing-software.cloud-infrastructure-engineering.docker.nsenter-and-tcpdump-into-container-namespaces
name: nsenter-and-tcpdump-into-container-namespaces
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, nsenter, nsenter-target, nsenter-net, tcpdump, packet-capture, network-troubleshooting, network-debugging]
level: advanced
description: "Use host tools inside a container's namespaces with nsenter -t PID -n/-m/-p and capture its traffic with tcpdump on the netns or the host veth, saving pcaps for Wireshark."
sources: ["https://man7.org/linux/man-pages/man1/nsenter.1.html", "https://docs.docker.com/engine/network/", "https://www.tcpdump.org/manpages/tcpdump.1.html"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nsenter and tcpdump into container namespaces

Works when the container has no tools at all, because the **host's** binaries run inside the
container's namespaces.

## Find the PID
```sh
PID=$(docker inspect -f '{{.State.Pid}}' app)
```

## nsenter
```sh
sudo nsenter -t $PID -n ip addr                  # network namespace only (host FS, host tools)
sudo nsenter -t $PID -n ss -ltnp                 # what is listening inside
sudo nsenter -t $PID -n curl -sv http://127.0.0.1:8080/
sudo nsenter -t $PID -m -u -i -n -p sh           # "become" the container (its FS - needs a shell in it)
sudo nsenter -t $PID -m cat /etc/resolv.conf     # read a file in the mount namespace
```
Namespace flags: `-m` mount, `-u` UTS, `-i` IPC, `-n` net, `-p` PID, `-U` user, `-C` cgroup;
`-a` all. `-n` alone is the sweet spot: container network view + full host toolset.
Rootless/userns containers: add `-U --preserve-credentials`.

## tcpdump inside the netns
```sh
sudo nsenter -t $PID -n tcpdump -i eth0 -nn 'port 5432'
sudo nsenter -t $PID -n tcpdump -i any -w /tmp/app.pcap -c 5000   # host path /tmp
```
Open `app.pcap` in Wireshark.

## tcpdump on the host side (veth / bridge)
```sh
# which veth belongs to the container
IFIDX=$(sudo nsenter -t $PID -n cat /sys/class/net/eth0/iflink)
VETH=$(grep -l "^$IFIDX$" /sys/class/net/veth*/ifindex | cut -d/ -f5)
sudo tcpdump -i $VETH -nn
sudo tcpdump -i docker0 -nn host 172.17.0.5      # whole default bridge
sudo tcpdump -i br-$(docker network inspect -f '{{.Id}}' mynet | cut -c1-12) -nn
```

## Without host access to tcpdump
Sidecar: `docker run --rm --net container:app nicolaka/netshoot tcpdump -i eth0 -w - > app.pcap`.

## Gotchas
- PID changes on restart; re-read it.
- Large captures fill disks fast - always `-c` or `-G/-W` rotation.

## Verify
`sudo nsenter -t $PID -n ip -br addr` matches `docker inspect` network IPs; pcap shows the
expected TCP handshake.

## Checked
2026-10-31. Confirmed in the nsenter man page: `-m -u -i -n -p -U -C -a` and `--preserve-credentials`. Removed: NAT-capture explanation, loopback remark and the env/cgroup claim (not on pages read). Shell one-liners are examples, not verified.
Method: documentation only; no commands were run.
