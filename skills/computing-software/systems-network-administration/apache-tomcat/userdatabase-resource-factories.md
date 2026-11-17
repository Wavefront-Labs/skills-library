---
id: computing-software.systems-network-administration.apache-tomcat.userdatabase-resource-factories
name: userdatabase-resource-factories
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, userdatabase, memoryuserdatabasefactory, datasourceuserdatabasefactory, tomcat-users-xml, jndi, readonly, watchsource]
level: advanced
status: docs-checked
description: "Configure the Tomcat 10.1 UserDatabase JNDI resource: MemoryUserDatabaseFactory over tomcat-users.xml (readonly, watchSource) or DataSourceUserDatabaseFactory."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/jndi-resources-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# UserDatabase resources

Memory-backed, in `GlobalNamingResources`:
```xml
<Resource name="UserDatabase" auth="Container" type="org.apache.catalina.UserDatabase"
          factory="org.apache.catalina.users.MemoryUserDatabaseFactory"
          pathname="conf/tomcat-users.xml" readonly="false"/>
```
- `readonly` is optional and defaults to true; if the XML is writable it is written to when Tomcat starts, and the file inherits the default file permissions of the Tomcat user.
- `watchSource`: if referenced in a Realm, the UserDatabase by default monitors `pathname` and reloads the file when its last modified time changes; `watchSource="false"` disables this.
- `conf/tomcat-users.xml` holds `<role rolename=.../>` and `<user username password roles/>` entries.

Database-backed:
```xml
<Resource name="UserDatabase" auth="Container" type="org.apache.catalina.UserDatabase"
          factory="org.apache.catalina.users.DataSourceUserDatabaseFactory"
          dataSourceName="jdbc/authority" readonly="false"
          userTable="users" userNameCol="user_name" userCredCol="user_pass"
          userRoleTable="user_roles" roleNameCol="role_name"/>
```
- The DataSource must be declared in the same JNDI context as the UserDatabase.
- Minimal schema: `users` and `user_roles`. Full schema adds `roles`, `groups`, `user_groups`, `group_roles` (attributes `roleTable`, `groupTable`, `userGroupTable`, `groupRoleTable`, `groupNameCol`).
- With a CredentialHandler, passwords are assumed encoded with its algorithm; otherwise clear text.
- `readonly` defaults to true; if the database is writable, changes made through Tomcat management can be persisted with the save operation.

Use it from `computing-software.systems-network-administration.apache-tomcat.realm-userdatabase-and-memory` with `resourceName="UserDatabase"`.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 JNDI Resources how-to (Memory and DataSource UserDatabase Resources). Reworded readonly and watchSource; removed the pathname bullet, which the page does not describe, and the generic verify line.

Method: documentation only; no commands were run.
