---
id: computing-software.systems-network-administration.netbird.sso-cloud-providers
name: sso-cloud-providers
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, single-sign-on, oidc-providers, okta, cloud-plans]
level: intro
status: docs-checked
description: "Choose a NetBird Cloud single sign-on option: no-setup Google, Microsoft and GitHub logins, Okta, and OIDC providers like Keycloak or Authentik, with plan limits."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/team/single-sign-on/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
No extra setup: Google Workspace, Microsoft Entra ID, and GitHub, Google or Microsoft social accounts. Users click the matching button on the login page.

Okta: dedicated guide for SSO and provisioning.

OIDC-compliant IdPs (configure on the IdP side, each has a guide): Authentik, Keycloak, JumpCloud, Auth0, Duo Security, Zitadel, cidaas, AWS Cognito, Zoho, IIJ ID.

Plans: Free supports Google, Microsoft and social logins; OIDC-compliant providers need Team or higher.

Self-hosted: this guide is Cloud only. Self-hosted deployments follow the self-hosted identity provider docs and support OIDC providers in both Community Edition and Enterprise.

Getting started:
1. Check whether your provider works without setup.
2. For Okta or a listed provider, follow its guide.
3. For another OIDC provider, configure the IdP to integrate with NetBird.

## Checked

2026-11-04. Confirmed against the NetBird single sign-on page: no-setup logins, Okta guide, the ten listed OIDC providers, Team plan requirement, Free plan scope, self-hosted note. Removed the sign-in-at-login-page step and the closing pairing advice on sign-in domains and IdP sync, which the page does not state.
Method: documentation only; no commands were run.
