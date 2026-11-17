---
id: computing-software.networking-hardware-and-wireless.strongswan.quickstart-roadwarrior-and-eap
name: quickstart-roadwarrior-and-eap
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, roadwarrior, eap, virtual-ip, pools, eap-id]
level: practitioner
status: docs-checked
description: "Roadwarrior gateway and client swanctl.conf patterns for strongSwan: certificate auth, virtual IP pools with vips = 0.0.0.0, EAP-MD5 secrets, and separate EAP identities."
sources:
  - https://docs.strongswan.org/docs/latest/config/quickstart.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# quickstart roadwarrior and eap
**Certificates.** The gateway omits `remote_addrs` and sets only its own `local` id and `local_ts`; the client sets `remote_addrs = moon.strongswan.org`, its own id (here an email that must be a subjectAltName in its certificate) and `remote_ts` with `start_action = start`.

**Virtual IP.** On the gateway add a pool and reference it from the connection:

```
pools { rw_pool { addrs = 10.3.0.0/16 } }
connections { rw { pools = rw_pool ... } }
```

Load with `swanctl --load-pools`. The client requests an address (IKEv1 mode config or IKEv2 configuration payloads) with `vips = 0.0.0.0`.

**EAP.** Gateway: `remote { auth = eap-md5 }`, `send_certreq = no`, and a `secrets` section with one `eap-<name>` block per client holding `id` and `secret`. Client: `local { auth = eap  id = ... }`, `remote { auth = pubkey ... }`, plus its own secret, and only the CA certificate.

**Separate EAP identity.** When the EAP identity differs from the IKEv2 identity (which then defaults to the client IP), use `remote { auth = eap-md5  eap_id = %any }` on the gateway and `local { auth = eap  eap_id = carol }` on the client; secrets then use that plain `id`.

## Checked
2026-11-04. Confirmed against the strongSwan Configuration Quickstart page: roadwarrior certificate case, virtual IP pool and vips = 0.0.0.0, swanctl --load-pools, EAP-MD5 case with send_certreq = no and eap-<name> secrets, EAP identity case with eap_id. Nothing removed.

Method: documentation only; no commands were run.
