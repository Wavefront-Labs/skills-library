---
id: computing-software.systems-network-administration.pi-hole.unbound-dnssec-validation-test
name: unbound-dnssec-validation-test
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [dnssec-works-test, ad-flag, dnssec-bogus]
level: advanced
status: draft
description: "Verify that Unbound validates DNSSEC for Pi-hole using the dnssec.works test domains and the ad flag."
sources: ["https://docs.pi-hole.net/guides/dns/unbound/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Test Unbound DNSSEC validation

The Unbound setup in the Pi-hole guide verifies DNSSEC signatures and discards BOGUS domains. Confirm it works by querying Unbound directly on port 5335:

```bash
dig fail01.dnssec.works @127.0.0.1 -p 5335
dig +ad dnssec.works @127.0.0.1 -p 5335
```

**Expected results**

- `fail01.dnssec.works` returns status `SERVFAIL` and no IP address.
- `dnssec.works` returns `NOERROR` plus an IP address and an `ad` flag in the `flags:` line. `ad` means Authentic Data: the answer was authenticated and validated using DNSSEC.

**If results differ from these**

- Check `harden-dnssec-stripped: yes` in `/etc/unbound/unbound.conf.d/pi-hole.conf`.
- Note `use-caps-for-id: no` is set because capitalization randomisation is known to cause DNSSEC issues sometimes.

**Timing.** The first query after startup may be slow; subsequent queries to other domains under the same TLD should be fairly quick.

**Checklist**

1. Query port 5335 directly, not through Pi-hole.
2. Look for `SERVFAIL` on the failing domain.
3. Look for `ad` on the good one.
