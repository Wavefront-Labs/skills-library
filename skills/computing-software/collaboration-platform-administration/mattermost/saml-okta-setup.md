---
id: computing-software.collaboration-platform-administration.mattermost.saml-okta-setup
name: saml-okta-setup
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [saml, okta, sso, assertion-encryption]
level: advanced
status: docs-checked
description: "Configure SAML 2.0 single sign-on between Okta and Mattermost: Okta app settings, encryption, metadata URL, attribute mapping and the user switch."
sources: ["https://docs.mattermost.com/administration-guide/onboard/sso-saml-okta.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SAML with Okta

Create the Okta app: log in as admin, use the Classic UI, Applications > Add Application > Create New App, Sign on method SAML 2.0. Give it a name and optional logo (showing the icon to users is recommended). SAML settings: Single sign on URL https://<your-mattermost-url>/login/sso/saml (normally matching the Mattermost Site URL), Audience URI such as mattermost, Name ID format unspecified, Application username Email. For encryption open Show Advanced Settings, set Assertion Encryption to Encrypted and upload the Service Provider Public Certificate in Encryption Certificate. Add attribute statements mapping Okta attributes to Mattermost ones. In the support step choose "I am an Okta customer adding an internal app" and "This is an internal app that we have created", then Finish.

In Mattermost, first set Override SAML bind data with AD/LDAP information to false if it is true. From the Okta Sign On tab, View Setup Instructions: copy the Identity Provider metadata link, note the Identity Provider Single Sign-On URL and Issuer, and download the X.509 certificate.

Then System Console > Authentication > SAML 2.0: paste the Identity Provider Metadata URL, which fills in the SAML SSO URL, Issuer URL and downloads the public certificate; or enter those three by hand. Set the Service Provider Login URL to the Okta single sign-on URL, turn on signature verification, encryption and request signing with the Service Provider Private Key, and set the assertion attributes. Email, Username and Id attributes are required and must match what you entered in Okta. Optionally set button text. If you map First Name and Last Name, set Teammate Name Display to Show first and last name under Site Configuration > Users and Teams. Save.

Confirm by switching your own admin account via Profile > Security > Sign-in Method > Switch to SAML SSO, and announce the migration to users. SAML can also be set in config.json, which needs a server restart.

## Checked

Confirmed against the Configure SAML with Okta page: Okta app settings, encryption, support parameters, the bind-data override step, metadata URL and manual fields, required Email, Username and Id attributes, name display recommendation, the sign-in switch and config.json restart note. The shared include files at the end of the page were not part of the source file read.

Method: docs-checked 2026-11-09 against the administration-guide/onboard/sso-saml-okta page (source rst from the mattermost/docs repo).
