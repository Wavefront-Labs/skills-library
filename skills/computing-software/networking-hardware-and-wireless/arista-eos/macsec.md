---
id: computing-software.networking-hardware-and-wireless.arista-eos.macsec
name: macsec
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, macsec, mac-security, 802-1ae, key-chain]
level: practitioner
status: draft
description: "Configure EOS MACsec profiles with key chain and connection key to encrypt point-to-point links."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MACsec link encryption
Goal: encrypt a link at layer 2.

```
key chain MSKEY
   key 1234567890abcdef1234567890abcdef
      key 1 encryption-algorithm aes256-gcm-xpn
mac security
   profile P1
      cipher aes256-gcm-xpn
      connection-key <cak-placeholder>
interface Ethernet1
   mac security profile P1
```

```
show mac security status
show mac security counters interface Ethernet1
```

- Only some hardware and optics support MACsec: confirm per platform.
- CAK/CKN values are secrets: keep them in a vault and rotate through key chains.
- Both ends need compatible cipher and key; use pre-shared key with fallback only deliberately.

Gotcha: A cipher suite mismatch brings the link up but drops traffic; `show mac security status` reveals the session state.

Operational tip: test failover between active and fallback keys during a window, since a key rollover that fails will take the link offline. Record which platforms and optics were validated. Monitor MKA counters after enabling, as intermittent link flaps on optics are easier to find when you correlate them with secure channel resets.

## Verify
- `show mac security status` shows `Secured` and counters increment.
