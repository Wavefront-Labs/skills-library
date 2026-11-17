---
id: computing-software.systems-network-administration.nagios-core.event-handler-restart-example
name: event-handler-restart-example
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, event-handler-example, restart-httpd, soft-state-handler, max-check-attempts, restart-service]
level: practitioner
status: docs-checked
description: "Worked Nagios Core event handler that restarts httpd on SOFT attempt 3 and as HARD fallback, wired to a service with max_check_attempts 4."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/eventhandlers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restart-on-failure handler

Setup from the docs: service `HTTP` on a host with `max_check_attempts` of 4 or greater (the page uses 4) and `event_handler restart-httpd`.

Command passes state arguments:
```
define command {
    command_name  restart-httpd
    command_line  /usr/local/nagios/libexec/eventhandlers/restart-httpd $SERVICESTATE$ $SERVICESTATETYPE$ $SERVICEATTEMPT$
}
```

Script logic (shell, sketch)
```
case "$1" in
OK|WARNING|UNKNOWN) ;;
CRITICAL)
  case "$2" in
  SOFT) [ "$3" = "3" ] && /etc/rc.d/init.d/httpd restart ;;
  HARD) /etc/rc.d/init.d/httpd restart ;;
  esac ;;
esac
exit 0
```

## Why it works
- Restarting on SOFT attempt 3 acts before the HARD alert and notification.
- The HARD branch is a fallback and runs only the first time the service enters HARD, so a still-down service is not restarted repeatedly.
- Ignore OK/WARNING/UNKNOWN; always exit 0.

General rules: `computing-software.systems-network-administration.nagios-core.event-handlers`.

## Checked

2026-11-04. Confirmed against the Event Handlers page: the HTTP service example, restart-httpd command line with $SERVICESTATE$ $SERVICESTATETYPE$ $SERVICEATTEMPT$, the case logic restarting on SOFT attempt 3 and on HARD, and that the handler runs only the first time the service enters a HARD problem state. Removed an unconfirmed sudo requirement and used the init script path from the page.

Method: documentation only; no commands were run.
