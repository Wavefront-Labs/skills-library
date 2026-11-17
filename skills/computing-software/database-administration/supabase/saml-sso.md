---
id: computing-software.database-administration.supabase.saml-sso
name: saml-sso
category: computing-software
field: database-administration
product: supabase
tags: [saml, sso, supabase-sso, attribute-mapping, identity-provider]
level: advanced
status: docs-checked
description: "Set up SAML 2.0 SSO in Supabase with the CLI: add, update, remove providers, endpoints, attribute mapping JSON, limits and RLS claims."
sources:
  - https://supabase.com/docs/guides/auth/sso/auth-sso-saml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: connect an enterprise identity provider (needs CLI v1.46.4 or later).

```bash
supabase sso add --type saml --remote=<your-project> --metadata-url 'https://company.com/idp/saml/metadata' --domains company.com
supabase sso add --type saml --remote=<your-project> --metadata-file /path/to/saml/metadata.xml --domains company.com
supabase sso update <provider-uuid> --remote=<your-project> --attribute-mapping-file /path/to/attribute/mapping.json
supabase sso remove <provider-id> --remote=<your-project>
supabase sso list --remote=<your-project>
supabase sso show <provider-id> --remote=<your-project>
supabase sso info --remote=<your-project>
```

Add `-o json` to `show` for JSON. Client: `supabase.auth.signInWithSSO({ domain: 'company.com' })`, with `options: { redirectTo }` and a `/callback` endpoint that exchanges the code.

Endpoints for the IdP: metadata `https://<project>.supabase.co/auth/v1/sso/saml/metadata` (add `?download=true` to download), ACS `/auth/v1/sso/saml/acs`, SLO `/auth/v1/sso/slo`. NameID must be `emailAddress` or `persistent`.

Rules: SAML 2.0 is disabled by default and needs Pro or higher; only users with write access can change providers. EntityID cannot be changed (a new one means a new provider). SLO is unsupported, so use session timeouts. SSO users are not identity-linked, so emails are not unique; key by UUID. Removing a provider logs its users out immediately. Assertions without email are rejected. IdP-initiated flows are incompatible with PKCE. Prefer a Metadata URL so keys can rotate.

Attribute mapping: `{"keys":{"email":{"name":"mail"}}}`; use `"array": true` for multi-value, `default` for missing values, `names` for alternates.

RLS: `auth.jwt()#>>'{amr,0,method}'` returns `sso/saml`; `{amr,0,provider}` the provider UUID.

## Checked

Confirmed against the page: CLI v1.46.4, supabase sso add/update/remove/list/show/info and their flags, -o json, metadata and ACS and SLO URLs, NameID requirement, Pro plan and disabled by default, write access, EntityID immutability, SLO unsupported, no identity linking, immediate logout on removal, email requirement, PKCE and IdP-initiated incompatibility, attribute mapping keys (array, default, names), JWT amr expressions. Nothing removed.

Method: docs-checked 2026-11-09 against the Supabase docs source for guides/auth/enterprise-sso/auth-sso-saml (apps/docs/content on GitHub master), read in full.
