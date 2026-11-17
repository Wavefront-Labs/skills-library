---
id: computing-software.collaboration-platform-administration.matrix-synapse.oidc-provider-quirks-keycloak-azure-github
name: oidc-provider-quirks-keycloak-azure-github
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, oidc, keycloak, azure-ad, github, auth0, authentik, subject-claim, discover, client-auth-method]
level: advanced
status: docs-checked
description: "Provider-specific Synapse OIDC settings for Keycloak, Azure AD, GitHub, Gitea, Auth0, Authentik and Facebook, including subject_claim and discover false."
sources:
  - https://element-hq.github.io/synapse/latest/openid.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The OIDC page gives per-provider examples. The recurring differences are worth knowing before you copy one.

**Non-OIDC OAuth2 providers lack `sub`.** GitHub and Gitea are plain OAuth2, and their user endpoint returns no `sub`, so set `subject_claim: "id"` under `user_mapping_provider.config`. GitHub also needs `discover: false` with explicit `authorization_endpoint`, `token_endpoint`, `userinfo_endpoint` (`https://api.github.com/user`) and scope `read:user`; its `localpart_template` is `{{ user.login }}`. Mastodon and Twitter use `subject_template` instead, for example `{{ user.id }}`. Twitter also needs Synapse 1.75.0 or later and `pkce_method: "always"`.

**Discovery off.** Facebook's discovery document excludes the `code` response type that Synapse relies on, so the example sets `discover: false` and lists the URIs manually, including `jwks_uri`.

**Client auth method.** GitLab, Gitea, Forgejo, Twitch and Apple use `client_auth_method: "client_secret_post"`; Apple builds its secret from a key file with `client_secret_jwt_key` (`key_file`, `jwt_header` with `alg: ES256` and `kid`, `jwt_payload` with `iss` set to the Team ID). XWiki uses `client_auth_method: none`.

**Azure AD.** Register an app, set the redirect URI to the callback, note the tenant ID, and set `issuer` to `https://login.microsoftonline.com/<tenant id>/v2.0` plus explicit endpoints; the mapping uses `{{ user.preferred_username.split('@')[0] }}`.

**Auth0.** Add a rule that puts a `preferred_username` claim into the ID token.

**Authentik.** Use RSA signing keys; ECC keys do not work, and the provider must have a signing key and no encryption key.

**Keycloak.** Client access type `confidential`, valid redirect URI set to the callback, and optionally the backchannel logout URL with session required, plus `backchannel_logout_enabled: true` in Synapse.

**Dex over plain HTTP** needs `skip_verification: true`. Where userinfo is not in the ID token (GitLab, Django OAuth Toolkit, Shibboleth), set `user_profile_method: "userinfo_endpoint"`.

## Checked

Method: docs-checked 2026-11-09 against docs/openid.md (Synapse develop branch, raw markdown, read in full).
