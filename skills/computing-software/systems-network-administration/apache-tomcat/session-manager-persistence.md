---
id: computing-software.systems-network-administration.apache-tomcat.session-manager-persistence
name: session-manager-persistence
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, session-manager, standardmanager, persistentmanager, sessions-ser, filestore, datasourcestore, maxactivesessions, session-persistence, sessionidgenerator]
level: advanced
status: docs-checked
description: "Configure the Tomcat 10.1 session Manager: StandardManager pathname persistence, maxActiveSessions, attribute filters, PersistentManager with FileStore or DataSourceStore."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/manager.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Session Manager

A `<Manager>` inside `<Context>` is optional; the default is StandardManager.

Common: `maxActiveSessions` (-1; at the limit `IllegalStateException` on create), `sessionLastAccessAtStart` (false), `sessionActivityCheck` (false), `notifyAttributeListenerOnUnchangedValue` (true).

StandardManager:
- `pathname` (null): file for saving sessions across restarts; set non-empty to enable.
```xml
<Context><Manager pathname="SESSIONS.ser"/></Context>
```
- `persistAuthentication` (false; Principal must be Serializable), `processExpiresFrequency` (6), `secureRandomClass` (`java.security.SecureRandom`), `secureRandomAlgorithm` (SHA1PRNG).
- `sessionAttributeNameFilter` / `sessionAttributeValueClassNameFilter`: anchored regexes limiting persisted attributes; `warnOnSessionAttributeFilterFailure` false (true under a SecurityManager).
- Attributes must be `Serializable`; `<distributable/>` in web.xml makes Tomcat enforce it. Expired sessions are not restored.
- Session ID length: nested `<SessionIdGenerator sessionIdLength="..."/>`.

PersistentManager (set `className="org.apache.catalina.session.PersistentManager"`, nest a `<Store>`, and set system property `org.apache.catalina.session.StandardSession.ACTIVITY_CHECK` or `org.apache.catalina.STRICT_SERVLET_COMPLIANCE` to true):
- `maxIdleBackup` (-1), `maxIdleSwap` (-1, >= backup), `minIdleSwap` (-1, < maxIdleSwap), `saveOnRestart` (true).
- `FileStore`: `directory` (default the context's temporary work dir); one file per session, so scalability problems as sessions grow; mainly for experiments.
- `DataSourceStore`: `dataSourceName`, `localDataSource` (false), `sessionTable` (`tomcat$sessions`), `sessionIdCol` (`id`), `sessionDataCol` (`data`), `sessionValidCol` (`valid`), `sessionMaxInactiveCol` (`maxinactive`), `sessionAppCol` (`app`). Match column names to your table.

Verify: after a normal shutdown, `SESSIONS.ser` exists (relative paths resolve against the Context work directory).

## Checked

2026-11-04. Read the Tomcat 10.1 Manager page (config/manager.html): confirmed the common attributes and defaults, every StandardManager attribute and default, the PersistentManager attributes, system property note and Store requirement, FileStore and DataSourceStore attributes and default column names, SessionIdGenerator sessionIdLength, serialization and distributable notes, and the SESSIONS.ser example. Reworded the FileStore scale remark and the verify step to what the page states.

Method: documentation only; no commands were run.
