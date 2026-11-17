---
id: computing-software.networking-hardware-and-wireless.opnsense.caching-proxy-squid
name: caching-proxy-squid
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [squid, web-proxy, transparent-proxy, web-filter, pac]
level: practitioner
status: docs-checked
description: "OPNsense forward caching proxy via os-squid: authenticators, ACLs, traffic limits, category web filter, transparent HTTPS risks and WPAD/PAC."
sources: ["https://docs.opnsense.org/manual/proxy.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Caching proxy (Squid)

Since 24.1 the proxy is not in the default installation; install os-squid from System > Firmware > Plugins. It is a forward caching proxy that reduces bandwidth and speeds up repeated requests, with multi-interface support, transparent mode (including SSL), ICAP for antivirus engines, HTTP and FTP proxying, ACLs for both, compressed blacklists, category filtering, and compatibility with the traffic shaper.

Authentication (Web Proxy > Administration > Forward Proxy > Authentication Settings): LDAP including Active Directory, RADIUS, the local user manager, or none.

Access control (Forward Proxy > Access Control List) offers subnets, ports, MIME types, banned IPs, whitelists, blacklists and browser/user-agent rules.

Traffic management (General Proxy Settings > Traffic Management Settings): maximum download size, maximum upload size, overall bandwidth throttling and per-host throttling.

Category web filter is built in, so squidGuard is not needed: fetch lists from a remote URL, flat files or compressed category lists, automatic conversion to squid ACLs, a built-in scheduler to keep them current, and compatibility with popular blacklists.

Transparent mode diverts requests without client configuration. HTTP works well; for HTTPS the proxy acts as a man in the middle, so clients must trust its certificate. The docs warn that transparent HTTPS can be dangerous and may be refused by services such as e-banking. If transparent mode is unsuitable, use WPAD or PAC for automatic configuration; WPAD via DNS needs the GUI on default TCP/80, which is itself a security risk (MITM), so avoid configuring the appliance from untrusted networks.

Custom error pages: choose Custom for User error pages in General Proxy Settings and an Error Pages tab appears.

## Checked

2026-11-03. Confirmed against the OPNsense Caching Proxy manual page: os-squid from 24.1, authenticators, ACL options, traffic management settings, category filter, transparent HTTPS and WPAD/PAC warnings, custom error pages. Nothing removed.

Method: documentation only; no commands were run.
