---
id: computing-software.systems-network-administration.dns-dhcp.encrypted-dns-clients-and-doh-policy
name: encrypted-dns-clients-and-doh-policy
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, dns-over-tls, dns-over-https, encrypted-dns-client, doh-policy, canary-domain, use-application-dns-net, windows-doh, systemd-resolved-dot, android-private-dns, firefox-trr, chrome-secure-dns, ddr, enterprise-policy]
level: practitioner
status: draft
description: "Control encrypted DNS on endpoints: point Windows, Linux, Android and Apple at your DoH/DoT resolver and stop browser DoH bypass (canary domain, policy, DDR)."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/dns/doh-client-support
  - https://support.mozilla.org/en-US/kb/canary-domain-use-application-dnsnet
  - https://datatracker.ietf.org/doc/html/rfc9462
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Encrypted DNS clients and enterprise DoH policy

## Configure clients to use your encrypted resolver
- **Windows 11 / Server 2022+**:
  ```
  Add-DnsClientDohServerAddress -ServerAddress 10.0.0.53 -DohTemplate https://resolver.example.org/dns-query -AllowFallbackToUdp $false -AutoUpgrade $true
  Get-DnsClientDohServerAddress
  ```
  then set the adapter DNS to 10.0.0.53 with "Encrypted only" (Settings or GPO "Configure DNS over HTTPS").
- **Linux systemd-resolved**: `/etc/systemd/resolved.conf`: `DNS=10.0.0.53#resolver.example.org`,
  `DNSOverTLS=yes` (or `opportunistic`); `resolvectl status` shows `+DNSOverTLS`.
- **Android**: Settings > Private DNS > hostname `resolver.example.org` (DoT 853) or MDM profile.
- **Apple**: configuration profile with a `DNSSettings` payload (DoH or DoT) via MDM.
- **DDR** (RFC 9462): resolvers advertise their encrypted endpoints via `_dns.resolver.arpa` SVCB;
  Windows and Apple can auto-upgrade when the resolver publishes them.

## Stop bypass (browsers using their own DoH)
Browser DoH sends queries to Cloudflare/Google/NextDNS over 443, skipping RPZ filtering, split DNS
and logging.
- **Firefox**: respects the canary domain. Make your resolvers return NXDOMAIN for
  `use-application-dns.net` (RPZ entry `use-application-dns.net CNAME .`) and Firefox disables
  default DoH. Also enterprise policy `DNSOverHTTPS: {Enabled: false}` (or point it to your resolver).
- **Chrome/Edge**: only upgrades to DoH if the system resolver is a known DoH provider; manage with
  policy `DnsOverHttpsMode = off` or `secure` with `DnsOverHttpsTemplates` = your resolver.
- **Network level**: block outbound TCP/UDP 53 and 853 except from your resolvers; block known
  DoH endpoints by IP/SNI on the NGFW (app-ID "dns-over-https"); this is defence in depth, not
  complete (new endpoints appear).
- Apps with hard-coded DoH (some malware, some IoT): detectable via NGFW app-ID/TLS SNI logs.

## Verify
- [ ] Endpoints show your resolver with encryption active (`resolvectl`, `Get-DnsClientDohServerAddress`).
- [ ] `dig use-application-dns.net @resolver` returns NXDOMAIN; Firefox about:networking shows DoH off.
- [ ] Outbound 853 and public DoH blocked except from resolvers (test from a client).
