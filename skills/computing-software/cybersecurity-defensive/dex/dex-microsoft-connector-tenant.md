---
id: computing-software.cybersecurity-defensive.dex.dex-microsoft-connector-tenant
name: dex-microsoft-connector-tenant
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [microsoft, connector, tenant, azure-ad]
level: practitioner
status: docs-checked
description: "Control which Microsoft accounts can log in to Dex using the tenant parameter: common, consumers, organizations or a tenant id."
sources:
  - https://dexidp.io/docs/connectors/microsoft/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Microsoft connector authenticates users through their Microsoft account. On refresh Dex re-queries Microsoft, storing read-only Microsoft access and refresh tokens in its storage.

```yaml
connectors:
- type: microsoft
  id: microsoft
  name: Microsoft
  config:
    clientID: $MICROSOFT_APPLICATION_ID
    clientSecret: $MICROSOFT_CLIENT_SECRET
    redirectURI: http://127.0.0.1:5556/dex/callback
    tenant: organizations
```

The `tenant` value decides which accounts can authenticate:

- `common` (default): personal and business/school accounts.
- `consumers`: personal accounts only.
- `organizations`: business/school accounts only.
- `<tenant uuid>` or `<tenant name>`: only accounts belonging to that tenant.

Register the application callback as `(dex issuer)/callback`, for example `https://auth.example.com/dex/callback` when Dex listens at a non-root path.

Gotchas:

- Group lookups require `tenant` to be a tenant uuid or name, not `common`, `consumers` or `organizations`.
- Pick `organizations` or a specific tenant for company logins, otherwise any Microsoft personal account can authenticate.

Check: log in with a personal account while `tenant: organizations` is set and confirm it is rejected.

Dex keeps these tokens in its backing datastore, so protect the storage backend with transport security and access control.

## Checked

2026-11-03: read against Dex docs, Microsoft connector (https://dexidp.io/docs/connectors/microsoft/).

Removed or corrected: Nothing removed.

Method: documentation only; no commands were run.
