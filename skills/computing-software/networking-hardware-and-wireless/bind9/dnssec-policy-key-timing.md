---
id: computing-software.networking-hardware-and-wireless.bind9.dnssec-policy-key-timing
name: dnssec-policy-key-timing
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, dnssec-policy, key-lifetime, signature-validity]
level: advanced
status: docs-checked
description: "Write a custom BIND 9 dnssec-policy: keys with lifetime and algorithm, dnskey-ttl, signature validity and refresh, and the timing defaults."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://bind9.readthedocs.io/en/latest/chapter5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dnssec policy key timing
A custom policy:

```
dnssec-policy "custom" {
    dnskey-ttl 600;
    keys {
        ksk lifetime P1Y algorithm ecdsap384sha384;
        zsk lifetime 60d algorithm ecdsap384sha384;
    };
    nsec3param iterations 0 optout no salt-length 0;
};
```

Key roles in `keys` are `ksk`, `zsk` or `csk`; options include `key-store`, `lifetime`, `algorithm`, `tag-range` and `flags`.

Defaults documented in the reference: `dnskey-ttl` 1h, `purge-keys` P90D, `publish-safety` and `retire-safety` 1h, `signatures-refresh` P5D, `signatures-validity` P2W, `max-zone-ttl` PT24H, `zone-propagation-delay` PT5M, `parent-ds-ttl` P1D, `parent-propagation-delay` PT1H.

Reference a policy from a zone with `dnssec-policy "custom";`.

## Checked

2026-11-04. Read the dnssec-policy Block Definition and every option entry in the Administrator Reference Manual; listed defaults, key roles and keys options confirmed, and the example algorithm name is in the DNSSEC chapter. Nothing was removed.

Method: documentation only; no commands were run.
