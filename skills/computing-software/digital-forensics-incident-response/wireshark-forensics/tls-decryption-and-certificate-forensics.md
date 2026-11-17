---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.tls-decryption-and-certificate-forensics
name: tls-decryption-and-certificate-forensics
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [tls-decryption, sslkeylogfile, wireshark, tshark, rsa-private-key, certificate-forensics, cert-transparency, self-signed-certificate, ja3, ja4, tls-fingerprinting, man-in-the-middle, man-in-the-middle-proxy, mitmproxy, dfir, network-forensics, rsa-key-decryption]
level: advanced
status: docs-checked
description: "Decrypt TLS traffic in Wireshark with an SSLKEYLOGFILE or RSA private key, and read certificate chains/SNI/self-signed certs for phishing and C2 infrastructure clues."
sources: ["https://wiki.wireshark.org/TLS", "https://www.ietf.org/archive/id/draft-ietf-tls-keylogfile-00.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# TLS decryption and certificate forensics

**Goal:** the baseline pcap-triage skill
(computing-software.digital-forensics-incident-response.wireshark-forensics.pcap-triage-and-session-reconstruction)
pulls JA3/JA4 fingerprints and SNI from *encrypted* TLS metadata; this skill covers
actually decrypting the payload when the keys exist, and reading what's left in the
certificate itself when they don't.

## 1. Decrypting with SSLKEYLOGFILE
If the traffic was captured **with logging enabled at capture time** (or can be
reproduced), setting the `SSLKEYLOGFILE` environment variable before launching a
browser/client causes it to write per-session TLS secrets to a file as connections
happen:
```
export SSLKEYLOGFILE=/path/to/keylog.txt      # set before launching the client
```
In Wireshark: Edit → Preferences → Protocols → TLS → "(Pre)-Master-Secret log
filename" (`tls.keylog_file`) → point at that file. A key log file works even when a
Diffie-Hellman key exchange is in use, whereas an RSA private key only works in a limited
number of cases (and not for TLS 1.3). Firefox, Chrome and curl honour the variable; Safari
and Edge did not at the time the Wireshark wiki was written (their TLS libraries lack the
mechanism), and OpenSSL 3.4 and later reads it directly. **The keylog file must have been captured during/alongside the pcap** — if
the traffic is historical and no keylog was saved at the time, this path is closed;
check whether the environment this traffic came from (malware sandbox, a monitored
endpoint) was already configured to log keys before assuming decryption is possible.

## 2. Decrypting with the server's RSA private key (SSLv3 and TLS 1.0-1.2, RSA key exchange only)
If you have the server's private key (your own infrastructure, or a key seized during
a lawful acquisition), Wireshark can decrypt sessions that used RSA key exchange:
Edit → Preferences → RSA Keys (Wireshark 3.0 and later), then "Add new keyfile..."
(the older TLS "RSA keys list" dialog is deprecated and its IP and port fields are unused).
This **does not work** if the cipher suite used (EC)DHE for key exchange —
which is the overwhelming majority of modern TLS traffic, by design, specifically to
provide forward secrecy and defeat exactly this kind of after-the-fact decryption with
a long-lived private key. Check the negotiated cipher suite in the Client/Server
Hello before spending time trying this path; a quick look at Wireshark's own
decrypted-or-not indicator avoids wasted effort.

## 3. Man-in-the-middle capture as an alternative
When neither of the above applies and decryption is still needed (e.g. analyzing
malware's own C2 traffic in a controlled lab), intercept at the client with a
TLS-terminating proxy configured as the
malware's effective TLS endpoint — this requires the lab environment to trust the
proxy's CA certificate and works only because you control the client side
(see the isolated detonation environment in
computing-software.digital-forensics-incident-response.malware-analysis.static-and-dynamic-triage).
This is a lab/detonation technique, not something applicable to a captured pcap from
an incident after the fact.

## 4. Certificate forensics when you can't decrypt
Even without decryption, the certificate presented during the TLS handshake (visible
unencrypted in the Server Hello/Certificate messages) carries real signal:
- **Self-signed or very recently issued certificates** (check `notBefore`) are common
  for throwaway C2 infrastructure and phishing kits — a cert issued hours or days
  before first observed use is a stronger signal than domain age alone.
- **Certificate Transparency logs** let you pivot from a specific
  certificate (by serial number or SAN) to every other domain that certificate (or
  one from the same issuing pattern/CA account) has covered — the same
  infrastructure-pivoting logic as
  computing-software.digital-forensics-incident-response.incident-response-process.threat-intelligence-and-ioc-pivoting,
  applied to TLS certs specifically.

## Verify
- Confirm the negotiated cipher suite before attempting RSA-private-key decryption —
  (EC)DHE suites cannot be decrypted this way regardless of key possession.
- Confirm a keylog file's timestamps actually overlap the pcap's capture window
  before relying on it for decryption of that specific capture.
- For any certificate-based pivot, record the exact match basis (serial number, SAN
  overlap, issuer pattern) and its confidence, per the pivoting discipline in the
  threat-intelligence skill above.

Verify findings against more than one source before treating a single certificate-based
pivot as conclusive attribution of shared infrastructure.

## Checked
2026-11-01. Confirmed in the Wireshark TLS wiki: the `SSLKEYLOGFILE` mechanism and which
applications support it, the "(Pre)-Master-Secret log filename" preference, key log working with
DH key exchange, RSA keys working only in limited cases and not with TLS 1.3, the Edit →
Preferences → RSA Keys dialog from Wireshark 3.0 and the deprecated RSA keys list. Removed:
named proxy tools, named CT services and the JA3S clustering claim, which were not confirmed.
Method: documentation only; no commands were run.
