---
id: computing-software.cybersecurity-defensive.splunk.splunk-saml-and-ldap-authentication
name: splunk-saml-and-ldap-authentication
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, splunk-saml-authentication, saml, ldap, authentication-conf, role-mapping, sso, splunk-platform-admin]
level: practitioner
status: draft
description: "Configure Splunk Enterprise SAML (Entra ID, Okta) and LDAP authentication with role mapping, local admin fallback and the scripted-auth needs for scheduled searches."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/Security/HowSAMLSSOworks", "https://docs.splunk.com/Documentation/Splunk/latest/Security/ConfigureSSOAzureAD", "https://docs.splunk.com/Documentation/Splunk/latest/Security/SetupuserauthenticationwithLDAP"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Splunk SAML and LDAP authentication

## SAML
1. In the IdP, create a SAML app: ACS `https://<sh>:8000/saml/acs`, entity ID matching Splunk's
   `entityId`, send a group/role claim (`http://schemas.microsoft.com/ws/2008/06/identity/claims/groups`
   or a custom `role` attribute) plus `realName` and `mail`.
2. Splunk: Settings > Authentication methods > SAML; upload IdP metadata; set attribute query
   or not. Resulting `authentication.conf`:
```
[authentication]
authType = SAML
authSettings = saml_idp
[saml_idp]
entityId = splunk-prod
idpSSOUrl = https://login.microsoftonline.com/<TENANT_ID>/saml2
signAuthnRequest = true
signedAssertion = true
[roleMap_SAML]
admin = <ADMIN_GROUP_ID>
ess_analyst = <SOC_GROUP_ID>
```
3. Search head cluster: identical config on all members (deploy via deployer) and the IdP must
   accept each member's ACS or the load balancer URL as one SP.

## Scheduled searches and SAML
Splunk cannot query the IdP for a user's roles when the user is offline; scheduled searches owned
by SAML users fail role resolution unless you configure **scripted authentication** (Entra/Okta
scripts shipped with Splunk) or attribute query, or reassign searches to a service/nobody owner.

## LDAP
Settings > Authentication methods > LDAP: LDAPS (port 636), bind DN service account, user base DN,
group base DN, `groupMemberAttribute = member`, nested groups need `nestedGroups = 1` (AD).
Map groups to roles. Use LDAP only when SAML is unavailable; it adds a hard dependency on DCs.

## Fallback
Keep one local `admin` account with a vaulted password; reach the local login with
`https://<sh>:8000/en-US/account/login?loginType=splunk` when the IdP is down.

## Gotchas
- Clock skew over a few minutes breaks assertion validation.
- Entra sends group object IDs, not names; map IDs, or configure group name claims.
- Users with no mapped role get a login loop; check `splunkd.log` component `SAMLAuthProvider`.

## Verify
Log in as a test user in each mapped group and confirm `| rest /services/authentication/current-context`
shows expected roles; confirm local admin login URL works.
