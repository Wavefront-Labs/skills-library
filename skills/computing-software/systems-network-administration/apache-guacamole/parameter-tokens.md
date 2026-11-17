---
id: computing-software.systems-network-administration.apache-guacamole.parameter-tokens
name: parameter-tokens
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, parameter-tokens, guac-username, guac-password, history-uuid, token-modifiers, ldap-tokens, oidc-tokens, cas-tokens, jdbc-tokens, single-sign-on-credentials]
level: practitioner
status: docs-checked
description: "Use Guacamole parameter tokens like ${GUAC_USERNAME} in connection settings, with LOWER/UPPER modifiers, escaping, extension-specific tokens and prompting rules."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parameter tokens

Any parameter value can contain tokens substituted at connect time.

Built-in:
- `${GUAC_USERNAME}`, `${GUAC_PASSWORD}`: the Guacamole login (enables SSO into RDP/SSH)
- `${GUAC_CLIENT_ADDRESS}`, `${GUAC_CLIENT_HOSTNAME}`
- `${GUAC_DATE}` (YYYYMMDD), `${GUAC_TIME}` (HHMMSS)

Syntax:
- Modifier: `${GUAC_USERNAME:UPPER}` or `:LOWER`.
- Escape a literal with a leading `$`: `$${TOKEN}`.

Extension tokens:
- CAS: attributes as `${CAS_EMAIL}` (the CAS server must release them).
- JDBC: `JDBC_CONNECTION_ID`, `JDBC_CONNECTION_NAME`, `JDBC_HOSTNAME`, `JDBC_PROTOCOL`, `JDBC_STARTDATE`, `JDBC_STARTTIME`.
- LDAP: attributes as `${LDAP_...}`, chosen with `ldap-user-attributes`.
- OIDC: claims as `${OIDC_...}`, chosen with `openid-attributes-claim-type`; multi-valued claims are not unrolled.
- Recording history tokens `${HISTORY_PATH}`, `${HISTORY_UUID}` (apache-guacamole.recording-playback).

Examples: `username: ${GUAC_USERNAME}`, `password: ${GUAC_PASSWORD}`, `recording-name: ${GUAC_DATE}-${GUAC_TIME}`, `drive-path: /path/to/${GUAC_USERNAME}`.

Prompting: for RDP and VNC, Guacamole prompts for credentials only when none are configured. A preconfigured wrong value fails rather than prompts.

Verify: connect and confirm the remote login uses the Guacamole user; an unresolved token indicates the source extension is not providing it.

## Checked

2026-11-04. Confirmed against the Guacamole manual pages configuring-guacamole (Parameter tokens, token modifiers, extension tokens, parameter prompting) and recording-playback (HISTORY_UUID, HISTORY_PATH): built-in GUAC_ tokens and date/time formats, UPPER and LOWER, the leading-dollar escape, CAS_, JDBC_, LDAP_ and OIDC_ prefixes, multi-valued claims not unrolled, and prompting only for RDP and VNC when credentials are not configured. Nothing removed; the Examples line is illustrative usage.

Method: documentation only; no commands were run.
