---
id: computing-software.systems-network-administration.apache-guacamole.quickconnect
name: quickconnect
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, quickconnect, ad-hoc-connections, connection-bar, quickconnect-allowed-parameters, quickconnect-denied-parameters, uri-syntax]
level: practitioner
status: docs-checked
description: "Create ad-hoc Guacamole connections from a URI with the quickconnect extension: URI syntax, allowed and denied parameter lists, and security cautions."
sources:
  - https://guacamole.apache.org/doc/gug/adhoc-connections.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quickconnect (ad-hoc connections)

Adds a connection bar to the home page. The connection exists only for the session and is not shared.

Install: `guacamole-auth-quickconnect-1.6.0.jar` into `GUACAMOLE_HOME/extensions/`; restart Tomcat. Docker: `QUICKCONNECT_ENABLED=true`.

URI syntax: `protocol://username:password@host:port/?parameters`
- `ssh://linux1.example.com/` prompts for credentials
- `vnc://linux1.example.com:5900/` (VNC needs an explicit port)
- `rdp://localuser@windows1.example.com/?security=rdp&ignore-cert=true&disable-audio=true`
Any protocol parameter can be given in the query.

Controls (optional):
- `quickconnect-allowed-parameters` (`QUICKCONNECT_ALLOWED_PARAMETERS`): only these may be used.
- `quickconnect-denied-parameters` (`QUICKCONNECT_DENIED_PARAMETERS`): stripped even if also allowed.
The manual does not specify the list separator; check the release notes before setting them.

Security: users must already be authenticated by another module. Because users can set any parameter, the manual's own RDP example sets `enable-drive=true` and `drive-path` to a folder on the guacd host (apache-guacamole.rdp-drive-redirection), so use `quickconnect-denied-parameters` to remove such parameters for users you do not trust.

Verify: type a URI and press Enter; the session starts without a stored connection.

## Checked

2026-11-04. Confirmed against the Guacamole manual page adhoc-connections: in-memory, per-session, unshared connections, no authentication of its own, install jar and QUICKCONNECT_ENABLED, the URI form and the three example URIs, VNC having no default port, and the allowed/denied parameter properties (denied wins over allowed). Changed: the security advice now cites the manual's drive-path example instead of claiming access to any directory guacd can read, and the guesswork about restricting guacd file access was removed. Kept the note that the page does not specify the list separator.

Method: documentation only; no commands were run.
