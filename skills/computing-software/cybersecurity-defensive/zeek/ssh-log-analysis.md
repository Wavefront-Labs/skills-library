---
id: computing-software.cybersecurity-defensive.zeek.ssh-log-analysis
name: ssh-log-analysis
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, ssh-log, lateral-movement, hassh, inbound-outbound]
level: practitioner
status: docs-checked
description: "Read Zeek ssh.log for lateral movement, failed logins, inbound versus outbound direction, and hassh client and server fingerprints."
sources: ["https://docs.zeek.org/en/current/reference/logs/ssh.html", "https://docs.zeek.org/en/current/frameworks/notice.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ssh.log analysis

Fields are documented in `SSH::Info`.

**Lateral movement**: a connection between systems on the same subnet or within one organisation. A successful entry shows the client (for example 192.168.4.142) logged into the server (192.168.4.1); the rest profiles the client, server and the encryption used. The `hassh` field (from the HASSH package) hashes the encryption algorithms the client offers; `hasshServer` does the same for the server. They are similar to JA3 and JA3S for TLS.

**Failed logins**: the page created failures by entering a wrong password and then pressing return twice. The resulting log lacks the entry a successful login produces, and the author notes one odd entry he cannot explain, with at least one authentication attempt having occurred. Do not assume failed attempts always appear cleanly.

**Direction**: Zeek decides whether an SSH login is inbound or outbound. An outbound example is a host on the 192.168.4.0/24 enterprise network logging into an Internet host. Analysts can use this to spot systems that should not initiate outside SSH.

Brute force detection is separate: the notice framework example loads `protocols/ssh/detect-bruteforcing` and raises `SSH::Password_Guessing`, tunable with `SSH::password_guesses_limit`.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
