---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.client-behavior-review
name: client-behavior-review
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [client-behavior-review, abusive-clients, thundering-herd-clients, mobile-clients, exponential-backoff, production-readiness-review]
level: practitioner
status: docs-checked
description: "Review client behaviour before launch: automatic requests without user input, retries and backoff, jitter, and server-side control of client configuration."
sources: ["https://sre.google/sre-book/reliable-product-launches/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client behaviour review

SRE Book "Reliable Product Launches", "Client Behavior": on a traditional website every request follows a
user action, so request rates are limited by how fast users click and load doubles only if users double.
That no longer holds for clients that initiate actions without user input, such as a phone app that
periodically syncs its data or a website that periodically refreshes; abusive client behaviour can easily
threaten stability. (Protecting against scrapers and denial-of-service is a different topic from designing
safe first-party client behaviour.) The chapter's checklist question is "Do you have auto-save, auto-complete
or heartbeat functionality?", with action items to back off exponentially on failure and to jitter
automatic requests.

## Questions to ask
- Does the client retry? With exponential backoff and jitter?
- Does anything happen at a fixed wall-clock time or on a fixed period shared by all clients?
- What happens when the server is down and all clients come back at once?
- Can the polling or sync interval be changed from the server?
- Is there a server-controlled way to switch off every background behaviour?

## Required client controls
| Control | Implementation |
|---|---|
| Jittered automatic requests | randomise the schedule per client |
| Server-controlled behaviour | per the book, an app can check in periodically and download a configuration file that enables or disables features or sets parameters such as how often it syncs or retries |
| Backoff on errors | exponential on failure |

The book adds that dormant, server-switchable functionality makes aborting a launch easier: switch the
feature off, iterate and release an updated app, without shipping a new app version to every phone.

## Server-side defences
- Per-client rate limiting (see `per-customer-limits-and-quotas`).
- Handling overload from synchronized client behaviour: the book lists it among overload causes (SRE Book
  "Reliable Product Launches", and see "Handling Overload").

## Gotchas
- Third-party SDKs inside your app may have their own retry storms; test them.
- Notifications that trigger an app open and an API call create herds sized to your audience; stagger sends.

## Verify
- [ ] Simulated server outage: reconnect traffic on recovery stays within capacity (load test with real client logic).
- [ ] Every background client behaviour is server-configurable.

## Checked
2026-11-01. Confirmed against the SRE Book "Reliable Product Launches" chapter ("Client Behavior" section, example
checklist question and action items, server-side client configuration, dormant functionality, synchronized client
behaviour as an overload cause). Removed: `Retry-After`/429 and `User-Agent` advice, time-zone/DST claim,
reject-by-version-at-the-edge, and the month-long mobile adoption claim, as none appears on a fetched page.
Method: documentation only; no commands were run.
