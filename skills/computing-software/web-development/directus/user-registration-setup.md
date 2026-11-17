---
id: computing-software.web-development.directus.user-registration-setup
name: user-registration-setup
category: computing-software
field: web-development
product: directus
tags: [user-registration, public-registration, register-endpoint, role-policy]
level: practitioner
status: docs-checked
description: "Enable public user registration in Directus: create a role and read policy, turn on registration, then register via Studio or POST /users/register."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/getting-started/5.authenticate-user.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
1. In settings, open User Roles and create a role named "User" (applied to new registrants).
2. Inside the role, create a policy (example "Read Posts") with a **Read** permission on the target collection.
3. In settings enable User Registration, select that role, and (for the quickstart) disable Verify Email.

Register through the API:

```bash
curl --request POST \
  --header 'Content-Type: application/json' \
  --data '{ "email": "hello@example.com", "password": "d1r3ctu5" }' \
  --url 'https://directus.example.com/users/register'
```

GraphQL: `mutation { users_register(email: "...", password: "...") }`. SDK: `client.request(registerUser(email, password))` with `createDirectus(url).with(rest())`.

Notes:
- After logging out of the Studio the Sign In screen shows a Sign Up option.
- With Verify Email disabled the user can log in immediately.

The page says the new user then appears in the user directory.

## Checked

2026-11-04: role and policy setup, User Registration setting with Verify Email disabled, Sign Up option, and the REST, GraphQL and SDK registration calls confirmed against the Directus Authenticate a User page. Replaced a Verify line with the page's statement.

Method: documentation only; no commands were run.
