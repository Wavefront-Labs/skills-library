---
id: computing-software.systems-network-administration.netbird.ssh-troubleshooting
name: ssh-troubleshooting
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, netbird-ssh, ssh-troubleshooting, permission-denied, sftp-unavailable]
level: practitioner
status: docs-checked
description: "Diagnose NetBird SSH failures: permission denied, server not detected, timeouts, SFTP unavailable and not-authorized errors, with the checks the docs recommend."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/peers/ssh.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Match the symptom to the documented check.

- Permission denied or server not detected: confirm the target runs with `--allow-server-ssh`, that SSH is enabled in the Dashboard, and that the peer is online.
- Connection timeout: check the access policy (ACL) allows the source group to the destination, and run `netbird status -d` to see peer state.
- SFTP unavailable: restart the server with `--enable-ssh-sftp`.
- Not authorized: verify the user's group is in the policy's source groups and is mapped to the requested OS user (Limited Access mode).
- JWT validation fails: the server's clock must be synchronized with the IdP.
- Everything broke after a server upgrade to v0.61.0: peers older than v0.61.0 lose SSH; update SSH servers first, then clients, then management and dashboard.
- Port forwarding refused: the server needs `--enable-ssh-local-port-forwarding` and/or `--enable-ssh-remote-port-forwarding`; forwarding works only through `netbird ssh`, not on Windows servers, and only as the user running NetBird.
- Cannot bind to port: the local port (local forwarding) or remote port (remote forwarding) is already in use or unavailable.

Quick sequence:
```
netbird status -d
netbird ssh user@<peer-ip>
```

## Checked

2026-11-04: read the SSH Access page troubleshooting, limitations and version history sections. Confirmed each symptom and check. Added the forwarding flags and bind errors from the page; removed the debug bundle advice, which the SSH page does not give.

Method: documentation only; no commands were run.
