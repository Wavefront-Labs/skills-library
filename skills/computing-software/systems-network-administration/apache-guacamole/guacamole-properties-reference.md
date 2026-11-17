---
id: computing-software.systems-network-administration.apache-guacamole.guacamole-properties-reference
name: guacamole-properties-reference
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, guacamole-properties, guacd-hostname, guacd-port, case-sensitivity, extension-priority, skip-if-unavailable, log-level, logback, environment-properties, api-session-timeout]
level: practitioner
status: docs-checked
description: "Core guacamole.properties settings with defaults: guacd-*, api-session-timeout, case-sensitivity, extension-priority, log-level, env-var overrides, logback.xml."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# guacamole.properties reference

| Property | Default | Notes |
|---|---|---|
| `guacd-hostname` / `guacd-port` | localhost / 4822 | where guacd listens |
| `guacd-ssl` | off | `true` requires TLS to guacd |
| `api-session-timeout` | 60 | minutes of inactivity |
| `api-max-request-size` | 2097152 | bytes, 0 = unlimited; not for uploads |
| `allowed-languages` | all | e.g. `en, de` |
| `case-sensitivity` | `enabled` | also `usernames`, `group-names`, `disabled`; affects Guacamole comparisons only, not LDAP |
| `extension-priority` | filename order | namespaces, `*` = all unlisted |
| `skip-if-unavailable` | none | provider IDs allowed to fail, e.g. `mysql, ldap` |
| `log-level` | `info` | error, warn, info, debug, trace |
| `enable-environment-properties` | - | `true` lets env vars override |

Env overrides: uppercase, dashes to underscores (`guacd-hostname` becomes `GUACD_HOSTNAME`); always on in the Docker image.

`extension-priority: saml` loads SAML first; `*, saml` loads it last. Startup logs show the namespaces and load order.

Logging: for more than a level, put `logback.xml` in GUACAMOLE_HOME:
```xml
<configuration>
  <appender name="GUAC-DEBUG" class="ch.qos.logback.core.ConsoleAppender">
    <encoder><pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern></encoder>
  </appender>
  <root level="debug"><appender-ref ref="GUAC-DEBUG"/></root>
</configuration>
```
Verify: after a restart, the startup log lists extension namespaces in the expected load order.

## Checked

2026-11-04. Confirmed against the Guacamole manual page configuring-guacamole: every default and note in the table (guacd-hostname, guacd-port, guacd-ssl, api-session-timeout 60, api-max-request-size 2097152 not applying to uploads, allowed-languages, the four case-sensitivity values and the LDAP caveat, extension-priority with *, skip-if-unavailable, log-level values, enable-environment-properties), the uppercase and underscore environment naming, Docker use, and the Logback console example. Changed: removed the claim that extension-priority controls automatic SSO redirect or login form display, which the page does not state, and the Tomcat-log level check.

Method: documentation only; no commands were run.
