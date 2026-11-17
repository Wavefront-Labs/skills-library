---
id: computing-software.networking-hardware-and-wireless.traefik.provider-file
name: provider-file
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, file-provider, providers, directory, watch, dynamic-configuration]
level: practitioner
status: docs-checked
description: "Load Traefik routing configuration from files with the file provider using filename or directory and live watching."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/install-configuration/providers/others/file.md
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/dynamic-configuration-methods.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# provider file
The file provider reads routing configuration from YAML or TOML. Options: `filename` or `directory` (mutually exclusive), `watch` (default true, reload on change) and `debugLogGeneratedTemplate`. Every provider also honours `providers.providersThrottleDuration`, the minimum wait after a reload before the next refresh event is accepted.

```yaml
# install configuration
providers:
  file:
    directory: "/etc/traefik/dynamic"
    watch: true
```
```yaml
# /etc/traefik/dynamic/app.yml
http:
  routers:
    app:
      rule: "Host(`app.example.com`)"
      service: app
  services:
    app:
      loadBalancer:
        servers:
          - url: "http://10.0.0.11:8080"
```
Gotchas: `filename` and `directory` are mutually exclusive and the reference recommends `directory`. If the link between file systems is broken, for example when a single file is bind-mounted into a container, a change to the source is not reported to the linked file; set `directory` to the parent directory and mount that instead. `providers.providersThrottleDuration` defaults to 2s and applies to each provider independently.

## Checked
2026-11-03. Confirmed against the Traefik file provider reference page and the dynamic configuration methods page: `filename`, `directory`, `watch` (default true), `debugLogGeneratedTemplate`, `providersThrottleDuration` and the mounted-directory guidance. Removed: the malformed-file claim, the atomic-save claim and the API Verify step.
Method: documentation only; no commands were run.


