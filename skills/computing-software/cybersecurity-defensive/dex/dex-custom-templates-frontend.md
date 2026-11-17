---
id: computing-software.cybersecurity-defensive.dex.dex-custom-templates-frontend
name: dex-custom-templates-frontend
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [templates, frontend, theme, branding]
level: practitioner
status: docs-checked
description: "Customise Dex login pages with frontend.dir, frontend.issuer, frontend.extra and the extra template function."
sources:
  - https://dexidp.io/docs/guides/templates/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dex lets you replace its HTML templates and pass arbitrary data to them.

Steps from the docs:

1. Copy the contents of the `web` directory into a new directory.
2. Customise the templates, keeping all existing variables so Dex keeps working.
3. Render values from `frontend.extra` in templates with `{{ "your_key" | extra }}`.
4. Set `frontend.dir` to your web directory, or set the `DEX_FRONTEND_DIR` environment variable.
5. Optionally add custom data under `frontend.extra`.
6. Optionally set `frontend.issuer` to change the Dex title and the "Log in to" tag.
7. Optionally create a custom theme in the `themes` directory.

```yaml
frontend:
  dir: /path/to/custom/web
  issuer: my-dex
  extra:
    tos_footer_link: "https://example.com/terms"
    client_logo_url: "../theme/client-logo.png"
    foo: "bar"
```

Test by running Dex with a valid configuration and walking through a login flow.

Gotchas:

- Removing template variables can break the login flow, so only add to or restyle them.
- Keys under `extra` are your own data, referenced by name in templates.

Check: load the login page and confirm the footer link and logo from `extra` render.

## Checked
2026-11-09: read the Dex Customizing Dex Templates guide in full; the steps, `frontend.dir`, `DEX_FRONTEND_DIR`, `frontend.issuer`, `frontend.extra`, the `extra` template function and the example config all match.
Method: documentation only; no commands were run.
