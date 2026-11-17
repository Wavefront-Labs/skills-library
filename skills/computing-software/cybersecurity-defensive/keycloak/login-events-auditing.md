---
id: computing-software.cybersecurity-defensive.keycloak.login-events-auditing
name: login-events-auditing
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, events, login-events, audit, event-types]
level: practitioner
status: docs-checked
description: "Turn on and read Keycloak user events, event types, and the logging and email event listeners including their kc options."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/events/login.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# login events auditing
Keycloak triggers events for successful logins, wrong passwords, account updates and more. By default it does not store or display events in the Admin Console; only error events are logged to the Admin Console and the server log file.

Procedure: *Realm settings* > *Events* tab > *User events settings* tab > toggle *Save events* ON, set the *Expiration* field, use *Add saved types* to choose more event types, then *Add*. *Clear user events* deletes all saved events. View them under *Events* in the menu; *Search user event* filters.

Event types in the docs:
- Login: Login, Register, Logout, Code to Token, Refresh Token.
- Brute force protection: User disabled by permanent lockout, User disabled by temporary lockout.
- Identity brokering: Federated identity link override (and its error).
- OAuth: OAuth2 extension grant (and its error).
- Account: Social Link, Remove Social Link, Update Email, Update Profile, Send Password Reset, Update Credential, Remove Credential, Send Verify Email, Verify Email; Update Password, Update TOTP and Remove TOTP are deprecated.
Each event has a corresponding error event.

## Event listeners
Two built in: Logging and Email.

Logging Event Listener: writes a log line when an error event occurs, for example `type=LOGIN_ERROR, realmId=..., clientId=..., userId=..., ipAddress=..., error=invalid_user_credentials`. To fight bots, parse the log for `LOGIN_ERROR`, extract the IP address and feed it to intrusion prevention software. It logs to the `org.keycloak.events` category; debug events are not in server logs by default. To change the levels it uses (debug, info, warn, error, fatal):
```
bin/kc.sh start --spi-events-listener--jboss-logging--success-level=info --spi-events-listener--jboss-logging--error-level=error
```

Email Event Listener: emails the user on Login Error, Update Password, Update TOTP, Remove OTP, Update Credential and Remove Credential; optional events are the permanent and temporary lockout events. It needs a user with an email address that is marked verified, and the realm's email settings configured. Enable it under *Realm settings* > *Events* > *Event listeners* field > select `email`. Options:
```
kc.sh --spi-events-listener--email--exclude-events=UPDATE_CREDENTIAL,REMOVE_CREDENTIAL
kc.sh --spi-events-listener--email--include-events=USER_DISABLED_BY_TEMPORARY_LOCKOUT_ERROR,USER_DISABLED_BY_PERMANENT_LOCKOUT
```

## Checked
2026-11-03. Confirmed against server_admin/topics/events/login.adoc: procedure, event table, both listeners and their option names. Removed: the "events table grows" gotcha, "detection ideas" beyond the page's IPS recipe, and the invented Verify step; corrected the claim that events are stored unless disabled (only error events are logged by default).
Method: documentation only; no commands were run.
