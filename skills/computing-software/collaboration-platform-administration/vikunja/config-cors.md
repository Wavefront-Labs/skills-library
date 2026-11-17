---
id: computing-software.collaboration-platform-administration.vikunja.config-cors
name: config-cors
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, cors-section, cors-origins, publicurl-required, separate-frontend-domain]
level: practitioner
status: docs-checked
description: "Understand why Vikunja needs service.publicurl when CORS is on, and how to set cors.origins or disable CORS for split frontend and API hosts."
sources:
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/install.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`cors.enable` defaults to true. By default it is enabled only for requests from the desktop application running on localhost.

`service.publicurl` is required when `cors.enable` is true. The install page says the same for each install method: set the public URL (`VIKUNJA_SERVICE_PUBLICURL` as an environment variable) or set `cors.enable` to `false`.

Other options:
- `cors.origins`: list of origins allowed to access the API; each must include the protocol (`http://` or `https://`) and the port, if any. Defaults: `http://127.0.0.1:*` and `http://localhost:*`.
- `cors.maxage`: seconds a preflight result may be cached (default 0).

If frontend and API are on separate domains or ports, adjust these settings accordingly.

For desktop client OIDC login the config reference says to allow redirects to `127.0.0.1`.

## Checked

2026-11-04: checked against config-raw.json (service.publicurl, cors.enable, cors.origins, cors.maxage, auth.openid note) and the install page. Removed the "unauthorized on non-standard port" symptom line (it is from the Docker guide, not these sources).

Method: documentation only; no commands were run.
