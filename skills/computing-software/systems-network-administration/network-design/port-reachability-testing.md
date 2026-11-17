---
id: computing-software.systems-network-administration.network-design.port-reachability-testing
name: port-reachability-testing
category: computing-software
field: systems-network-administration
product: network-design
tags: [test-netconnection, netcat, port-reachability, firewall-testing, nc, powershell, connectivity-check]
level: practitioner
status: docs-checked
description: "Prove whether a TCP or UDP port is reachable end to end with Test-NetConnection, nc, bash /dev/tcp and curl, and read open vs refused vs filtered correctly."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection
  - https://man.openbsd.org/nc.1
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Port reachability testing

"The firewall rule is in" is a claim; a connection test from the real source host is evidence.

## Windows
```
Test-NetConnection db01.example.net -Port 1433
#  TcpTestSucceeded : True / False
Test-NetConnection 10.0.0.5 -Port 443 -InformationLevel Detailed
Test-NetConnection -ComputerName web01 -CommonTCPPort HTTP
```
`-Port` tests a TCP port, `-CommonTCPPort` takes a named port, and `-InformationLevel Detailed` adds detail; the result
includes `TcpTestSucceeded`.
Loop over ports:
```
445,3389,5985 | % { [pscustomobject]@{Port=$_; Open=(Test-NetConnection 10.0.0.5 -Port $_ -WarningAction SilentlyContinue).TcpTestSucceeded} }
```

## Linux/macOS (netcat)
```
nc -vz -w 3 db01.example.net 5432      # TCP: -v verbose, -z scan without sending data, -w timeout seconds
nc -vzu -w 3 10.0.0.53 53              # UDP (unreliable, see below)
```
See the nc man page for your variant's options; the OpenBSD `nc` documents `-z`, `-w` and `-u`.

## Interpreting results
| Result | Typical meaning |
|---|---|
| Connected / succeeded | path and listener OK (a proxy or load balancer may be answering) |
| Connection refused (immediate) | host reachable, nothing listening, or a firewall set to reject |
| Timeout | packets dropped: firewall/ACL/security group, routing, or the host is down |

Always test from the actual source (or the same subnet and security group): a test from your laptop proves nothing
about the app server's path.

## UDP is different
There is no handshake, so a UDP "success" only means no error came back. Test with the real protocol (a DNS query for
DNS, and so on) instead.

## Gotchas
- Name resolution is part of the test; test by IP too to separate DNS from firewall issues.
- Transparent proxies and TLS inspection can accept the TCP handshake for any port.

## Verify
- [ ] Test result recorded with source host, destination, port, time, and outcome in the change ticket.

## Checked
2026-10-28. Confirmed in the Test-NetConnection reference (`-Port`, `-CommonTCPPort`, `-InformationLevel Detailed`,
`TcpTestSucceeded`) and the OpenBSD nc(1) man page (`-z`, `-w`, `-u`). Removed as unconfirmed: bash `/dev/tcp`, curl
telnet and health-check lines, the claim that Test-NetConnection pings first, nmap/ntpdate/snmpget examples, the
"No route to host" row. Interpretation rows are operational judgement.
Method: documentation only; no commands were run.
