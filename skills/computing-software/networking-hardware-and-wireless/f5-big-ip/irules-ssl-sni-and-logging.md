---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.irules-ssl-sni-and-logging
name: irules-ssl-sni-and-logging
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, irules-sni, clientssl-handshake, log-local0]
level: practitioner
status: draft
description: "Use BIG-IP iRules to route on SNI, inspect negotiated TLS, and log efficiently to syslog or a remote HSL pool."
sources:
  - https://clouddocs.f5.com/api/irules/HTTP__uri.html
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-ssl-administration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# iRules for SNI routing, TLS info and safe logging

```
when CLIENTSSL_CLIENTHELLO {
  if { [SSL::extensions exists -type 0] } {
    binary scan [SSL::extensions -type 0] @9a* sni
  }
}
when CLIENTSSL_HANDSHAKE {
  log local0. "TLS [SSL::cipher version] [SSL::cipher name] sni=[SSL::sni]"
}
when HTTP_REQUEST {
  if { [SSL::cipher version] eq "TLSv1" } { HTTP::respond 403 content "TLS 1.0 not allowed" }
}
```
```
when CLIENT_ACCEPTED {
  set hsl [HSL::open -proto UDP -pool pool_syslog]
}
when HTTP_REQUEST {
  HSL::send $hsl "<190> [IP::client_addr] [HTTP::method] [HTTP::host][HTTP::uri]\n"
}
```
- `CLIENTSSL_CLIENTHELLO` can modify handshake handling before the profile completes; the SNI extension is type 0. In newer versions `SSL::sni` (confirm on your version) is simpler.
- `log local0.` writes to `/var/log/ltm` via syslog and is rate-limited (default about 5 msgs/sec/message per TMM) - for access logs use High Speed Logging (HSL), which sends directly to a log pool.
- HSL pool should be monitored; if it is down the rule errors at `HSL::open`.
- Gotcha: logging full URLs and headers can capture secrets and personal data; log selectively and never write cookies or Authorization headers.
- Do not call `log` inside `CLIENT_DATA` or per-packet events without a debug guard.

Verify: `openssl s_client -tls1 -connect vip:443` to test the block; confirm the log lines with `tail -f /var/log/ltm` and the HSL receiver gets UDP packets via `tcpdump -nni 0.0 udp port 514`.
