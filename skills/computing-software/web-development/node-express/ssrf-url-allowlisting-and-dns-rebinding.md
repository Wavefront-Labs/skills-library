---
id: computing-software.web-development.node-express.ssrf-url-allowlisting-and-dns-rebinding
name: ssrf-url-allowlisting-and-dns-rebinding
category: computing-software
field: web-development
product: node-express
tags: [ssrf, server-side-request-forgery, url-allowlist, dns-rebinding, owasp-a10, outbound-requests, egress-proxy]
level: practitioner
status: verified
description: "Defending server-side fetches of user-supplied URLs: scheme/host allowlists, resolving and pinning IPs to beat DNS rebinding, and egress controls."
sources:
  - https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/
  - https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html
  - https://portswigger.net/web-security/ssrf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSRF: URL allowlisting and DNS rebinding

**Goal:** features that fetch URLs (webhooks, imports, image proxies, PDF renderers, link previews) can't be pointed at internal services.

## 1. Prefer an allowlist
If the destination set is known (partner APIs, your own buckets), allow exact hosts and schemes only:
```js
const ALLOWED = new Set(['api.partner.com', 'hooks.slack.com']);
const u = new URL(input);
if (u.protocol !== 'https:' || !ALLOWED.has(u.hostname) || u.username || u.password || (u.port && u.port !== '443')) throw new Error('blocked');
```
The parsed `port` is the empty string for the scheme's default port (`https://api.partner.com:443/x` has `port === ''`, `:8443` has `'8443'`), so the port test above is safe. Compare parsed `hostname` exactly - never `includes`/`endsWith` without a leading dot (`evilpartner.com`, `api.partner.com.evil.io`).

## 2. Open-ended URLs: validate the resolved IP, then connect to that IP
Checking the hostname then letting the HTTP client resolve again is a TOCTOU hole: **DNS rebinding** returns a public IP for the check and `127.0.0.1` for the connection. Resolve once, check every address, and pin the connection:
```js
import dns from 'node:dns/promises';
import ipaddr from 'ipaddr.js';
async function resolvePublic(hostname) {
  const addrs = await dns.lookup(hostname, { all: true });
  for (const { address } of addrs) {
    const r = ipaddr.process(address).range();     // handles IPv4-mapped IPv6
    if (r !== 'unicast') throw new Error(`blocked ${address} (${r})`);
  }
  return addrs[0].address;
}
```
`ipaddr.process` unwraps IPv4-mapped IPv6 (`::ffff:127.0.0.1` is `loopback`); everything except `unicast` is blocked, which covers `reserved` (192.0.2.0/24, 198.18.0.0/15, 192.88.99.0/24, 2001:db8::/32), `rfc6052` (NAT64, which can embed 127.0.0.1) and `6to4`. Then connect with a custom `lookup` that returns the vetted address (undici `Agent({ connect: { lookup } })` or `http.Agent` with `lookup`), keeping SNI/Host as the original hostname. Libraries: `ssrf-req-filter`, `request-filtering-agent` (Node), `advocate` (Python).

## 3. Network layer (the real backstop)
Run fetchers in an isolated egress path: an outbound proxy (Smokescreen) that enforces public-only destinations, or a subnet/security group with no route to internal ranges and the metadata service. App checks get bypassed; network policy doesn't.

## 4. Response handling
Don't return raw response bodies/errors to the user (blind SSRF still leaks via timing; full SSRF leaks data). Cap size and time, restrict content types.

## Verify
- [ ] Test URLs: `http://127.0.0.1`, `http://[::1]`, `http://0x7f000001`, `http://2130706433`, `http://169.254.169.254`, `http://10.0.0.1`, `http://localtest.me`, a rebinding domain (rbndr.us) - all blocked.
- [ ] Connections go to the validated IP (packet capture or debug log).
- [ ] Egress proxy logs show denials for internal ranges.

## Checked
Run on Windows with Node 20.20.2, ipaddr.js 2.5.0 and undici 7.30.1: `.range()` for 24 addresses (loopback, private, linkLocal 169.254.169.254, carrierGradeNat, unspecified, multicast, broadcast, reserved, uniqueLocal incl. `fd00:ec2::254`, rfc6052 `64:ff9b::7f00:1`, 6to4, IPv4-mapped; public ones are `unicast`); live DNS: `localtest.me`, `127.0.0.1.nip.io` and `7f000001.c0a80001.rbndr.us` returned 127.0.0.1 so a hostname check alone is not enough; an undici `Agent` with a custom `connect.lookup` was called once for the hostname, connected to the address the lookup returned and sent `Host: pinned.invalid:<port>`. Linux pass: WHATWG URL parsing is built into Node and gave the same results on Linux (Node 20.20.2 musl in a WSL2 distro). Not run: `ssrf-req-filter`, `request-filtering-agent`, Smokescreen, packet capture, a real rebinding race (the rbndr host alternates answers; only one answer was seen).
