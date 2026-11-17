---
id: computing-software.cloud-infrastructure-engineering.google-cloud.iap-settings-reauthentication-and-sessions
name: iap-settings-reauthentication-and-sessions
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, identity-aware-proxy, iap-settings, iap-reauthentication, iap-session, cors, access-denied-page]
level: advanced
status: docs-checked
description: "Tune IAP per resource with gcloud iap settings: reauthentication method and max age, CORS preflight, login hints, custom access-denied pages and allowed domains."
sources: ["https://cloud.google.com/iap/docs/customizing", "https://cloud.google.com/iap/docs/configuring-reauth", "https://cloud.google.com/sdk/gcloud/reference/iap/settings/set"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IAP settings, reauthentication and sessions

IAP settings are hierarchical: org → folder → project → all web services → web service type → service → version.
IAP walks the hierarchy from the top and applies settings as found, so lower levels override higher ones.

## 1. Read the effective settings
```bash
gcloud iap settings get --project=<P>
gcloud iap settings get --project=<P> --resource-type=compute --service=<BACKEND_SERVICE>
gcloud iap settings get --project=<P> --resource-type=app-engine --service=admin
```

## 2. Set reauthentication for sensitive apps
```yaml
# reauth.yaml
accessSettings:
  reauthSettings:
    method: SECURE_KEY        # LOGIN | SECURE_KEY | ENROLLED_SECOND_FACTORS
    maxAge: 3600s             # user must reauthenticate after 1 h; minimum is 300s
    policyType: MINIMUM       # MINIMUM merges with lower levels (shorter maxAge, stronger method wins); DEFAULT lets a lower level replace it
  oauthSettings:
    loginHint: example.com    # verified Workspace domain; skips the account chooser
applicationSettings:
  accessDeniedPageSettings:
    accessDeniedPageUri: https://help.example.com/request-access
    generateTroubleshootingUri: true
```
```bash
gcloud iap settings set reauth.yaml --project=<P> --resource-type=compute --service=<BACKEND_SERVICE>
```
Methods: `LOGIN` = the user signs in again with login credentials; `SECURE_KEY` = the user's configured
security key; `ENROLLED_SECOND_FACTORS` = one of the user's enrolled second factors. When two levels
are merged, precedence is secure key > enrolled second factors > login.

`loginHint` and the custom access-denied page are documented as part of a paid enterprise security
subscription; the domain must be verified (a Workspace primary or secondary domain).
`loginHint` is not an access control.

## 3. CORS and API clients
Browsers send CORS preflight `OPTIONS` requests without credentials, so IAP answers them with an
error by default (`allow_http_options` defaults to false).
```yaml
access_settings:
  cors_settings:
    allow_http_options: true
```
IAP then passes `OPTIONS` through to your app, which must answer the preflight itself. Apply only
on services that serve cross-origin XHR.

## 4. Reauth cookie scope
After reauthentication IAP sets a cookie on the top-level private domain, so other IAP apps on that
domain (`bar.example.com` after `foo.example.com`) do not prompt again while it is valid. For
`myapp.appspot.com` the cookie domain is `myapp.appspot.com`, because `appspot.com` is a public domain.

## Gotchas
- `policyType: DEFAULT` at org level lets a lower level replace the org setting; use `MINIMUM` at the top.
- Reauth is a browser control: it is not supported for programmatic user access, service accounts and
  IAP for TCP are exempt, and it does not work with `allUsers`, external identities (OAuth, SAML)
  or Workforce Identity Federation identities.
- `SECURE_KEY` needs users to have a configured security key; enrol them first.

## Verify
- [ ] After `maxAge`, the browser is asked to reauthenticate with the configured method.
- [ ] `gcloud iap settings get` shows the expected effective `reauthSettings`.
- [ ] A denied user lands on the custom access-denied page.

## Checked
2026-10-31. Confirmed against the IAP "Customize IAP" and "IAP reauthentication" pages and the IAP v1
discovery document (ReauthSettings, AccessDeniedPageSettings, OAuthSettings): hierarchy and override
rule, reauth methods, MINIMUM/DEFAULT merge rules and method precedence, 300 s minimum `maxAge`,
cookie scope, reauth limitations, CORS default, `loginHint` and `generateTroubleshootingUri` fields.
Removed: Admin console "Google Cloud session control" path, `/_gcp_iap/clear_login_cookie`,
propagation delay and 401 claims (not in the pages).
Method: documentation only; no commands were run.
