---
id: computing-software.cybersecurity-defensive.wazuh.server-api-hardening
name: server-api-hardening
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [server-api, api-yaml, https, default-credentials, max-request-per-minute, wazuh-wui]
level: advanced
status: docs-checked
description: "Harden the Wazuh server API: api.yaml HTTPS options, default credentials, password rules, wazuh-wui dashboard dependency, rate limits, login blocking."
sources:
  - https://documentation.wazuh.com/current/user-manual/api/securing-api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Config file: `/var/ossec/api/configuration/api.yaml`. Apply changes with `systemctl restart wazuh-manager`.

HTTPS is enabled by default. If no certificate is in `/var/ossec/api/configuration/ssl/`, the API generates a self-signed key and certificate on first start and logs them in `/var/ossec/logs/api.log` (when the log format is `plain`). HTTPS options: `enabled`, `key`, `cert`, `use_ca`, `ca`, `ssl_protocol`, `ssl_ciphers`.

Default credentials: `wazuh:wazuh` and `wazuh-wui:wazuh-wui` (OVA). With the installation assistant, the `wazuh` password is in `wazuh-install-files/wazuh-passwords.txt` inside `wazuh-install-files.tar`. Change them.

Password change: `PUT /security/users/{user_id}`. Passwords must be 8 to 64 characters with upper case, lower case, a number and a symbol.

Gotcha: changing the `wazuh-wui` password breaks the dashboard connection until you update `/usr/share/wazuh-dashboard/data/wazuh/config/wazuh.yml`.

Network and limits:
- `host` defaults to `['0.0.0.0', '::']`, `port` to `55000`.
- `max_request_per_minute` defaults to 300; 0 disables the limit.
- `max_login_attempts` defaults to 50 attempts per 300-second period from the same IP address; exceeding it blocks that IP for the duration of the period. Adjust with `max_login_attempts` and `block_time`.
- When the request limit is exceeded, the API rejects further requests from any user for the rest of the period.

Restrict `host` and firewall port 55000 to management networks.

## Checked

2026-11-08: confirmed against the Wazuh docs page Securing the Wazuh server API (read in full): HTTPS default and self-signed generation, api.yaml HTTPS options, default credentials, wazuh-passwords.txt extraction, password rules, the wazuh-wui dashboard warning, default host and port, the 300 requests-per-minute limit and its 0 disable, and the 50 attempts per 300 seconds login limit. Reworded the block_time description to the page's wording.
Method: documentation only; no commands were run.
