---
id: computing-software.software-engineering.api-design.server-side-request-forgery-in-apis
name: server-side-request-forgery-in-apis
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, api-ssrf, ssrf, owasp-api-top-10, url-fetch, webhooks, cloud-metadata, allow-list]
level: advanced
status: docs-checked
description: "Stop SSRF (OWASP API7:2023) in endpoints that fetch user-supplied URLs: allow-lists, DNS-rebinding-safe resolution, redirect control and metadata blocking."
sources: ["https://owasp.org/API-Security/editions/2023/en/0xa7-server-side-request-forgery/", "https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Server-side request forgery in APIs

Any field that makes your server fetch a URL (webhook target, picture URL, custom SSO, URL preview) can be aimed at internal services or at the cloud metadata address `169.254.169.254`. OWASP scenario #2: a webhook "test request" whose response was shown to the user returned cloud credentials from the metadata service. Scenario #1: a picture URL of `localhost:8080` let the attacker port-scan from response time. SSRF risk cannot always be completely eliminated; choose protections against the business risk.

## Defences (OWASP API7 and the SSRF Prevention Cheat Sheet)
1. Isolate the resource-fetching mechanism in your network; these features should retrieve remote resources, not internal ones.
2. Use allow-lists where possible: expected remote origins, URL schemes and ports, and accepted media types.
3. Domain allow-listing alone does not stop DNS rebinding. Resolve the name (A and AAAA records), check every resulting address is public (not private, loopback or link-local, IPv4 and IPv6), then connect only to the validated address; a second unchecked DNS lookup between check and connection can bypass it.
```python
import ipaddress, socket
def safe_ips(host, port=443):
    ips = []
    for _, _, _, _, sa in socket.getaddrinfo(host, port, type=socket.SOCK_STREAM):
        ip = ipaddress.ip_address(sa[0])
        if not ip.is_global:
            raise ValueError("blocked address")
        ips.append(sa[0])
    return ips  # connect to one of these, not to the hostname again
```
4. Disable HTTP redirections in the client; otherwise a validated URL can redirect to an internal one.
5. Use a well-tested, maintained URL and IP parser to avoid parsing inconsistencies. The cheat sheet notes some parsers are exposed to hex, octal, dword and mixed-encoding bypasses, so do not use regexes.
6. Validate and sanitise client-supplied input, and do not send raw upstream responses to clients.
7. On AWS, migrate to IMDSv2 and disable IMDSv1 as defence in depth; the cheat sheet lists metadata endpoints for AWS, GCP (`metadata.google.internal`) and Azure to block.
8. Avoid fetching a URL at all where possible (accept an upload or an ID instead).

## Gotchas
- Block lists miss encodings; prefer allow-lists and parse with an IP library.
- A validated IP must be the one actually used for the connection.
- Blind SSRF still leaks information through response time (scenario #1).

Verify: submit `http://127.0.0.1`, `http://169.254.169.254/`, a hostname resolving to a private address, and a public URL that redirects to localhost; all four must be refused.

## Checked
2026-11-08. Read in full: OWASP API Security Top 10 2023 page API7 (definition, both scenarios, prevention list) and the OWASP SSRF Prevention Cheat Sheet (allow-listing, DNS rebinding paragraphs, redirects, parser encodings, IMDSv2, metadata endpoint table). Removed: the IMDSv2 hop-limit-1 setting (not on the page), the specific `::ffff:` IPv4-mapped example, and a code bug where the function returned only the last address. The Python snippet was rewritten from the cheat sheet's approach and not run.
Method: documentation only; no commands were run.
