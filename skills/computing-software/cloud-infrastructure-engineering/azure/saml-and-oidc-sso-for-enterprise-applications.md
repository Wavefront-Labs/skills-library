---
id: computing-software.cloud-infrastructure-engineering.azure.saml-and-oidc-sso-for-enterprise-applications
name: saml-and-oidc-sso-for-enterprise-applications
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, entra-id, enterprise-applications, saml-sso, enterprise-app-sso, gallery-apps, saml-signing-certificate, user-assignment-required]
level: practitioner
status: docs-checked
description: "Configure SAML single sign-on for Entra enterprise apps: reply URL and identifier, claim transformations, signing certificate rollover and debugging."
sources: ["https://learn.microsoft.com/entra/identity/enterprise-apps/add-application-portal-setup-sso", "https://learn.microsoft.com/entra/identity-platform/saml-claims-customization", "https://learn.microsoft.com/entra/identity/enterprise-apps/tutorial-manage-certificates-for-federated-single-sign-on", "https://learn.microsoft.com/entra/identity/enterprise-apps/debug-saml-sso-issues"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SAML SSO for enterprise applications

**Goal:** a third-party app signs users in through Entra with the right claims, and the signing certificate never expires unnoticed.

## 1. Basic SAML configuration
- Set the **Reply URL (Assertion Consumer Service URL)** and **Sign on URL** from the app's own configuration guide. The **Identifier (Entity ID)** is typically a URL specific to the application; follow the app's guide to get the right value (for some gallery apps it is generated once you enter the other two).
- The Test button stays greyed out until the required attributes in Basic SAML Configuration are filled in and saved.

## 2. Claims
- The NameID format option **Persistent** makes the identity platform use Persistent as the nameID format.
- Claim transformations include `ExtractMailPrefix()` (removes the domain suffix from the email or user principal name, so `joe_smith` instead of `joe_smith@contoso.com`) and `ToLowercase()`; see the claims customization page for the full table.
- For group claims you select the group types to include: security groups, directory groups, or groups assigned to a particular application.
- A regex transformation can take up to five additional parameters.

## 3. Signing certificate
- Entra generates a self-signed certificate for a gallery app's SAML sign-on, valid for three years by default. You cannot change the expiry of a saved certificate; instead create a new one (its expiry defaults to three years from today and can be set to any date up to three years ahead).
- Rollover: select **New Certificate**, save, give the new certificate to the app, then at the agreed time open the ellipsis on the new row and choose **Make certificate active**. The old one becomes Inactive.
- Download formats: raw (binary) or Base64 certificate; gallery apps may also offer federation metadata XML. The per-tenant, per-application metadata URL can be ingested by apps that support it.
- Entra emails 60, 30 and 7 days before the certificate expires. The notification list takes up to five addresses (including the admin who added the app); use a distribution list to reach more people.

## 4. Debugging
- Use the **Test single sign-on** page. If sign-in fails, the My Apps Secure Sign-in Extension gathers the SAML request and response and shows resolution guidance; without it, use "Get resolution guidance" and a tool such as Fiddler to capture them.

## Verify
- [ ] Test sign-in succeeds with the expected claims.
- [ ] The certificate expiry date and notification emails are recorded.

## Checked

Method: docs-checked 2026-11-09 against the Learn pages for the SAML certificate tutorial, SAML claims customization, SSO setup and debug-saml-sso-issues (keyword checks of each page). Removed unconfirmed claims: default NameID mapping, the app-registration vs enterprise-app advice, Assignment required, Conditional Access and My Apps notes, the IdP-initiated sign-on URL rule, token refresh and Resource Graph expiry reporting.
