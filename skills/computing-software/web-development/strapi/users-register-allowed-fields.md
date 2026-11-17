---
id: computing-software.web-development.strapi.users-register-allowed-fields
name: users-register-allowed-fields
category: computing-software
field: web-development
product: strapi
tags: [strapi, users-permissions, registration, allowedfields, user-model, signup]
level: practitioner
status: docs-checked
description: "Accept extra User fields on Strapi registration by listing them in users-permissions config.register.allowedFields."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/features/users-permissions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Registration fields

If you add fields to the User model that must be accepted at registration, list them in `config.register` of the plugin config, otherwise they are not accepted.

```js
module.exports = ({ env }) => ({
  // ...
  "users-permissions": {
    config: {
      register: {
        allowedFields: ["nickname"],
      },
    },
  },
  // ...
});
```

## Context
- End users are a content-type (`User`), managed in the Content Manager with fields Username, Email, Password, Confirmed, Blocked, Role.
- If "Enable signups" is on in advanced settings, a new User entry is created automatically when someone registers.
- A user without a role gets the "Default role" from advanced settings.
- The default (`create-strapi-app`) config also uses `jwtManagement: 'refresh'`; see `computing-software.web-development.strapi.users-permissions-jwt`.

## Checked

Checked 2026-11-04 against the Strapi Users & Permissions page (registration configuration, admin panel usage, advanced settings) and the CLI page (security defaults for new projects). Nothing removed.

Method: documentation only; no commands were run.
