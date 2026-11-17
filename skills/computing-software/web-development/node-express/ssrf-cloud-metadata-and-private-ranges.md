---
id: computing-software.web-development.node-express.ssrf-cloud-metadata-and-private-ranges
name: ssrf-cloud-metadata-and-private-ranges
category: computing-software
field: web-development
product: node-express
tags: [ssrf, server-side-request-forgery, cloud-metadata-endpoint, private-ip-blocking, imdsv2, link-local, ip-ranges]
level: practitioner
status: verified
description: "Blocking SSRF targets: cloud metadata endpoints (169.254.169.254, IMDSv2), RFC1918/loopback/link-local/IPv6 ranges, and odd IP encodings."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html
  - https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html
  - https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSRF: cloud metadata and private ranges

**Goal:** even if an SSRF check is bypassed, the most damaging targets - instance credentials and internal admin services - are unreachable.

## 1. Ranges to deny (resolve first, then check every address)
| Range | What |
|---|---|
| `127.0.0.0/8`, `::1` | Loopback |
| `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `fc00::/7` | Private |
| `169.254.0.0/16`, `fe80::/10` | Link-local - **includes cloud metadata 169.254.169.254** |
| `100.64.0.0/10` | Carrier-grade NAT (used internally by some clouds/K8s) |
| `0.0.0.0/8`, `::` | "This host" - often reaches localhost |
| `::ffff:0:0/96` | IPv4-mapped IPv6 - unwrap then re-check |
| `fd00:ec2::254` | AWS IMDS over IPv6 |
| `224.0.0.0/4`, `240.0.0.0/4`, broadcast | Multicast/reserved |
Use a library (`ipaddr.js` `.range()`, Python `ipaddress.ip_address(x).is_global`, but not on its own: on Python 3.14 `is_global` is True for `64:ff9b::7f00:1` (NAT64 wrapping 127.0.0.1), `224.0.0.1` (multicast) and `192.88.99.1`, so also reject `is_multicast`, NAT64 `64:ff9b::/96` and `::ffff:`-mapped addresses (unwrap `ipv4_mapped` first) rather than regexes: attackers use decimal (`2130706433`), hex (`0x7f.1`), octal (`0177.0.0.1`), short forms (`127.1`) and IPv6 encodings. Python's `ipaddress` rejects these forms, but `socket.getaddrinfo` on Linux (glibc/musl) accepts all of them and connects to 127.0.0.1, while on Windows it refused them: validate the hostname before it reaches any resolver, or resolve once and check the result.

## 2. Metadata service hardening
- **AWS**: require IMDSv2 (`HttpTokens=required`) - needs a PUT to get a session token, which most SSRF primitives can't do - and set hop limit 1 so containers can't reach it through the host. Give the instance role least privilege.
- **GCP**: metadata requires `Metadata-Flavor: Google` header; **Azure**: requires `Metadata: true` header. Header requirements stop simple GET-only SSRF but not SSRFs where headers are attacker-controlled.
- Kubernetes: block pod egress to `169.254.169.254` with NetworkPolicy unless needed; use workload identity.

## 3. Redirects re-open the hole
A public URL can `302` to `http://169.254.169.254/`. Disable automatic redirects (`redirect: 'manual'` in fetch/undici) and re-validate each hop's resolved IP, max 3 hops.

## 4. Internal services
Don't rely on "internal = trusted": require auth on internal admin endpoints (Redis, Elasticsearch, Consul, Docker socket, kubelet) so an SSRF hit isn't game over.

## Verify
- [ ] All encodings of 127.0.0.1 and 169.254.169.254 blocked in tests.
- [ ] `aws ec2 describe-instances` shows `HttpTokens: required`, hop limit 1.
- [ ] A redirect-to-metadata test URL is blocked at the second hop.

## Checked
Run on Windows (Python 3.14.0, ipaddr.js 2.5.0, Node 20.20.2) and on Linux (Python 3.14.8 musl in WSL2): `ipaddr.js` ranges and `is_global` for the ranges in the table (loopback, private, link-local, CGNAT, 0.0.0.0, mapped, `fd00:ec2::254`, multicast, reserved) and the NAT64, multicast and 192.88.99.1 gaps above; `ipaddress.ip_address` rejects the alternative IPv4 notations and `getaddrinfo` accepts them on Linux only. Fetched: AWS EC2 metadata docs (PUT responses default to hop limit 1; `HttpTokens` documented for `modify-instance-metadata-options` as `required`), Google Compute metadata docs (`Metadata-Flavor: Google` required) and Azure IMDS docs (`Metadata:true` header). Not run: any cloud instance, NetworkPolicy, `aws ec2 describe-instances`, IMDSv2 token exchange, the 240.0.0.0/4 entry.
