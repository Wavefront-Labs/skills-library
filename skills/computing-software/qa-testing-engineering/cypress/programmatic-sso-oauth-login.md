---
id: computing-software.qa-testing-engineering.cypress.programmatic-sso-oauth-login
name: programmatic-sso-oauth-login
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [programmatic-login, cypress-authentication, oauth, cy-session, sso-testing]
level: practitioner
status: docs-checked
description: "Log in programmatically in Cypress against OAuth/OIDC providers (Auth0, Okta, Cognito, Azure AD): token requests with cy.request, storing tokens, and caching with cy.session."
sources:
  - https://docs.cypress.io/api/commands/session
  - https://docs.cypress.io/api/commands/env
  - https://docs.cypress.io/api/cypress-api/expose
  - https://docs.cypress.io/app/guides/authentication-testing/auth0-authentication
  - https://docs.cypress.io/app/guides/authentication-testing/okta-authentication
  - https://docs.cypress.io/app/guides/authentication-testing/amazon-cognito-authentication
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Programmatic SSO/OAuth login (Cypress)

**Goal:** authenticate in milliseconds without driving the identity provider's UI in every test.

## Approach
1. Get tokens directly from the IdP's token endpoint (test tenant/app with a grant suited to automation).
2. Put them where your app expects them (localStorage, cookie, or your backend session endpoint).
3. Cache with `cy.session`.

## Example: OIDC resource-owner password grant (test tenant only)
```js
Cypress.Commands.add('loginByOidc', (username, password) => {
  cy.session(['oidc', username], () => {
    cy.request({
      method: 'POST',
      url: `${Cypress.expose('idp_url')}/oauth/token`,
      form: true,
      body: {
        grant_type: 'password', username, password,
        client_id: Cypress.expose('client_id'), audience: Cypress.expose('audience'), scope: 'openid profile email',
      },
      log: false,
    }).then(({ body }) => {
      window.localStorage.setItem('auth', JSON.stringify({ accessToken: body.access_token, idToken: body.id_token }));
    });
  }, {
    validate() { cy.request({ url: '/api/me', failOnStatusCode: true }); },
    cacheAcrossSpecs: true,
  });
});
```
In Cypress 16 `Cypress.env()` was removed: put public values (domain, client id, audience) under `expose` in the config and read them with `Cypress.expose()`; read secrets (passwords, client secrets) under `env` with `cy.env(['KEY']).then(({ KEY }) => ...)`. The `expose` values are visible to application code, so never put secrets there.

If the app uses a server-side session, call the backend's own login/token-exchange endpoint instead so it sets the cookie.

## Provider notes
- **Auth0**: the Cypress guide enables the "Password" grant type on the application (unchecked by default) and sets the tenant "Default Audience" and "Default Directory" (`Username-Password-Authentication`); it posts to `/oauth/token` with `grant_type: 'password'`.
- **Okta**: the guide posts to the Authentication API (`/api/v1/authn`) for a session token, then signs in with the Okta auth SDK using that `sessionToken`.
- **Amazon Cognito**: the guide uses the AWS Amplify auth library with `cy.session()`.
- **Microsoft Entra ID** and **Google**: see the Cypress guides for each; confirm the flow your tenant allows (MFA or federation can block password-based flows).

## Security
- Use dedicated test users and a non-production tenant; keep secrets in CI environment variables read with `cy.env()`, and use `log: false` on sensitive commands.
- Never enable password grant on production apps for testing.

## Keep one real UI login test
Programmatic login skips the login page; have one test that drives the full redirect flow with `cy.origin()`.

## Verify
Later logins restore the cached session quickly, `validate()` catches expired sessions, and no secrets appear in the command log or videos.

## Checked
Checked against the Cypress documentation sources (cypress-io/cypress-documentation, docs/, last commit 2026-10-24, which document Cypress 16; latest release v16.2.0). Confirmed: `cy.session(id, setup, options)` with `validate` and `cacheAcrossSpecs` (default false), cookies, localStorage and sessionStorage are preserved after setup and validate, `Cypress.env()` removal in Cypress 16 with `cy.env()` and `Cypress.expose()` replacements and the public-values-only rule, Auth0 password grant settings and `/oauth/token` request, Okta `/api/v1/authn` plus `sessionToken`, Cognito via Amplify, `cy.origin()`. The example command was not run; the `/oauth/token` request shape follows the Auth0 guide and other providers differ.

Method: documentation only; no commands were run.
