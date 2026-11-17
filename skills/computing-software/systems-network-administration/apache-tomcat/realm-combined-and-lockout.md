---
id: computing-software.systems-network-administration.apache-tomcat.realm-combined-and-lockout
name: realm-combined-and-lockout
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, realm, combinedrealm, lockoutrealm, brute-force, failurecount, lockouttime, account-lockout]
level: practitioner
status: docs-checked
description: "Chain several Tomcat 10.1 Realms with CombinedRealm and add brute-force protection with LockOutRealm: failureCount, lockOutTime, cacheSize and caseSensitive."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/realm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CombinedRealm and LockOutRealm

CombinedRealm nests several `<Realm>` elements, tried in order; the first realm that authenticates supplies user and roles.
```xml
<Realm className="org.apache.catalina.realm.CombinedRealm">
  <Realm className="org.apache.catalina.realm.DataSourceRealm" .../>
  <Realm className="org.apache.catalina.realm.JNDIRealm" .../>
</Realm>
```

LockOutRealm extends CombinedRealm and locks a user after repeated failures:

| Attribute | Default |
|---|---|
| `failureCount` | 5 consecutive failures |
| `lockOutTime` | 300 s; further failures during lockout reset the timer, valid attempts during lockout fail without resetting it |
| `cacheSize` | 1000 failed-user entries |
| `cacheRemovalWarningTime` | 3600 s; a warning is logged if a failed user is removed from the cache before it has been there this long |
| `caseSensitive` | false |

```xml
<Realm className="org.apache.catalina.realm.LockOutRealm"
       failureCount="5" lockOutTime="300">
  <Realm className="org.apache.catalina.realm.UserDatabaseRealm"
         resourceName="UserDatabase"/>
</Realm>
```

Notes:
- LockOutRealm needs no change to the underlying realms: it records all failed logins, including for users that do not exist, and the list of failed users is limited (`cacheSize`) to prevent a DOS with invalid users. The cache grows to that size over time and may not shrink.
- `caseSensitive` controls how user names are treated for locking decisions (false: case insensitive).

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Realm reference (Combined Realm, LockOut Realm). Reworded the lockout-timer and cache rows; replaced the per-username and memory notes with the page's statements; removed the generic verify line.

Method: documentation only; no commands were run.
