---
id: computing-software.collaboration-platform-administration.nextcloud.brute-force-protection-behaviour
name: brute-force-protection-behaviour
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [brute-force, throttling, bruteforcesettings, ip-whitelist, 429]
level: practitioner
status: docs-checked
description: "Understand how Nextcloud throttles by source IP, the 25 second delay and 429 limit, the IP whitelist app, and why disabling the protection is discouraged."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/bruteforce_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: read throttling behaviour correctly before changing any setting.

How it works:
- Requests from an IP address through a protected entrypoint are slowed for up to a 24 hour period, and in extreme cases blocked outright for up to 30 minutes.
- The primary filter is the IP address, so an account is unaffected when connecting from a different IP than the attacker.
- On the login page each failed attempt takes longer. The maximum delay is 25 seconds. If the maximum number of attempts (currently 10) is reached within the last 30 minutes, the server returns `429 Too Many Requests` until the count drops below the threshold.
- A successful login from the same source IP clears earlier invalid attempts.
- A daily cronjob prunes history; entries expire after 48 hours.

Controls:
- Enabled by default. The shipped `bruteforcesettings` app adds *Administration settings -> Security -> Brute-force IP whitelist*, where you see the status of your own IP and exempt IPv4 or IPv6 addresses and ranges.
- Disabling the `bruteforcesettings` app only removes the web UI; protection is in core.
- The only off switch is `auth.bruteforce.protection.enabled` in `config.php`. The docs heavily discourage this for production servers reachable by a public IP, since it lets an attacker iterate over users, passwords and two-factor codes.

Prefer fixing the cause of false positives (a misconfigured reverse proxy or a misbehaving client) over whitelisting.

Check: repeated bad logins from a test host slow down, then a good login resets the delay.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/bruteforce_configuration.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
