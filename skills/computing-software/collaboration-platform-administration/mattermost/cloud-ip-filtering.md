---
id: computing-software.collaboration-platform-administration.mattermost.cloud-ip-filtering
name: cloud-ip-filtering
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [ip-filtering, cidr, cloud-enterprise, allowlist]
level: practitioner
status: docs-checked
description: "Restrict a Mattermost Cloud workspace to approved CIDR ranges in the System Console, including the lockout safeguard and recovery path."
sources: ["https://docs.mattermost.com/administration-guide/manage/cloud-ip-filtering.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cloud IP filtering

IP filtering restricts workspace access to approved IP ranges and requires a Mattermost Cloud Enterprise subscription. A system admin finds it in the System Console under Site Configuration > IP Filtering.

Ranges are written in CIDR notation: an address, a slash and the prefix length. For example 192.168.0.0/24 covers 192.168.0.0 to 192.168.0.255, because the first 24 bits are the network part and 8 bits remain for hosts.

Enable and disable: filtering is active as soon as at least one range is on the allowlist. To switch it off temporarily, remove all ranges or flip the global IP Filtering toggle.

Add a range: select Add Filter, enter the range in CIDR form (such as 192.168.1.0/24), give it a descriptive label so it is recognisable later, and save. Edit or delete a range by hovering over its rule, using the edit or delete option, changing or confirming, and selecting Save.

Safeguard: the System Console refuses to save changes if the IP address you are currently using is not inside the ranges you are saving, which prevents locking yourself out.

Recovery: if existing filters block you from the workspace, you must contact Mattermost support. Going through that process disables all existing rules, so any IP address can then reach the workspace until you re-create the filters. Plan ranges to include every office, VPN egress and remote admin address before enabling.

## Checked

Confirmed against the Cloud IP Filtering page: Cloud Enterprise requirement, System Console location, CIDR example, enable and disable behaviour, add, edit and remove steps, the save safeguard and the support-led recovery that disables all rules. Nothing removed.

Method: docs-checked 2026-11-09 against the full administration-guide/manage/cloud-ip-filtering page (source rst from the mattermost/docs repo).
