---
id: computing-software.systems-network-administration.pi-hole.unbound-resolvconf-and-logging
name: unbound-resolvconf-and-logging
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [unbound-resolvconf, unbound-verbosity, apparmor-unbound-log]
level: sme
status: draft
description: "Fix the Debian openresolv conflict with Unbound and enable Unbound logging with the right AppArmor exception."
sources: ["https://docs.pi-hole.net/guides/dns/unbound/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Unbound resolvconf conflict and logging

**resolvconf conflict (Debian Bullseye and later).** The auto-installed `openresolv` package can make `unbound-resolvconf.service` write `nameserver 127.0.0.1` without port 5335 to `/etc/resolv.conf`, which breaks Pi-hole and Unbound. Check and fix:

```bash
systemctl is-active unbound-resolvconf.service
sudo systemctl disable --now unbound-resolvconf.service
sudo sed -Ei 's/^unbound_conf=/#unbound_conf=/' /etc/resolvconf.conf
sudo rm /etc/unbound/unbound.conf.d/resolvconf_resolvers.conf
sudo service unbound restart
```

**Logging.** Do not raise verbosity for daily use because Unbound logs a lot. Levels: 0 errors only, 1 operational info, 2 detailed, 3 query level, 4 algorithm level, 5 client identification for cache misses. In the `server:` block add:

```yaml
logfile: "/var/log/unbound/unbound.log"
log-time-ascii: yes
verbosity: 1
```

Create the file and give Unbound ownership:

```bash
sudo mkdir -p /var/log/unbound
sudo touch /var/log/unbound/unbound.log
sudo chown unbound /var/log/unbound/unbound.log
```

On modern Debian or Ubuntu, add an AppArmor exception: append `/var/log/unbound/unbound.log rw,` to `/etc/apparmor.d/local/usr.sbin.unbound`, then reload AppArmor.

**Checklist**

1. Disable the resolvconf service if active.
2. Restart Unbound.
3. Enable logging only while debugging.
