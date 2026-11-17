---
id: computing-software.systems-network-administration.linux.namespaces-from-first-principles
name: namespaces-from-first-principles
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, namespaces, unshare, nsenter, ip-netns, pid-namespace, net-namespace, mount-namespace, uts-namespace, user-namespace, cgroup-namespace, containers, isolation, veth, sysadmin]
level: advanced
status: docs-checked
description: "Build container-style isolation by hand with unshare/nsenter/ip netns — what each of the 7 namespace types isolates and its gotchas."
sources:
  - https://man7.org/linux/man-pages/man7/namespaces.7.html
  - https://man7.org/linux/man-pages/man1/unshare.1.html
  - https://github.com/util-linux/util-linux/blob/master/sys-utils/unshare.1.adoc
  - https://github.com/util-linux/util-linux/blob/master/sys-utils/nsenter.1.adoc
  - https://github.com/iproute2/iproute2/blob/main/man/man8/ip-netns.8
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux namespaces from first principles — what Docker is standing on

**Goal:** understand container isolation as kernel primitives, not Docker
magic — create namespaces by hand, connect a network namespace to the host,
and know exactly what each namespace type does and doesn't isolate, which is
what actually explains most "why can my container see/do that" questions.

## 1. The namespace types
| Type | Isolates | Common surprise |
|---|---|---|
| `pid` | Process IDs (own PID 1) | Processes outside are invisible from in, but processes inside ARE visible from the host's root PID namespace with different PIDs. |
| `net` | Interfaces, routes, iptables/nftables, ports | Starts with *only* loopback — no interface means no network until you wire one up. |
| `mnt` | Mount points | Shares the underlying filesystem; a bind-mount into the namespace is how containers get their rootfs. |
| `uts` | Hostname, NIS domain | Cheapest one — just `hostname` isolation. |
| `ipc` | SysV IPC, POSIX message queues/semaphores | Rarely the thing biting you, but Docker isolates it by default. |
| `user` | UID/GID mapping | Root (UID 0) inside can map to an unprivileged UID outside — the real mechanism behind "rootless containers." |
| `cgroup` | Which cgroup subtree a process sees as "root" | Cosmetic/views-only; actual resource limits come from the cgroup controllers themselves, not this namespace. |
| `time` | Offsets of `CLOCK_MONOTONIC` and `CLOCK_BOOTTIME` | `unshare --time --boottime <secs>` sets the boot-time offset. |

## 2. Build one by hand with `unshare`
```bash
# New PID + mount + UTS namespace, with a new /proc mount so `ps` only shows this namespace
unshare --pid --mount --uts --fork --mount-proc /bin/bash
hostname sandbox              # only visible inside
ps aux                        # only this namespace's processes — because /proc was remounted
```
`--mount-proc` mounts a fresh proc filesystem (default at `/proc`) just before the program
runs and implies a new mount namespace; without it `/proc` still shows the old PID
namespace's processes. `--fork` is needed so the program runs as PID 1 of the new PID namespace.

## 3. Network namespaces — the one you'll hand-build most
```bash
ip netns add webapp
ip netns exec webapp ip link set lo up      # namespaces start with loopback only, nothing else

# connect it to the host with a veth pair
ip link add veth-host type veth peer name veth-ns
ip link set veth-ns netns webapp
ip addr add 10.200.0.1/24 dev veth-host
ip link set veth-host up
ip netns exec webapp ip addr add 10.200.0.2/24 dev veth-ns
ip netns exec webapp ip link set veth-ns up
ip netns exec webapp ip route add default via 10.200.0.1

# host side: allow forwarding + NAT so the namespace can reach the internet
sysctl -w net.ipv4.ip_forward=1
# then add a masquerade rule for 10.200.0.0/24 with your firewall tool (nftables or iptables)
```
A veth pair plus NAT is the building block of bridge-style container networking; building it by hand once makes that clearer.

```bash
ip netns exec webapp curl -s https://example.com    # run anything inside the namespace
nsenter --net=/var/run/netns/webapp -- bash          # or attach an interactive shell to it
```

## 4. `nsenter` — entering a running process's namespaces
```bash
PID=$(docker inspect -f '{{.State.Pid}}' mycontainer)
nsenter -t $PID -n -m -u -p -i bash     # join its net, mount, uts, pid, ipc namespaces
```
This is the escape hatch when a container's own tools are too minimal to debug from
inside (no shell, no `ip`, distroless image) — enter its namespaces from the
host where full tooling is available.

## 5. User namespaces — the rootless piece
```bash
unshare --user --map-root-user --mount --pid --fork bash
id    # uid=0(root) inside ...
# ... but on the host, `ps -eo pid,user` for this process shows the real unprivileged UID
```
A user namespace is the kernel mechanism rootless container tools build on: a process can be root *inside* its namespace (so apt/chown/etc
work normally) while being mapped to a harmless UID outside, limiting the
blast radius of a container escape. `/etc/subuid` and `/etc/subgid` define
the UID/GID ranges a user is allowed to map.

## Gotchas
- Namespaces alone give isolation, **not resource limits** — a process in an
  isolated PID/net/mnt namespace can still consume unlimited CPU/memory/IO
  unless paired with cgroups (see
  `computing-software.systems-network-administration.linux.cgroups-from-first-principles`).
  Container runtimes always combine both; namespaces by themselves are not a
  security boundary against resource exhaustion.
- A mount namespace does not isolate the filesystem *content* unless you
  also give it its own rootfs (chroot/pivot_root) — `unshare --mount` alone
  still sees the host's files, just can mount/unmount independently of it.
- Deleting the process that created a namespace doesn't always delete the
  namespace: `ip netns` namespaces are pinned by a bind-mount under
  `/var/run/netns/` and persist until explicitly `ip netns delete`d, even
  with zero processes left inside — a common source of "phantom" leftover
  namespaces on long-lived hosts.
- User namespace UID mapping interacts badly with bind-mounted host paths
  that use real host UIDs — files owned by host UID 1000 can appear owned
  by `nobody` or a totally different user inside a user-namespaced container
  depending on the mapping range.

## Verify
- [ ] `lsns` lists the namespace, its type, and the PID that owns/uses it — confirms it actually exists and who's in it.
- [ ] A network namespace has loopback up and, if intended, a working default route out through a veth pair (`ip netns exec <ns> ping -c1 <gateway>`).
- [ ] `unshare --pid --mount-proc` namespaces show only their own processes in `ps`, not the host's.
- [ ] `ip netns delete` / exiting the unshared shell actually removes the namespace (`lsns` no longer lists it) — no orphaned namespace left behind.

## Checked

Checked against the util-linux `unshare(1)` and `nsenter(1)` man sources and the Linux kernel documentation tree (namespaces compatibility list) on 2026-10-26. Confirmed: `unshare` options `--pid`, `--mount`, `--uts`, `--ipc`, `--net`, `--user`, `--cgroup`, `--time`, `--fork`, `--mount-proc` (default `/proc`, implies a mount namespace), `--map-root-user`, `--boottime`; the time namespace as an eighth type (the old text said seven); `/etc/subuid` as the mapping source for `--map-users`. `ip netns` add/exec/delete and named namespaces bind-mounted under the netns run directory, `nsenter -t/-n/-i` (iproute2 and util-linux man sources). Fixed: the NAT line no longer assumes a pre-existing nft table. Removed: claims about Docker or `kubectl exec` internals.

Method: documentation only; no commands were run.
