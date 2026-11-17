---
id: computing-software.systems-network-administration.apache-tomcat.single-sign-on-valve
name: single-sign-on-valve
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, valve, singlesignon, sso, realm, host, jsessionidsso, requirereauthentication]
level: practitioner
status: docs-checked
description: "Enable SingleSignOn across web apps on one Tomcat 10.1 Host: valve placement, shared Realm requirement, cookie behaviour, requireReauthentication and cookieName."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/host.html
  - https://tomcat.apache.org/tomcat-10.1-doc/config/valve.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SingleSignOn valve

```xml
<Host name="localhost" appBase="webapps">
  <Valve className="org.apache.catalina.authenticator.SingleSignOn"/>
</Host>
```

Requirements and behaviour:
- All apps on the host must share one Realm: nest the `<Realm>` in the Host or Engine, not in a Context.
- Unprotected resources trigger no authentication.
- Reaching a protected resource in any app challenges using that app's login method; roles then apply across all apps on the host.
- Logging out of one app (for example invalidating a FORM session) invalidates sessions in all apps.
- Uses a cookie, so clients must accept cookies.

Attributes (valve page):
- `cookieName`: JSESSIONIDSSO.
- `cookieDomain`: the host domain to be used for SSO cookies.
- `requireReauthentication` (false): when true, the valve uses cached username and password to reauthenticate to the Realm on each request of an SSO session where the app uses BASIC or FORM; DIGEST, SPNEGO and CLIENT-CERT use their normal authentication. Only makes sense with two or more BASIC/FORM apps. When false, the valve authenticates from a valid SSO cookie without rechecking the Realm.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Host reference (Single Sign On rules) and Valve reference (Single Sign On Valve attributes). Removed the share-across-subdomains and unset-by-default claims and the generic verify line.

Method: documentation only; no commands were run.
