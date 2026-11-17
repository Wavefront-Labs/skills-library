---
id: computing-software.systems-network-administration.pi-hole.docker-port-conflicts-and-listening
name: docker-port-conflicts-and-listening
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [systemd-resolved-port-53, docker-port-conflicts, bridge-listening-mode]
level: practitioner
status: docs-checked
description: "Resolve port 53, 80 and 443 conflicts for a Pi-hole container, including systemd-resolved and the bridge listening mode."
sources: ["https://docs.pi-hole.net/docker/tips-and-tricks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Port conflicts and listening mode in Docker

**Port 53 held by systemd-resolved.** Ubuntu 17.10+ and Fedora 33+ run a caching stub on port 53. Disable the stub:

```bash
sudo sh -c 'mkdir -p /etc/systemd/resolved.conf.d && printf "[Resolve]\nDNSStubListener=no\n" | tee /etc/systemd/resolved.conf.d/no-stub.conf'
sudo sh -c 'rm -f /etc/resolv.conf && ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf'
systemctl restart systemd-resolved
```

The symlink step matters because the stub setting does not change the nameserver entries, which would otherwise break resolution. Disabling `systemd-resolved` entirely can cause VPN name resolution problems.

**Ports 80 or 443 in use.** Either change the mapping, for example `"8080:80/tcp"`, or in `network_mode: host` set the web ports:

```yaml
FTLCONF_webserver_port: '8080o,[::]:8080o,8443os,[::]:8443os'
```

This only affects web ports; DNS (53), DHCP (67) and NTP (123) need Docker port mappings or host networking.

**Bridge network.** The default `bridge` mode needs the DNS interface setting "Listen on all interfaces, permit all origins" (`dns.listeningMode` = `ALL`).

**SELinux Enforcing.** Add `:z` to the volume lines.

**Test.** Load `http://pi.hole/admin/`.

**Checklist**

1. Find what holds the port.
2. Stop it or remap the port.
3. Set listening mode for bridge networking.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: Docker Tips and Tricks (docker/tips-and-tricks). Nothing needed removing.
Method: documentation only; no commands were run.
