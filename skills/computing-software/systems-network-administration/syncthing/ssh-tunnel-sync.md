---
id: computing-software.systems-network-administration.syncthing.ssh-tunnel-sync
name: ssh-tunnel-sync
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, ssh-tunnel, port-forward, tunneling]
level: advanced
status: docs-checked
description: "Tunnel Syncthing sync traffic between two hosts over SSH with local and remote forwards and fixed tcp:// addresses."
sources: ["https://docs.syncthing.net/users/tunneling.html", "https://docs.syncthing.net/users/firewall.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Syncing through an SSH tunnel

## Tunnel
Only 22/TCP needs to be open from hosta to hostb. From hosta, open one SSH session that forwards port 22001 on each machine to 22000 on the other:

```sh
ssh -i /path/to/key.pem \
  -L 127.0.0.1:22001:127.0.0.1:22000 \
  -R 127.0.0.1:22001:127.0.0.1:22000 \
  syncguy@hostb
```
Using 127.0.0.1 explicitly keeps both tunnel and Syncthing off external interfaces. The SSH server must allow port forwarding.

## Syncthing side (both hosts)
In Settings > Connections, untick NAT traversal, local discovery, global discovery and relaying. Set the Sync Protocol Listen Address to:

```
tcp://127.0.0.1:22000
```
Then add the remote device and, under Edit > Advanced, set its Addresses to:

```
tcp://127.0.0.1:22001
```
Do the same on both sides so each reaches the other through its local 22001.

## Troubleshooting
Run `sudo netstat -tupna | grep 2200` on both hosts. Expect Syncthing listening on 127.0.0.1:22000, ssh listening on 127.0.0.1:22001, and established connections between the two.

Common faults are SSH client or server misconfiguration, wrong key permissions, SELinux policy, and a firewall blocking port 22. To re-establish the tunnel after a reboot or failure, the page suggests autossh.

## Checked

2026-11-09. Confirmed against the Syncthing SSH Tunneling page (users/tunneling, raw rst from syncthing/docs); the Firewall Setup page (users/firewall) was read for the default ports 22000/TCP, 22000/UDP and 21027/UDP. Confirmed: the ssh -L/-R command, 127.0.0.1 rationale, port-forwarding requirement, Connections settings to untick, listen address, per-device Addresses value, netstat check and expected output, common faults. Removed: nothing; added the 22/TCP-only note and the autossh suggestion from the page.

Method: documentation only; no commands were run.
