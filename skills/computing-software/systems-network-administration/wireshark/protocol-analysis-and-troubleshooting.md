---
id: computing-software.systems-network-administration.wireshark.protocol-analysis-and-troubleshooting
name: protocol-analysis-and-troubleshooting
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tshark, protocol-analysis, network-troubleshooting, expert-info, decode-as, dns, dns-timeout, servfail, nxdomain, dhcp, dora, dhcp-nak, arp, duplicate-ip, gratuitous-arp, icmp, pmtud, path-mtu, fragmentation-needed, http, http-status, service-response-time, smb, smb2, kerberos, ntlm]
level: advanced
status: docs-checked
description: "Diagnose DNS, DHCP, ARP, ICMP/PMTUD, HTTP and SMB2/Kerberos faults in Wireshark: the filter and packet signature for each failure, Expert Info, Decode As."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChStatistics.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChAdvExpert.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChStatSRT.html
  - https://www.wireshark.org/docs/dfref/
  - https://datatracker.ietf.org/doc/html/rfc1191
  - https://datatracker.ietf.org/doc/html/rfc2131
  - https://datatracker.ietf.org/doc/html/rfc2132
  - https://datatracker.ietf.org/doc/html/rfc1035
  - https://datatracker.ietf.org/doc/html/rfc4120
  - https://datatracker.ietf.org/doc/html/rfc4443
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Protocol analysis and troubleshooting — know what "broken" looks like per protocol

**Goal:** go from "the app is slow/broken" to a named protocol failure with frame numbers.
TCP-level analysis (retransmissions, zero window, RTT) and TLS handshakes are covered in
`computing-software.systems-network-administration.wireshark.traffic-capture-and-analysis`;
filter syntax in `...wireshark.packet-capture-filtering-techniques`. This skill is the
per-protocol signature catalogue above TCP.

## 0. Triage order
1. Analyze > Expert Information, grouped by severity. Treat entries as a map, not a verdict.
2. Statistics > Protocol Hierarchy: is the protocol you expect even there?
3. If a protocol runs on a non-standard port it shows as raw TCP/UDP: use Decode As to override
   which protocol is called for that port.
4. Work down the stack: name resolution, address, path, transport, application. Many
   "application" failures are DNS or MTU.

## 1. DNS
- Unanswered queries: `dns.flags.response == 0 && !dns.response_in`.
- Slow answers: `dns.time > 0.2` (the time between query and response).
- Response codes (RFC 1035), field `dns.flags.rcode`: 2 = server failure, 3 = name error
  (meaningful only from an authoritative server: the name does not exist), 5 = refused (the name server refuses the operation).
- A truncated UDP answer (`dns.flags.truncated == 1`) means the client should retry over TCP.

## 2. DHCP
- Filter `dhcp` (older builds: `bootp`). The normal exchange is Discover, Offer, Request, ACK.
- `dhcp.option.dhcp == 6` is a DHCPNAK (RFC 2132 message type 6). RFC 2131: a server sends a
  DHCPNAK when the client's notion of its network address is incorrect, for example after
  moving to a new subnet.
- Check which server answered with `dhcp.option.dhcp_server_id`; an unexpected server id is a
  second DHCP server on the segment.

## 3. ARP and layer 2
- `arp.duplicate-address-detected` and `arp.duplicate-address-frame` are Wireshark's flags for
  two MAC addresses claiming one IP address.
- ARP requests for the gateway with no reply: check VLAN, switch port and upstream path.

## 4. ICMP and path MTU
- IPv4: ICMP type 3, code 4 (`icmp.type == 3 && icmp.code == 4`) is Destination Unreachable,
  fragmentation needed and DF set (RFC 1191); the message carries a Next-Hop MTU field.
- IPv6: `icmpv6.type == 2` is Packet Too Big (RFC 4443).
- Black-hole signature: the handshake completes and small requests work, but the first
  full-size segment (for example `tcp.len >= 1400`) is retransmitted repeatedly and no such ICMP
  message arrives. A smaller MTU on the path (a tunnel) with ICMP filtered is one cause; work
  out the right MSS or MTU from the real tunnel overhead.

## 5. HTTP (cleartext or decrypted)
- Server errors: filter `http.response.code >= 500`.
- `http.time > 1` finds slow responses. Compare it with the TCP RTT to separate network delay
  from server time.

## 6. SMB2 and Kerberos (Windows file access)
- `smb2.nt_status != 0` lists SMB2 packets with a non-zero NT status.
- Statistics > Service Response Time > SMB2 gives per-command response times.
- `kerberos.error_code` values (RFC 4120): 6 = client not found in the Kerberos database,
  7 = server not found in the Kerberos database, 24 (0x18) = pre-authentication failed, 37
  (0x25) = clock skew too great.

## Verify
- [ ] Expert Info reviewed and each warning either explained or dismissed with reason.
- [ ] Name resolution, addressing (DHCP/ARP) and path MTU ruled in or out before blaming the app.
- [ ] Failure stated as protocol + code + frame number (e.g. "frame 2231: KRB error 37").
- [ ] Non-standard ports decoded with Decode As, not ignored.
- [ ] Fix confirmed by a second capture showing the healthy signature.

## Checked
2026-11-09. Read: Wireshark dfref pages for dns, dhcp, arp, icmp, icmpv6, http, smb2 and kerberos
(every field named above exists), the User's Guide chapters on statistics, Expert Information,
Service Response Time (SMB2 listed) and Decode As, RFC 1035 (rcodes 2, 3, 5), RFC 2132 (DHCPNAK
is type 6), RFC 2131 (NAK use), RFC 1191 (type 3 code 4, Next-Hop MTU), RFC 4443 (Packet Too Big
type 2) and RFC 4120 (error codes 6, 7, 24, 37). Removed: the whole SIP/RTP section (VoIP
menus, loss and jitter thresholds, rtp_udp heuristic, one-way audio causes), the HTTP Request
Sequences menu, the Cisco `ip tcp adjust-mss` example, SMB STATUS_ name list, the AAAA stall
timing, the SERVFAIL/DNSSEC and NXDOMAIN search-suffix explanations, DHCP relay and scope causes,
and the ARP storm and inspection explanations. Tags voip, sip, rtp, jitter, packet-loss and
rtp-stream-analysis, mss-clamping were dropped with them.
Method: docs-checked 2026-11-09 against Wireshark dfref pages, the User's Guide chapters and RFCs 1035, 1191, 2131, 2132, 4120 and 4443.
