---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-fortitoken-two-factor
name: fortigate-fortitoken-two-factor
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [fortitoken, fortios, two-factor, mfa, otp, email-token, sms-token]
level: practitioner
status: draft
description: "Add two-factor authentication to FortiGate local users or VPN logins using FortiToken mobile, hardware tokens or email."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: second factor for admin or VPN access.

```
config user local
    edit "alice"
        set type password
        set passwd <PASSWORD>
        set two-factor fortitoken
        set fortitoken "FTKMOB0123456789"
        set email-to "alice@example.com"
    next
end
```
Two-factor options: `fortitoken` (hardware or mobile), `email`, `sms`, or `fortitoken-cloud`. For FortiToken Mobile, activation needs the token to be assigned to a user and the activation code sent by email; the user then enrols in the app within the activation window.

Check licensing: FortiGate includes a small number of free mobile tokens; additional tokens are licensed (confirm).

Gotchas
- Time drift above about 30 seconds breaks TOTP codes; keep NTP right on the FortiGate.
- The FortiGate must reach the activation service for mobile tokens (internet from the unit).
- SSL VPN or admin login prompts for the code in a second field/step; clients need the right "token" prompt support.
- Back up admin access with an emergency method.

## Verify
```
diagnose test authserver local alice <PASSWORD>
get user fortitoken
```
Log in to the VPN as the user and confirm the token challenge appears and a wrong code is rejected.
