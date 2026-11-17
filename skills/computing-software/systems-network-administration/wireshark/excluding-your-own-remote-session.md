---
id: computing-software.systems-network-administration.wireshark.excluding-your-own-remote-session
name: excluding-your-own-remote-session
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, exclude-ssh-session, capture-filter, rdp, ssh, bpf, feedback-loop]
level: practitioner
status: verified
description: "Build capture filters that keep your own SSH or RDP management session out of a capture on a remote box, using SSH_CONNECTION and Wireshark's auto-filter."
sources:
  - https://wiki.wireshark.org/CaptureFilters
  - https://www.tcpdump.org/manpages/pcap-filter.7.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Excluding your own remote session

Capturing on a box you are logged into remotely puts your own session in the capture. Each
packet displayed (tcpdump to the terminal) creates more SSH packets: a loop that floods the
capture and the link.

## SSH: exclude exactly your connection
`$SSH_CONNECTION` holds `client_ip client_port server_ip server_port`:
```bash
set -- $SSH_CONNECTION
sudo tcpdump -i eth0 -w cap.pcap "not (host $1 and port $2 and port $4)"
```
This keeps other SSH traffic (which may be what you are debugging) and drops only yours.
Lazy version when you do not need any SSH: `not port 22`.

## RDP on Windows
```
not (host <your_client_ip> and tcp port 3389)
```
Wireshark's own pre-fill for a Windows remote session is `not port 3389`, which covers both TCP and UDP.

## Wireshark does it for you
Wireshark, TShark and rawshark 4.4.1 contain templates that read `SSH_CONNECTION`, `SSH_CLIENT`, `REMOTEHOST` and
`DISPLAY` and pre-fill the capture filter for remote sessions (Capture Options shows it): `not (tcp port %s and host %s
and tcp port %s and host %s)` for `SSH_CONNECTION`, `not (tcp port %s and host %s and tcp port %s)` for `SSH_CLIENT`,
`not host %s` for `REMOTEHOST`, and `not port 3389` for a Windows remote-desktop session (found in the binaries with a
strings search; there is no `SESSIONNAME` string in them). Check the filter is
there rather than assuming.

## Pipelines
For `ssh host tcpdump -w - | wireshark -k -i -` the capture on the remote host must exclude
the same SSH connection carrying the pipe, or every captured packet is sent back over it.

## Verify
- [ ] Capture contains no packets of your own session (`tcp.port == <your client port>` empty)
      while other traffic is present.

## Checked
Run on Windows with Wireshark 4.4.1: with `SSH_CONNECTION="192.0.2.10 54321 10.0.0.5 22"`, `set -- $SSH_CONNECTION` gave
`not (host 192.0.2.10 and port 54321 and port 22)` and `dumpcap -d -f` compiled it (22 BPF instructions); the RDP filter
and `not port 22` also compiled. The filter templates and variable names come from reading the
shipped `wireshark.exe`/`tshark.exe` binaries. The tcpdump flags (`-i`, `-w`) are from its manual page, and the filter
syntax is the libpcap syntax that `dumpcap -d` compiled.
