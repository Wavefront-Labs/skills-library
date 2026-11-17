---
id: computing-software.digital-forensics-incident-response.log-analysis.client-attribution-through-x-forwarded-for
name: client-attribution-through-x-forwarded-for
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [xff-attribution, x-forwarded-for, proxy-logs, web-logs, dfir]
level: practitioner
status: draft
description: "Attribute web requests to real clients behind CDNs, load balancers and proxies using X-Forwarded-For, Forwarded and CDN headers, and spot spoofed header values."
sources: ["https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For", "https://www.rfc-editor.org/rfc/rfc7239", "https://developers.cloudflare.com/fundamentals/reference/http-headers/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Client attribution through X-Forwarded-For

Behind a CDN or load balancer, the web server's client IP is the proxy. The real client is in a header each hop appends to.

## Headers
| Header | Set by |
|---|---|
| `X-Forwarded-For: client, proxy1, proxy2` | Each proxy appends the address it received from |
| `Forwarded: for=203.0.113.7;proto=https` (RFC 7239) | Standardised form |
| `CF-Connecting-IP`, `True-Client-IP` | Cloudflare / Akamai (single trusted value) |
| `X-Real-IP` | nginx convention |
| AWS ALB / ELB access logs `client:port` | Load balancer log has the real IP directly |

## Rule: trust from the right
The **leftmost** XFF value is whatever the client sent and can be forged. Count from the right, skipping the hops you control: the first address not belonging to your infrastructure is the client.
```text
X-Forwarded-For: 1.2.3.4, 198.51.100.20, 10.0.0.5
                 ^forged?  ^real client    ^your ALB
```

## Investigation steps
1. Map the request path (CDN -> WAF -> LB -> reverse proxy -> app) and which component logs which IP.
2. Check whether the web server logs XFF at all (`%{X-Forwarded-For}i` in Apache, `$http_x_forwarded_for` in nginx, IIS advanced logging / `X-Forwarded-For` custom field). If not, use CDN/LB logs and join on time, URI and request ID.
3. Join on a request ID header (`X-Request-ID`, `CF-Ray`, ALB `X-Amzn-Trace-Id`) where available.
4. Flag requests where the leftmost value is private/loopback or odd (`127.0.0.1`, `localhost`): attempts to bypass IP allowlists.

## Gotchas
- Apps that use the leftmost XFF for access control or rate limits are exploitable; attackers' log entries then show fake IPs.
- Direct-to-origin traffic bypassing the CDN has no CDN header: check for origin IP exposure.

## Verify
For each attributed client IP, the CDN or load balancer log shows the same request (time, URI, request ID) from that address.
