---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-initial-setup-hostname-time-dns
name: fortigate-initial-setup-hostname-time-dns
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [fortigate-initial-setup, fortios, hostname, ntp, dns, admin-timeout, global-settings]
level: practitioner
status: draft
description: "Set FortiGate hostname, timezone, NTP, DNS and hardened admin access settings from the CLI."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: a new FortiGate with correct time, DNS and a locked-down management plane before policies are built.

```
config system global
    set hostname "fgt-edge-01"
    set timezone "US/Pacific"
    set admintimeout 10
    set admin-https-ssl-versions tlsv1-2 tlsv1-3
    set admin-lockout-threshold 3
    set admin-lockout-duration 300
    set admin-sport 8443
end
config system ntp
    set ntpsync enable
    set type custom
    config ntpserver
        edit 1
            set server 192.0.2.123
        next
    end
end
config system dns
    set primary 192.0.2.53
    set secondary 192.0.2.54
end
```
Moving the admin HTTPS port frees 443 for SSL VPN or other services. Restrict which interfaces allow management with `set allowaccess ping https ssh` per interface (see the interfaces skill) and disable HTTP/telnet.

Gotchas
- The timezone value format differs between releases (name vs numeric index); confirm with `set timezone ?`.
- Wrong time breaks certificates, FortiGuard licensing, HA sync and logs.
- Changing `admin-sport` over the same HTTPS session drops it; reconnect on the new port.

## Verify
```
get system status
execute time
diagnose sys ntp status
execute ping 192.0.2.53
```
NTP status shows a synchronised server and `get system status` lists the hostname.
