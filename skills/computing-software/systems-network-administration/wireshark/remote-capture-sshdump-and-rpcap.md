---
id: computing-software.systems-network-administration.wireshark.remote-capture-sshdump-and-rpcap
name: remote-capture-sshdump-and-rpcap
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, sshdump, rpcapd, remote-capture, extcap, tcpdump-over-ssh, ciscodump]
level: practitioner
status: verified
description: "Capture on a remote host into local Wireshark with sshdump or a tcpdump-over-SSH pipe, or rpcapd on Windows, while excluding your own SSH session."
sources:
  - https://www.wireshark.org/docs/man-pages/sshdump.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Remote capture (sshdump, pipes, rpcap)

## SSH pipe (works everywhere)
```bash
ssh admin@server 'sudo tcpdump -i eth0 -U -s0 -w - "not port 22"' | wireshark -k -i -
```
- `-U` writes each packet out as it is saved (tcpdump manual) so Wireshark updates live; `-w -` writes to standard
  output.
- `not port 22` keeps your own SSH stream out (otherwise each captured packet generates more
  SSH traffic which is captured again: a feedback loop).
- sudo must not prompt: use a sudoers rule for tcpdump only, or capabilities.
Windows client: `ssh ... | "<WIRESHARK_DIR>\Wireshark.exe" -k -i -` (`-i -` reads a capture from standard input, `-k` starts capturing at once; per the wireshark manual page).

## sshdump (extcap built into Wireshark)
In the interface list choose **SSH remote capture**, set host, user, key, remote interface
and capture filter. CLI equivalent:
```bash
sshdump --extcap-interface sshdump --remote-host server --remote-username admin \
  --sshkey ~/.ssh/id_ed25519 --remote-interface eth0 --remote-capture-command-select tcpdump \
  --remote-filter "not port 22" --fifo /tmp/remote.pcap --capture
```
Every option above is documented in the sshdump manual page; the CLI form above is assembled from those options (the Windows install's
extcap folder holds only `etwdump`). Only OpenSSH-format private keys are supported
for `--sshkey`; `--remote-password` is stored in plain text and visible to other users, so prefer keys with an agent.
The default remote filter in the dialog is `not ((host myhost) and port 22)`. `--remote-capture-command-select` takes
`dumpcap`, `tcpdump` or `other` (with `--remote-capture-command`). `ciscodump` does the same against IOS/IOS-XE and ASA
devices using Cisco EPC; `udpdump` is a UDP receiver for exported datagrams (for example from Aruba routers).

## rpcapd (Windows/legacy)
The Npcap install here has no `rpcapd.exe`; run a current libpcap rpcapd build on the remote host
(`rpcapd -n -p 2002`: `-n` permits NULL authentication, `-p` sets the control port; lab only) and in Wireshark add a
remote interface `rpcap://host:2002/`. The rpcapd manual page now lists TLS options (`-S` require TLS, `-K` key file,
`-X` certificate file); without them traffic and credentials are unprotected, so prefer SSH.

## Bandwidth
Remote capture sends every captured byte back over the network. Use a tight capture filter
and snaplen (`-s 128`) on busy servers, or capture to a file remotely and copy it.

## Verify
- [ ] Live packets arrive from the remote host, none of them from your own SSH session.

## Checked
Option names, defaults and descriptions for sshdump, ciscodump and udpdump were read from the Wireshark manual pages on
wireshark.org (`sshdump`: `--remote-host`, `--remote-username`, `--sshkey`, `--remote-interface`,
`--remote-capture-command-select`, `--remote-filter`, `--fifo`, `--capture`); rpcapd `-n`, `-p`, `-S`, `-K`, `-X` from the
tcpdump.org manual page; tcpdump `-U` and `-w -` from the tcpdump manual page; Wireshark `-k` and `-i -` from the
`wireshark` manual page shipped with the install. A directory listing showed the Windows install has no `sshdump` or
`rpcapd`, the flags are checked against the manual pages.
