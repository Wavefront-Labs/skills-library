---
id: computing-software.cloud-infrastructure-engineering.kubespray.cilium-transparent-encryption-ipsec-and-wireguard
name: cilium-transparent-encryption-ipsec-and-wireguard
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [cilium, encryption, ipsec, wireguard, secrets]
level: advanced
status: docs-checked
description: "Turn on Cilium transparent encryption with cilium_encryption_type ipsec (with a base64 cilium_ipsec_key you generate) or wireguard (Linux 5.6+)."
sources:
  - https://kubespray.io/docs/CNI/cilium.md
  - https://kubespray.io/docs/operations/port-requirements.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Cilium can transparently encrypt Cilium-managed host traffic and traffic between endpoints with IPsec or WireGuard (WireGuard needs Cilium 1.10.0 or newer).

**IPsec.** Set:

```yml
cilium_encryption_enabled: true
cilium_encryption_type: "ipsec"
```

A third variable, `cilium_ipsec_key`, needs a secret key string that Kubespray does not generate. The Cilium documentation recommends:

```shell
echo "3 rfc4106(gcm(aes)) $(echo $(dd if=/dev/urandom count=20 bs=1 2> /dev/null | xxd -p -c 64)) 128"
```

Kubespray creates the secret itself, so you only pass the key base64-encoded:

```shell
echo "cilium_ipsec_key: "$(echo -n "3 rfc4106(gcm(aes)) $(echo $(dd if=/dev/urandom count=20 bs=1 2> /dev/null | xxd -p -c 64)) 128" | base64 -w0)
```

**WireGuard.** Two variables:

```yml
cilium_encryption_enabled: true
cilium_encryption_type: "wireguard"
```

Kubespray supports Linux distributions with the WireGuard kernel mode on Linux 5.6 and newer.

Remember the firewall: the port page lists UDP 51871 as the Cilium WireGuard tunnel endpoint.

## Checked

2026-11-08. Cited pages re-read in full. IPsec and WireGuard variables and commands were confirmed on the Cilium page; the UDP 51871 note is from the Port Requirements page.

Method: documentation only; no commands were run.
