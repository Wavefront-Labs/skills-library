---
id: computing-software.networking-hardware-and-wireless.asterisk.security-contexts-network-and-events
name: security-contexts-network-and-events
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, security, dialplan-security, acl, permit, deny, security-log, event-logger, contexts, hardening]
level: practitioner
status: docs-checked
description: "Harden Asterisk: isolate toll services in dialplan contexts, protect manager access, apply permit and deny ACLs, and log security events with the security level in logger.conf."
sources:
  - https://docs.asterisk.org/Deployment/Important-Security-Considerations/Dialplan-Security/
  - https://docs.asterisk.org/Deployment/Important-Security-Considerations/Network-Security/
  - https://docs.asterisk.org/Deployment/Asterisk-Security-Framework/Asterisk-Security-Event-Logger/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# security: contexts, network and events
Improper configuration can allow unauthorized use of your facilities and substantial charges. Security covers network security (encryption, authentication) and dialplan security (authorization).

**Dialplan.** Any channel that can enter a context can reach every extension in it. Keep outgoing or toll services out of contexts reachable from incoming channels (IAX, trunks, untrusted stations), and never put them in `default`. Layer contexts with `include`:
```
[longdistance]
exten => _91NXXNXXXXXX,1,Dial(DAHDI/g2/${EXTEN:1})
include => local
[local]
include => default
```
Remove the `demo` context from `default`.

**Network.** `make samples` opens a few ports; check channel configs for ports and addresses. Reach the manager interface only from a safe environment or through SSH/VPN. For TCP/IP services, use `permit` and `deny` options in `manager.conf` and the channel configs. IAX2 supports RSA key authentication and AES encryption; SIP supports TLS and SRTP.

**Security framework.** The security event logger module adds a custom `security` logging level when loaded. Enable it by adding a log file with that level to `logger.conf`; this example logs to a file named `security_log`:
```
security_log => security
```

## Checked
2026-11-09: read the Dialplan Security, Network Security and Asterisk Security Event Logger pages in full and confirmed the context advice, the include example, demo context note, make samples ports, manager protection, permit and deny, IAX2 and SIP encryption statements, and the security logging level. Removed the AST_EVENT_SECURITY type name (not on the cited pages).

Method: documentation only; no commands were run.
