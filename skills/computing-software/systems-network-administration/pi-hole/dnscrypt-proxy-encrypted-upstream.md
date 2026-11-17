---
id: computing-software.systems-network-administration.pi-hole.dnscrypt-proxy-encrypted-upstream
name: dnscrypt-proxy-encrypted-upstream
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [dnscrypt-proxy, doh-upstream, systemd-socket-override]
level: advanced
status: docs-checked
description: "Run dnscrypt-proxy on 127.0.0.1:5053 as an encrypted DoH or DNSCrypt upstream for Pi-hole."
sources: ["https://docs.pi-hole.net/guides/dns/dnscrypt-proxy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# dnscrypt-proxy as Pi-hole upstream

dnscrypt-proxy provides DNS-over-HTTPS or other encrypted protocols between Pi-hole and its upstream, preventing man-in-the-middle attacks on that hop.

**Install.** Debian 13 and Ubuntu 25 and later have an official package:

```bash
sudo apt update
sudo apt install dnscrypt-proxy
```

Other distributions follow the project wiki.

**Avoid port 53.** FTL listens on 53, so override the socket with `sudo systemctl edit dnscrypt-proxy.socket`:

```text
[Socket]
ListenStream=
ListenDatagram=
ListenStream=127.0.0.1:5053
ListenDatagram=127.0.0.1:5053
```

Empty lines first unset the old values. Edit `/etc/dnscrypt-proxy/dnscrypt-proxy.toml`:

```toml
listen_addresses = []
server_names = ['cloudflare-security']
```

`listen_addresses` is empty to use systemd socket activation; choose `server_names` from the public server list at dnscrypt.info.

**Point Pi-hole at it and restart**

```bash
sudo pihole-FTL --config dns.upstreams '["127.0.0.1#5053"]'
sudo systemctl restart dnscrypt-proxy.socket dnscrypt-proxy.service pihole-FTL.service
```

If `cloudflared` is installed, you may uninstall it because `dnscrypt-proxy` replaces it.

**Checklist**

1. Override the socket to port 5053.
2. Set `server_names`.
3. Set the Pi-hole upstream and restart the three units.
4. Check each shows active (running).

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: dnscrypt-proxy (guides/dns/dnscrypt-proxy). Nothing needed removing.
Method: documentation only; no commands were run.
