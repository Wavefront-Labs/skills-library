---
id: computing-software.email-administration.mailcow.mailcow-netfilter-bans-and-external-blocklist
name: mailcow-netfilter-bans-and-external-blocklist
category: computing-software
field: email-administration
product: mailcow
tags: [netfilter, fail2ban-parameters, ban-time, netfilter-regex, external-firewall, blocklist-endpoint]
level: advanced
status: docs-checked
description: "Tune mailcow's built-in Netfilter bans, edit the log regex rules and publish blocked IPs as a URL for an external firewall."
sources: ["https://docs.mailcow.email/manual-guides/mailcow-UI/u_e-mailcow_ui-netfilter/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# mailcow Netfilter bans and blocklist export

Ban settings live under Configuration, Configuration and Details, Configuration, Fail2ban parameters: maximum ban time, maximum attempts before a ban, and similar options.

The same page has a regex section that defines which patterns in the container logs lead to a ban. The docs warn that it needs at least basic regex knowledge. New updates can add or remove default rules, in which case use Reset to default.

Since the 2023-12 update the Netfilter decisions can be exported as an external endpoint so another firewall can use them as a blocklist source (an OPNsense firewall can load the list dynamically). It is off by default: tick Manage Fail2Ban externally, then copy the generated URL into the consuming system. The URL can be regenerated with the reload icon next to the copy button.

The netfilter container reads the logs of the mailcow containers and counts failed logins per network; once a network reaches the maximum attempts it is banned for the ban time.

## Checked

2026-11-09. Confirmed on the Netfilter page: Fail2ban parameters path, max ban time and attempts, the regex section and warning, Reset to default, and the 2023-12 external endpoint with Manage Fail2Ban externally, the URL and reload button. Removed an unconfirmed sentence about SNAT rules and the Redis channel and replaced it with the page's description of how Netfilter counts failed logins.

Method: docs-checked 2026-11-09 against the full Netfilter page (u_e-mailcow_ui-netfilter.en.md in mailcow-dockerized-docs).
