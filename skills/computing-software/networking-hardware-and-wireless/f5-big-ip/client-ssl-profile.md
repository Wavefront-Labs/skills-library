---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.client-ssl-profile
name: client-ssl-profile
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, clientssl, tls-termination, cipher-string, sni]
level: practitioner
status: draft
description: "Terminate TLS on BIG-IP with a client SSL profile: certificate chain, cipher string, TLS versions, and SNI."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-ssl-administration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Client SSL profile and TLS termination

```
tmsh install sys crypto cert www.example.com from-local-file /var/tmp/www.crt
tmsh install sys crypto key www.example.com from-local-file /var/tmp/www.key
tmsh create ltm profile client-ssl cssl_www defaults-from clientssl cert-key-chain replace-all-with { www { cert www.example.com key www.example.com chain corp-chain } } ciphers "ECDHE+AES-GCM:!SSLV3:!TLSV1:!TLSV1_1" options { dont-insert-empty-fragments no-tlsv1.1 }
tmsh modify ltm virtual vs_web profiles add { cssl_www { context clientside } }
```
- The chain file must contain intermediates only; the VS sends leaf plus chain. Missing intermediates is the top cause of "works in Chrome, fails in curl".
- Ciphers: BIG-IP uses its own string syntax (`ECDHE+AES-GCM`), tested with `tmm --clientciphers 'ECDHE+AES-GCM'`. Disable TLS 1.0/1.1 and SSLv3 through the cipher string or `options { no-tlsv1 no-tlsv1.1 }` (confirm names for your version).
- SNI: create several client-ssl profiles on one VS; set `server-name www.example.com` on each and `sni-default true` on one that serves clients without SNI.
- `renegotiation disabled` defends against renegotiation DoS; enable secure renegotiation only if apps need it.
- Gotcha: after changing the certificate, new connections pick it up; existing ones keep the old one. Certificate/key mismatch fails the profile create with "key does not match".

Verify: `openssl s_client -connect vip:443 -servername www.example.com -showcerts` and `tmsh show ltm profile client-ssl cssl_www` for handshake and protocol counters.
