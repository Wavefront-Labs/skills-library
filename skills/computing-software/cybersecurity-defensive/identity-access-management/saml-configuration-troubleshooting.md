---
id: computing-software.cybersecurity-defensive.identity-access-management.saml-configuration-troubleshooting
name: saml-configuration-troubleshooting
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [sso, saml-troubleshooting, saml, federation, assertions, certificates, idp-sp, entra-id, saml-sso-troubleshooting, saml-sso-troubleshooting]
level: practitioner
status: docs-checked
description: "Troubleshoot SAML 2.0 SSO with Entra ID and Okta: values that must match, reading the SAML request and response, signing certificates, and the Entra test flow."
sources: ["https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/debug-saml-sso-issues", "https://help.okta.com/en-us/content/topics/apps/apps_app_integration_wizard_saml.htm"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# SAML configuration and troubleshooting

**Goal:** set up SAML SSO between an identity provider (IdP) and a service provider (SP, the app) correctly, and
diagnose failures by comparing the request and response against the configuration on both sides.

## Test first (Entra ID)
In the Entra admin center: Entra ID > Enterprise apps > All applications > the app > Single sign-on > SAML,
then use the Test single sign-on step (the Test button stays greyed out until the required attributes in Basic
SAML Configuration are saved). Success means Entra issued a SAML response and the app accepted it.

## Errors on the company sign-in page (request-side)
Gather the error message and the SAML request. The My Apps Secure Sign-in Extension (Chrome, Edge) collects both
and shows resolution guidance; without it, paste the error into Get resolution guidance and use a tool such as
Fiddler to capture traffic. Then verify:
- the destination in the request matches the SAML single sign-on service URL from Entra ID;
- the issuer in the request equals the identifier configured for the app in Entra ID (Entra uses it to find the app);
- `AssertionConsumerServiceURL` is where the app expects the token (configurable in Entra, not mandatory when it is in the request).
Keep the CorrelationID and Timestamp from the error for support cases.

## Errors on the application page (response-side)
Entra issued a token but the app rejected it. Retrieve the SAML response (extension, or Fiddler) and inspect:
- the NameID value and format (the user's unique identifier);
- the claims issued in the token;
- the certificate used to sign the token.
Then compare with what the app expects; if still failing, ask the app vendor what is missing from the response.
For gallery apps, check every step of the app's integration tutorial was followed.

## Okta
Create via Admin Console > Applications > Create App Integration > Classic experience > SAML 2.0. "Preview the
SAML Assertion" shows the XML generated from your settings. After creation, configure the app to verify signed
SAML assertions and trust Okta as IdP using the SAML Signing Certificates section on the Sign On tab (Manage
signing certificates).

## Security settings
Verify assertion signatures at the SP using the IdP's signing certificate, and keep the SP's copy of that
certificate current whenever the IdP certificate changes.

## Verify
Run the test with a user who is allowed and one who is not assigned; the second must fail.

## Checked
2026-11-01. Confirmed against Microsoft Learn "Debug SAML-based single sign-on to applications" and Okta's "Create SAML app integrations". Removed: AADSTS error-code mappings, `sts.windows.net` issuer example, assertion element names and clock-skew guidance, SAML-tracer, certificate lifetime figure, and general hardening advice not stated on these pages. The OASIS SAML core PDF text did not extract usable matches and is not cited.
Method: documentation only; no commands were run.
