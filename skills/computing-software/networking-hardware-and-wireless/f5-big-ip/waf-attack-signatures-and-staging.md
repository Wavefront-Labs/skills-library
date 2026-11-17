---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.waf-attack-signatures-and-staging
name: waf-attack-signatures-and-staging
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, attack-signatures, signature-staging, signature-sets]
level: practitioner
status: draft
description: "Manage ASM/Advanced WAF attack signature sets, update them offline, and use staging to avoid false positive blocks."
sources:
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-asm-implementations.html
  - https://my.f5.com/manage/s/article/K13823
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Attack signatures, signature sets and staging

```
tmsh show asm attack-signature-update
tmsh install asm attack-signatures file /var/tmp/ASM-SignatureFile_20240101.im  # confirm command on your version
tmsh list asm signature-set
tmsh modify asm policy pol_web signature-staging enabled
```
- Signature update: the updates are an `.im` file from F5 downloads, installed via Security > Options > Application Security > Attack Signatures > Update Signatures (system-wide). Automatic updates need the management interface to reach the update service.
- A signature set groups signatures by systems (e.g. Apache, SQL), type and accuracy. Assigning a set to the policy enables all its signatures; per-signature enable/disable and staging apply per policy.
- Staging: newly added or updated signatures start staged for 7 days (default), logging but not blocking; any hit during staging is reported as a learning suggestion, which lets you disable the signature or accept staging end. Policy `signature-staging enabled` sets this.
- Updating signatures takes effect for new requests after Apply; plan updates on standby units first.
- Gotcha: enforcing a signature set too wide (e.g. All Signatures) in blocking mode causes false positives on JSON/XML/Base64 payloads - narrow by parameter (e.g. disable signature 200001475 on a content field) rather than disabling globally.
- Do not edit signatures to hide an attack that is actually valid.

Verify: send a known SQL injection pattern to a test parameter and see "Attack signature detected" in the request log, with the signature ID and staging state shown.
