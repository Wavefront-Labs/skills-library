---
id: computing-software.systems-network-administration.cisco-networking.central-web-authentication-guests
name: central-web-authentication-guests
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, aaa, webauth, central-web-authentication, cwa, guest-access, ise, redirect-acl, coa]
level: practitioner
status: draft
description: "Give guests portal-based access with ISE Central Web Authentication on Catalyst or 9800 WLC: MAB trigger, redirect ACL, URL redirect and CoA reauthorisation."
sources:
  - https://www.cisco.com/c/en/us/support/docs/security/identity-services-engine/113362-config-web-auth-ios-00.html
  - https://www.cisco.com/c/en/us/support/docs/wireless/catalyst-9800-series-wireless-controllers/213920-central-web-authentication-cwa-on-cata.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Central Web Authentication (guests)

CWA flow: device connects -> MAB to ISE (unknown MAC) -> ISE returns a redirect ACL + URL ->
user's first HTTP request is redirected to the ISE guest portal -> user logs in/accepts AUP ->
ISE sends RADIUS **CoA** -> switch/WLC reauthenticates the session -> ISE now returns guest access.

## Switch side (wired)
```
ip http server                               ! needed for redirect interception
ip http secure-server
ip access-list extended REDIRECT-ACL
 deny udp any any eq domain                  ! deny = do NOT redirect
 deny udp any any eq bootps
 deny ip any host 10.99.0.11                 ! ISE PSN
 permit tcp any any eq www
 permit tcp any any eq 443
aaa server radius dynamic-author
 client 10.99.0.11 server-key <RADIUS_KEY>
interface Gi1/0/30
 authentication order mab
 mab
 ...                                          ! as for MAB
```
The redirect ACL is a match list: `permit` means intercept and redirect, `deny` passes.
ISE authorization profile: `Web Redirection (CWA)`, ACL name `REDIRECT-ACL`.

## WLC 9800 (wireless)
WLAN with MAC filtering + `aaa-override` + `nac` (RADIUS NAC) on the policy profile; the
redirect ACL is defined on the WLC with the same name ISE sends.

## Gotchas
- HTTPS sites cannot be redirected cleanly (certificate warning); OS captive portal detection
  (HTTP probes) usually triggers the portal anyway.
- CoA port UDP 1700 (Cisco) or 3799 must be allowed from ISE to the NAD.
- DNS must work before login or the client never sends HTTP.

## Verify
```
show access-session interface Gi1/0/30 details   ! URL Redirect ACL and URL before login
```
After login the session shows the guest authorization profile and no redirect.
- [ ] Guest sees portal, after login gets internet-only access; CoA visible in ISE logs.
