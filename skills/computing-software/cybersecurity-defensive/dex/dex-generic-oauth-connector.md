---
id: computing-software.cybersecurity-defensive.dex.dex-generic-oauth-connector
name: dex-generic-oauth-connector
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [oauth, connector, claimmapping, userinfo]
level: advanced
status: docs-checked
description: "Use the Dex generic oauth connector for OAuth 2.0 providers without OIDC: tokenURL, authorizationURL, userInfoURL and claim key mapping."
sources:
  - https://dexidp.io/docs/connectors/oauth/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `oauth` connector works with standards-compliant OAuth 2.0 providers that have no dedicated Dex connector. The docs show Reddit:

```yaml
connectors:
- type: oauth
  id: reddit
  name: reddit
  config:
    clientID: $REDDIT_CLIENT_ID
    clientSecret: $REDDIT_CLIENT_SECRET
    redirectURI: http://127.0.0.1:5556/dex/callback
    tokenURL: https://www.reddit.com/api/v1/access_token
    authorizationURL: https://www.reddit.com/api/v1/authorize
    userInfoURL: https://www.reddit.com/api/v1/me
    scopes:
    - identity
    userIDKey: id
    claimMapping:
      userNameKey: user_name
      preferredUsernameKey: preferred_username
      groupsKey: groups
      emailKey: email
      emailVerifiedKey: email_verified
```

Defaults: `userIDKey` is `id`, `userNameKey` is `user_name`, `preferredUsernameKey` is `preferred_username`, `groupsKey` is `groups`, `emailKey` is `email`, `emailVerifiedKey` is `email_verified`.

Other options:

- `insecureSkipEmailVerified`: for providers that return no `email_verified`.
- `insecureSkipVerify`: skip SSL validation.
- `rootCAs`: list of files with certificates for the provider.

Gotcha: the keys name fields in the provider's user info JSON, so inspect the real response of `userInfoURL` before mapping.

Values starting with `$` are read from the environment, so use references such as `$REDDIT_CLIENT_SECRET` to keep secrets out of the file.

## Checked

2026-11-03: read against Dex docs, generic OAuth connector (https://dexidp.io/docs/connectors/oauth/).

Removed or corrected: Unconfirmed claims that three endpoints are required and about registering the callback.

Method: documentation only; no commands were run.
