---
id: computing-software.cloud-infrastructure-engineering.google-cloud.custom-oauth-clients-for-iap
name: custom-oauth-clients-for-iap
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, identity-aware-proxy, iap-oauth-client, iap-custom-oauth, oauth-consent-screen, oauth-brand, iap-settings]
level: practitioner
status: docs-checked
description: "Choose Google-managed vs custom OAuth clients for IAP, configure the consent screen, create the client and redirect URI, and apply it with gcloud iap settings."
sources: ["https://cloud.google.com/iap/docs/custom-oauth-configuration", "https://cloud.google.com/iap/docs/sharing-oauth-clients"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom OAuth clients for IAP

By default IAP uses a **Google-managed OAuth client**: Google configures and manages it, it serves
internal users of your organization only, and it supports the browser flow only (an app using it
can still be reached programmatically through a separate client in the `programmatic_clients`
setting, or a service account JWT). Use a **custom OAuth client** to:
- manage access for external users outside your organization;
- protect web apps in projects that are not in a Google Cloud organization;
- show your own brand on the consent screen (custom branding appears only after Google verification).

With a custom client you create and manage the credentials, including storing the client secret safely.

## Custom client
1. Google Auth Platform → Branding → Get started: app name, user support email, Audience
   (Internal or External), contact email.
2. Create the client, either:
   - APIs & Services → Credentials → Create Credentials → OAuth client ID → Web application, then add
     the authorized redirect URI `https://iap.googleapis.com/v1/oauth/clientIds/<CLIENT_ID>:handleRedirect`; or
   - in the IAP page, resource → Settings → Custom OAuth → Auto Generate Credentials (IAP creates the
     client and adds the redirect URI; download the credentials JSON and secure or delete it).
3. Apply it to IAP:
   ```yaml
   # iap-oauth.yaml
   accessSettings:
     oauthSettings:
       clientId: <CLIENT_ID>
       clientSecret: <SECRET>
   ```
   ```bash
   gcloud iap settings set iap-oauth.yaml --project=<P>
   ```
   Use `--folder` or `--organization` instead of `--project` to give every service under that level the
   same branding, or add `--resource-type` (`app-engine`, `backend-services`, `cloud-run`, `compute`,
   `forwarding-rule`, `iap_web`) with `--service` (and `--region` for Cloud Run) for one service.

The page recommends the legacy per-resource configuration for App Engine and backend services,
because services configured through IAP settings do not show in the IAP UI. The legacy load balancer
form is `gcloud compute backend-services update <BACKEND> --global --iap=enabled,oauth2-client-id=<ID>,oauth2-client-secret=<SECRET>`.

## Gotchas
- Configure the branding page before creating the client.
- The auto-generated credentials file holds the client secret: secure or delete it.

## Verify
- [ ] First visit to the app after configuring the consent screen shows it; `gcloud iap settings get` shows the client ID.

## Checked
2026-10-31. Confirmed against "Use custom OAuth clients with IAP": managed vs custom comparison, reasons
to use a custom client, branding steps, redirect URI, auto-generate option, `accessSettings.oauthSettings`
YAML, resource types, legacy backend-service command. Removed: Chrome Enterprise Premium reason, Secret
Manager rotation advice, "Testing status" 7-day token note, re-authentication on client change and the
oauth-brands deprecation section (its page returned 404).
Method: documentation only; no commands were run.
