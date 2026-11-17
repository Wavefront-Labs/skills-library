---
id: computing-software.systems-network-administration.netbox.required-configuration-parameters
name: required-configuration-parameters
category: computing-software
field: systems-network-administration
product: netbox
tags: [allowed-hosts, secret-key, api-token-peppers]
level: practitioner
status: docs-checked
description: "Define the five parameters every new install must set in configuration.py."
sources: ["https://netboxlabs.com/docs/netbox/installation/3-netbox/", "https://netboxlabs.com/docs/netbox/configuration/required-parameters/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Required parameters

Goal: make `configuration.py` valid for a new install.

Copy `configuration_example.py` to `configuration.py` in `/opt/netbox/netbox/netbox/`. Only five parameters are required: `ALLOWED_HOSTS`, `API_TOKEN_PEPPERS`, `DATABASES`, `REDIS`, `SECRET_KEY`.

- `ALLOWED_HOSTS`: list or tuple of FQDNs/IPs, at least one. It also sets `CSRF_TRUSTED_ORIGINS`. `['*']` allows all host values but accepts risk.
- `API_TOKEN_PEPPERS`: dict of numeric ID (start at 1) to pepper, used to hash v2 API tokens. Each must be at least 50 characters. NetBox runs without it, but v2 tokens are unavailable. Add more IDs later to rotate. Consider reading peppers from environment variables.
- `DATABASES`: needs a `default` entry with `NAME`, `USER`, `PASSWORD`, `HOST`, `PORT` (blank for 5432), `CONN_MAX_AGE` (300 default) and `ENGINE`. The old singular `DATABASE` is deprecated.
- `REDIS`: `tasks` and `caching` entries.
- `SECRET_KEY`: random salt, never used directly to encrypt secret data. It must be identical on all servers in a highly available setup so sessions persist.

Generate keys and peppers with:
```
python3 ../generate_secret_key.py
```

**Checklist**

1. Five parameters present.
2. Peppers at least 50 characters.
3. Same SECRET_KEY across web servers.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Required-parameters and install pages: the five required parameters, API_TOKEN_PEPPERS 50-character minimum, DATABASES keys and CONN_MAX_AGE, REDIS tasks/caching, SECRET_KEY on all servers, generate_secret_key.py. Removed: Nothing.

Method: documentation only; no commands were run.
