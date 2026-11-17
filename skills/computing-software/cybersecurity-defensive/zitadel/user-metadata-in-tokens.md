---
id: computing-software.cybersecurity-defensive.zitadel.user-metadata-in-tokens
name: user-metadata-in-tokens
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, user-metadata, claims, userinfo, id-token, scopes]
level: practitioner
status: docs-checked
description: "Read ZITADEL user metadata from the userinfo endpoint or inside the ID token using the metadata scope, and decode its base64 values."
sources:
  - https://zitadel.com/docs/guides/manage/customize/user-metadata
  - https://zitadel.com/docs/apis/openidoauth/scopes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
User metadata is key-value data attached to a user, for example a contract number or internal ID. Set it in the console or with the SetUserMetadata call of the User Service API (the caller needs the user.write permission).

To get it for the logged-in user, request the reserved scope `urn:zitadel:iam:user:metadata`. Without that scope the response contains user data but no metadata object.

Userinfo: call the endpoint with the access token.

```bash
curl --request GET \
  --url "https://${CUSTOM_DOMAIN}/oidc/v1/userinfo" \
  --header "Authorization: Bearer $ACCESS_TOKEN"
```

The metadata arrives in the reserved claim `urn:zitadel:iam:user:metadata` as key-value pairs. Values are base64 encoded, so `MTIzNA` decodes to `1234`. This method is the preferred one with opaque tokens, since the call also confirms the token is valid.

ID token: enable "User Info inside ID Token" in the application's settings, then request a new token with the scope.

To manage metadata of users other than the one logged in, use the UserService API instead of tokens.

Typical uses are linking a user to an internal identifier, saving custom data at registration, and routing upstream traffic by user attribute.

## Checked

2026-11-08. Read in full: the user metadata guide and the scopes page. Corrected the API name: SetUserMetadata is in the User Service API.

Method: documentation only; no commands were run.
