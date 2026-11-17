---
id: computing-software.cybersecurity-defensive.security-architecture.remote-browser-isolation
name: remote-browser-isolation
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [remote-browser-isolation, rbi, browser-isolation, sse, pixel-pushing, dom-reconstruction, web-threat-protection]
level: practitioner
status: draft
description: "Deploy remote browser isolation for risky and uncategorised sites: rendering modes, policy triggers in the SWG/SSE, upload/download and clipboard controls, and user friction."
sources: ["https://developers.cloudflare.com/cloudflare-one/policies/browser-isolation/", "https://help.zscaler.com/zia/about-cloud-browser-isolation", "https://www.cisa.gov/resources-tools/resources/protective-dns-and-browser-isolation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Remote browser isolation (RBI)

**Goal:** web content executes in a disposable remote browser; the endpoint only receives a safe
rendering, so drive-by exploits and malicious scripts never run locally.

## Rendering modes
| Mode | How | Trade-off |
|---|---|---|
| Pixel pushing / video stream | Remote browser streams pixels | Strongest isolation; bandwidth, blurry text, poor typing latency |
| DOM reconstruction | Sanitised DOM sent and re-rendered | Good UX; some active content passes in transformed form |
| Network vector rendering (Cloudflare NVR) | Draw commands streamed | Good UX and isolation; vendor specific |

## Policy design (SWG/SSE)
- Isolate: uncategorised and newly registered domains, "security risk" categories, links clicked from email (URL rewriting), personal webmail.
- Do not isolate: SSO/IdP, business SaaS that breaks (video conferencing, WebAuthn flows), internal apps.
- In isolated sessions set: downloads blocked or scanned/CDR, uploads blocked, clipboard copy-out allowed / paste-in blocked, printing blocked, keyboard input read-only for phishing-suspect sites (prevents credential entry).

## Rollout
1. Pilot with security-risk categories only, measure tickets.
2. Add uncategorised/newly seen domains.
3. Consider full isolation only for high-risk user groups (executives, finance) - full isolation for all is expensive and frustrating.

## Gotchas
- WebAuthn/passkeys, client certificates and some video sites fail inside isolation; add bypasses deliberately.
- Isolation does not stop credential phishing if users can type into the page; use read-only mode on suspect categories.
- Licensing is often per user and sized for a subset; check before broadening policy.

## Verify
- [ ] A test page in an isolated category renders through isolation (vendor banner or dev-tools shows remote origin).
- [ ] A test download (EICAR) from an isolated site is blocked.
- [ ] Bypass list reviewed quarterly.
