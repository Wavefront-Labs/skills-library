---
id: computing-software.web-development.appwrite.appwrite-oauth2-login
name: appwrite-oauth2-login
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, auth, oauth2, social-login, providers]
level: practitioner
status: docs-checked
description: "Enable an OAuth2 provider in the Console and start a provider login from a client app with success and failure redirects."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/oauth2/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: sign in with a third-party account.

Console setup (Auth > Settings):
1. Open the provider and toggle it on.
2. Create an OAuth2 app on the provider's developer platform.
3. Copy the provider's credentials into the OAuth2 Settings modal.
4. Configure the redirect URL in the provider's platform using the URL shown in that modal.

Start the login from the client: `account.createOAuth2Session({ provider: OAuthProvider.Github, success: 'https://example.com/success', failure: 'https://example.com/failed', scopes: ['repo', 'user'] })`. The user is redirected to the provider, then back to your success or failure URL. The optional `scopes` are provider-specific and describe what the session may access; check the provider's docs for valid values.

Mobile: for Flutter on Android add an activity with the scheme `appwrite-callback-<PROJECT_ID>` to `AndroidManifest.xml`; for Apple add the same scheme under `CFBundleURLSchemes` in `Info.plist` (UIKit also needs a hook in `SceneDelegate.swift`).

OAuth2 login creates an identity, so a user can connect several providers to one account.

Provider tokens: read the current session with `account.getSession({ sessionId: 'current' })`; it carries `provider`, `providerUid`, `providerAccessToken` and `providerAccessTokenExpiry`. Refresh an expired token with `account.updateSession` instead of before every request.

OAuth2 is not available in GraphQL.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/auth/oauth2. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed the redirect-mismatch Gotcha (the page does not state it as the usual cause); replaced Verify with the session fields the page lists and the updateSession refresh note; added that OAuth2 is not available in GraphQL.

Method: documentation only; no commands were run.
