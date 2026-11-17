---
id: computing-software.cloud-infrastructure-engineering.rancher.auth-okta-saml-setup
name: auth-okta-saml-setup
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [okta, saml, acs, sp-initiated, assertion-encryption, metadata-xml, groups-field]
level: practitioner
status: docs-checked
description: "Integrate Okta with Rancher via SAML: ACS and audience URIs, attribute field mapping, encryption key pair, SP-initiated only."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/authentication-permissions-and-global-configuration/authentication-config/configure-okta-saml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Okta integration supports **Service Provider initiated logins only**. In Okta, create a SAML application with:

| Setting | Value |
|---|---|
| Single Sign on URL | `https://yourRancherHostURL/v1-saml/okta/saml/acs` |
| Audience URI (SP Entity ID) | `https://yourRancherHostURL/v1-saml/okta/saml/metadata` |

In Rancher open **Users & Authentication > Auth Provider > Okta** and complete the form. The field names refer to attribute names from your SAML attribute statements:

- Display Name Field, User Name Field, UID Field (unique per user) and Groups Field (the attribute from the group attribute statement);
- Rancher API Host, the URL of your Rancher server;
- a Private Key / Certificate pair used for assertion encryption;
- Metadata XML, the Identity Provider metadata file from the Okta application's Sign On section.

The page suggests generating the key pair with openssl, for example:

```
openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout myservice.key -out myservice.crt
```

Click **Enable**; Rancher redirects to the IdP login page and you authenticate to validate the setup. Okta returns a SAML assertion that includes the user's groups, so group-based permissions in Rancher work off that attribute.

If you configure Okta without OpenLDAP you cannot search or look up users or groups. Users and groups are then not validated when you assign permissions, exact user IDs (the UID Field value) must be typed correctly, and groups must be picked from the dropdown. The page describes adding an OpenLDAP backend for user and group search. If a pop-up seems not to appear, disable the pop-up blocker for the Rancher domain.

## Checked

2026-11-09. Read the cited Configure Okta (SAML) page in full and checked every claim against it (SP-initiated only, ACS and audience values, form fields, openssl example, Enable flow, SAML caveats). The yourRancherHostURL values are the page's placeholders. Removed the reference to another skill and the blanket statement about SAML lookup, which the page ties to Okta without OpenLDAP.

Method: documentation only; no commands were run.
