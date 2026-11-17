---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.basic-packet-capture-with-pktmon-and-wireshark
name: basic-packet-capture-with-pktmon-and-wireshark
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, evidence-gathering, packet-capture, pktmon, wireshark, display-filters, tcp-reset, tls-handshake, dns-capture, etl2pcapng]
level: advanced
status: gated
description: "Capture and read client network traffic for support: pktmon on Windows without installs, Wireshark capture and display filters, spotting DNS failures, TCP resets and TLS errors."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/networking/technologies/pktmon/pktmon"
  - "https://www.wireshark.org/docs/wsug_html_chunked/"
  - "https://wiki.wireshark.org/DisplayFilters"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# basic-packet-capture-with-pktmon-and-wireshark

Goal: answer "is the traffic leaving the PC, and what comes back?" with
evidence, when logs don't explain a connection failure.

## Capture on Windows without installing anything (pktmon)
```cmd
pktmon filter add -i 10.20.1.15            :: optional: limit to a host (or -p 443)
pktmon start --capture --comp nics --pkt-size 0 -f %TEMP%\cap.etl
:: reproduce the problem
pktmon stop
pktmon etl2pcap %TEMP%\cap.etl -o %TEMP%\cap.pcapng
pktmon filter remove
```
Open the pcapng in Wireshark on your own machine.

## Wireshark capture
Pick the active interface; capture filter (BPF) to reduce size, e.g.
`host 10.20.1.15` or `port 53`. Reproduce once, stop.
macOS/Linux: `sudo tcpdump -i en0 -w cap.pcap host 10.20.1.15`.

## Display filters that answer support questions
| Question | Filter |
|---|---|
| Did DNS resolve? | `dns` — look for responses with "No such name" or no response |
| Did the TCP connection open? | `tcp.flags.syn==1` — SYN without SYN/ACK = blocked/unreachable |
| Was it reset? | `tcp.flags.reset==1` — RST from server/firewall |
| Retransmissions/loss? | `tcp.analysis.retransmission` |
| TLS failing? | `tls.handshake` / `tls.alert_message` — alert after Client Hello = protocol/cipher/cert issue |
| HTTP errors (unencrypted) | `http.response.code >= 400` |
| Traffic to one host | `ip.addr==10.20.1.15` |
Statistics → Conversations shows who talked to whom.

## Interpreting patterns
- SYN, no reply → firewall drop / routing / host down.
- SYN, RST → port closed or actively refused (service not listening,
  firewall reject).
- Handshake ok, TLS alert → certificate/TLS version mismatch, TLS
  inspection.
- Long gaps before responses → server slowness vs network (compare
  timestamps).

## Gotchas
- Captures contain sensitive data (credentials in clear protocols, cookies)
  — get approval, keep short, store securely.
- VPN: capture on the virtual adapter to see inner traffic; physical NIC
  shows encrypted tunnel only.

## Verify
The capture shows the specific failure point (no DNS answer, RST, TLS
alert) that you then fix or hand to the network team with the pcap.

## Checked

- Date: 2026-11-02.
- Confirmed against: Pktmon is an in-box Windows capture tool and supports pktmon filter add (Microsoft Learn pktmon page); the tcp.flags.syn field semantics (Wireshark display filter docs).
- Not confirmed: the pktmon start options (--comp nics, --pkt-size 0), etl2pcap output syntax and the filter strings: the pktmon page fetched is an overview (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.
