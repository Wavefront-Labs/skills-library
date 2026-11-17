---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.ssh-metadata-analysis-with-hassh
name: ssh-metadata-analysis-with-hassh
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [hassh, ssh-forensics, encrypted-traffic-analysis, zeek, dfir]
level: advanced
status: draft
description: "Analyse SSH sessions without decryption: HASSH client/server fingerprints, version banners, Zeek ssh.log auth inference, packet-size patterns and brute force."
sources: ["https://github.com/salesforce/hassh", "https://docs.zeek.org/en/master/logs/ssh.html", "https://datatracker.ietf.org/doc/html/rfc4253"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SSH metadata analysis with HASSH

**Goal:** SSH is encrypted, but the key exchange is not. Fingerprint clients/servers, infer
authentication success, and spot tooling, tunnelling and brute force.

## What is visible
- Version banners: `SSH-2.0-OpenSSH_9.6p1 Ubuntu`, `SSH-2.0-libssh2_1.10.0`, `SSH-2.0-paramiko_3.4.0`, `SSH-2.0-Go`.
- `SSH_MSG_KEXINIT` algorithm lists (kex, encryption, MAC, compression) from both sides.

## HASSH
- **HASSH** = MD5 of the client's `kex;encryption;mac;compression` algorithm lists; **HASSHServer** for the server.
- Distinct libraries/tools produce distinct HASSHes even with spoofed banners (e.g. Go-based scanners, Paramiko, Metasploit modules, specific malware).
- Available in Zeek (package `hassh`), Suricata (`ssh.hassh` keyword), and Wireshark fields (`ssh.kex.hassh`, `ssh.kex.hasshserver`).
```text
Wireshark: ssh.kex.hassh == "ec7378c1a92f5a8dde7e8b7a1ddf33d1"
```

## Zeek ssh.log
- `auth_success` (heuristic T/F), `auth_attempts`, `client`, `server` banners, `direction`, `host_key` fingerprint, `hassh`.
- Brute force: many connections from one source with `auth_success=F`, short durations; Zeek notice `SSH::Password_Guessing`.
- Successful login after failures from the same source = likely compromise.

## Behaviour inference
- Interactive vs automated: interactive sessions show many small packets with human timing; file transfers show sustained large packets.
- Tunnelling/port forwarding: long sessions with traffic volume and patterns unlike shell use.
- Host key change for a known server = possible MITM or rebuilt server.

## Gotchas
- `auth_success` is inferred from packet sizes and can be wrong; confirm with server auth logs.
- Common OpenSSH client HASSHes are shared by millions of hosts; HASSH is most useful for rarer tools.

## Verify
Pair network-derived SSH events with sshd logs (`Accepted`/`Failed`) for the same source and time.
