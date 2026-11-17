---
id: computing-software.systems-network-administration.apache-tomcat.realm-jaas
name: realm-jaas
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, realm, jaasrealm, jaas, loginmodule, userclassnames, roleclassnames, appname]
level: advanced
status: docs-checked
description: "Delegate Tomcat 10.1 authentication to JAAS login modules with JAASRealm: appName, configFile, userClassNames, roleClassNames and useContextClassLoader."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/realm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# JAASRealm

Uses Java Authentication and Authorization Service `LoginModule`s.

| Attribute | Notes |
|---|---|
| `appName` | Application name in the JAAS login configuration; if not specified, derived from the name of the Container it is placed in (for example Catalina or ROOT) |
| `configFile` | JAAS config file searched with `ClassLoader#getResource(String)`, so it can be bundled in a web application; default is the JVM global JAAS configuration |
| `userClassNames` | Comma-separated user Principal classes |
| `roleClassNames` | Comma-separated role Principal classes |
| `useContextClassLoader` | true: context class loader loads the LoginModule and Principal classes; false: the container's class loader |

```xml
<Realm className="org.apache.catalina.realm.JAASRealm"
       appName="MyApp"
       userClassNames="com.example.UserPrincipal"
       roleClassNames="com.example.RolePrincipal"
       configFile="/path/to/jaas.config"/>
```

Steps:
1. Write the `LoginModule` and Principal classes.
2. Add a named entry in the JAAS config file matching `appName`.
3. Reference the Realm; roles come from the Principals listed in `roleClassNames`.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Realm reference (JAAS Realm). Reworded the appName, configFile and useContextClassLoader rows; removed the jar placement claim and the generic verify line.

Method: documentation only; no commands were run.
