---
id: computing-software.networking-hardware-and-wireless.unbound.spoofing-defences-and-unwanted-replies
name: spoofing-defences-and-unwanted-replies
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, use-caps-for-id, unwanted-reply-threshold, udp-connect, spoofing, caps-exempt]
level: advanced
status: docs-checked
description: "Defend Unbound against spoofed replies and cache poisoning: 0x20 casing, unwanted-reply-threshold, udp-connect, source port range and delay-close."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# spoofing defences and unwanted replies
- `use-caps-for-id: yes` (default no) randomises query-name casing (0x20) to foil spoofing; `caps-exempt` (alias `caps-whitelist`) lists domains exempt from it.
- `unwanted-reply-threshold` (0, disabled) clears caches after that many unwanted replies; 10 million is suggested.
- `udp-connect` (yes) uses connect(2) on UDP sockets to mitigate ICMP side-channel leakage.
- `outgoing-port-permit` and `outgoing-port-avoid` set the source ports used for outgoing queries; the default is ports above 1024 not IANA-assigned.
- `delay-close` (0, disabled) delays closing timed-out UDP ports so late replies do not hit closed ports.
- `harden-glue` and `harden-referral-path` limit what unauthenticated data is trusted.
- Unbound with `outgoing-interface` as an IPv6 netblock randomises source addresses.

Monitor `unwanted.replies` in extended statistics; some are normal over UDP but high values may indicate spoofing.

## Checked
2026-11-04. Confirmed against the unbound.conf manual: use-caps-for-id, caps-exempt, unwanted-reply-threshold, udp-connect, outgoing-port-permit/avoid, delay-close defaults and behaviour. Nothing removed.
Method: documentation only; no commands were run.
