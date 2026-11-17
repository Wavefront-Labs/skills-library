---
id: computing-software.systems-network-administration.pi-hole.home-assistant-pihole-switch
name: home-assistant-pihole-switch
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [home-assistant-pihole, api-blocking-toggle, rest-command]
level: practitioner
status: docs-checked
description: "Toggle Pi-hole blocking from Home Assistant with REST commands that log in, set /api/dns/blocking and log out."
sources: ["https://docs.pi-hole.net/guides/misc/homeassistant/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Home Assistant and Pi-hole blocking

The guide shows a Home Assistant boolean switch that disables or enables Pi-hole blocking via the v6 API.

**1. secrets.yaml**

```yaml
pi_hole_password: "your_pihole_password"
pi_hole_api_url: "http://192.168.1.2/api"
```

**2. configuration.yaml** defines three `rest_command` entries and an `input_boolean`:

- `pihole_login`: `POST {{ api_url }}/auth` with payload `{ "password" : "..." }`
- `pihole_set_blocking`: `POST {{ api_url }}/dns/blocking` with payload `{ "blocking" : true|false, "timer" : seconds|null }`
- `pihole_logout`: `DELETE {{ api_url }}/auth`

`pihole_set_blocking` and `pihole_logout` pass the session ID `sid` in a `sid` header; all three set `verify_ssl: false`.

**3. scripts.yaml** has `pi_hole_disable` and `pi_hole_enable`. Each script logs in, checks `response['status'] == 200`, reads `response['content']['session']['sid']`, sets blocking and logs out. Disabling uses `blocking: "false"` and `timer: "300"` (`null` for permanent); enabling uses `blocking: "true"` and `timer: "null"`.

**4. automations.yaml** links the boolean switch to the two scripts.

**Notes**

- Log out at the end of each script: `webserver.api.max_sessions` (default 16) limits concurrent sessions.
- The guide notes the example does not check Pi-hole's state before toggling, so changes made from the web interface or CLI are not reflected in the boolean.

**Checklist**

1. Store credentials in secrets.
2. The disable script blocks for 5 minutes (`timer: "300"`); enabling is permanent.

## Checked

2026-11-03. Read the Home Assistant guide (secrets, the three `rest_command` entries, `input_boolean`, both scripts, automations and the closing notes) and the `webserver.api.max_sessions` entry of the FTL configuration reference. Removed the application password suggestion, the unexplained self-signed certificate reason, and the dashboard verification item.

Method: documentation only; no commands were run.
