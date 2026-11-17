---
id: computing-software.web-development.strapi.policies
name: policies
category: computing-software
field: web-development
product: strapi
tags: [strapi, policies, authorization, policycontext, global-policy, routes]
level: practitioner
status: docs-checked
description: "Write Strapi policies that gate routes before the controller, and attach global, API or plugin policies by name."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/backend-customization/policies.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Policies

Functions that run before the controller on each request, mostly to secure business logic. Create with `strapi generate` or in:

- `./src/policies/` (global)
- `./src/api/[api-name]/policies/` (API)
- `./src/plugins/[plugin-name]/policies/` (plugin)

```js
module.exports = (policyContext, config, { strapi }) => {
  if (policyContext.state.user) { // if a session is open
    // go to next policy or reach the controller's action
    return true;
  }

  return false; // If you return nothing, Strapi considers you didn't want to block the request and will let it pass
};
```

`policyContext` wraps the controller context and works for both REST and GraphQL. Policies can be configured using a `config` object, passed as the second argument.

## Naming
- `global::policy-name`
- `api::api-name.policy-name`
- `plugin::plugin-name.policy-name`

```js
config: {
  policies: ['global::is-authenticated']
}
```

The Users & Permissions plugin exposes `plugin::users-permissions.isAuthenticated`. List available policies with `yarn strapi policies:list`.

Return `true` to allow, `false` to block; returning nothing lets the request through.

## Checked

2026-11-04: checked against the Strapi docs page Policies (backend-customization/policies). Confirmed: purpose, the three folder locations, `strapi generate`, handler signature and return behaviour, `policyContext` for REST and GraphQL, the three naming forms, `plugin::users-permissions.isAuthenticated`, `yarn strapi policies:list`. Reworded: the `config` argument sentence to match the page.

Method: documentation only; no commands were run.
