---
id: computing-software.devops-ci-cd.backstage.auth-service-to-service
name: auth-service-to-service
category: computing-software
field: devops-ci-cd
product: backstage
tags: [service-to-service, plugin-to-plugin, external-access, backstage]
level: advanced
status: docs-checked
description: "Secure plugin-to-plugin and external caller access with the auth and httpAuth services and static tokens."
sources:
  - https://backstage.io/docs/auth/service-to-service-auth
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Backend plugins using the backend system and the `auth` and `httpAuth` core services are secure by default. They generate self-signed tokens automatically for calls to other backend plugins, and receivers verify them against the caller's public key set endpoint.

A plugin calling another acquires a token like this:

```ts
const credentials = await httpAuth.credentials(req);
const { token } = await auth.getPluginRequestToken({
  onBehalfOf: credentials,
  targetPluginId: 'catalog',
});
```

and sends it in the `Authorization: Bearer` header.

For external callers, such as CI jobs or scripts, the docs describe several mechanisms:

- Static tokens (`type: static`) under `backend.auth.externalAccess`, each with `options.token` and `options.subject`.
- JWKS tokens (`type: jwks`) with `options.url`, `issuer`, `algorithm`, `audience` and `subjectPrefix`; subjects get the prefix `external:`.
- Custom handlers added through `externalTokenHandlersServiceRef`.

```yaml
backend:
  auth:
    externalAccess:
      - type: static
        options:
          token: ${CI_BACKSTAGE_TOKEN}
          subject: ci-job
        accessRestrictions:
          - plugin: catalog
```

Subjects must be strings without whitespace and identify the caller in the credentials that plugins receive. Each `accessRestrictions` entry requires `plugin`; optional `permission` and `permissionAttribute` (for example `action: create, read`) narrow it further. Without `accessRestrictions` a method has unlimited access to all plugins, so set them whenever possible.

For special cases such as worker nodes on read-only database replicas, plugin-to-plugin keys can be static under `backend.auth.pluginKeyStore` (`type: static`); the first key signs and later keys are only used for validation. `backend.auth.dangerouslyDisableDefaultAuthPolicy` disables issuing and verification of tokens between backends and is a last resort.

## Checked

2026-11-03. Confirmed against the Backstage Service to Service Auth page: `getPluginRequestToken` call, Bearer header, static and JWKS external access options, `accessRestrictions` fields, `pluginKeyStore` static keys. Removed: legacy-token bullet, token rotation advice and the key-generation troubleshooting hint (not in the page).

Method: documentation only; no commands were run.
