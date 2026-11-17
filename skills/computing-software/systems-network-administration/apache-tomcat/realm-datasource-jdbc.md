---
id: computing-software.systems-network-administration.apache-tomcat.realm-datasource-jdbc
name: realm-datasource-jdbc
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, realm, datasourcerealm, jdbc-realm, database-authentication, usertable, userrolestable, localdatasource]
level: practitioner
status: docs-checked
description: "Authenticate Tomcat 10.1 users from a database with DataSourceRealm: dataSourceName, localDataSource, user/role table and column attributes."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/realm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DataSourceRealm

Looks up users and roles through a JNDI JDBC DataSource each time it is required, so database changes apply to new logins immediately. It supports simultaneous authentications and leaves connection pooling to the DataSource.

| Attribute | Notes |
|---|---|
| `dataSourceName` | JNDI name of the DataSource |
| `localDataSource` | false (global DataSource); when nested in a Context, true uses a DataSource defined for that Context |
| `userTable` | Table of users |
| `userNameCol` | Username column (user and role tables) |
| `userCredCol` | Password column; treated as digested if a CredentialHandler is set, otherwise clear text |
| `userRoleTable` | User-to-role table |
| `roleNameCol` | Role name column in the user-roles table; required in most configurations (optional with `allRolesMode` `authOnly` or `strictAuthOnly`) |

```xml
<Realm className="org.apache.catalina.realm.DataSourceRealm"
       dataSourceName="jdbc/authDB"
       userTable="users" userNameCol="user_name" userCredCol="user_pass"
       userRoleTable="user_roles" roleNameCol="role_name"/>
```

Steps:
1. Define the DataSource (`computing-software.systems-network-administration.apache-tomcat.jdbc-datasource-resource`) in `GlobalNamingResources` or the Context.
2. Create the user and role tables: `userTable` needs the `userNameCol` and `userCredCol` columns, `userRoleTable` the `userNameCol` and `roleNameCol` columns. With a CredentialHandler, passwords are assumed encoded with its algorithm; otherwise clear text.
3. Add the Realm in Engine, Host or Context.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Realm reference (DataSource Database Realm). Added the table column requirements and allRolesMode note; removed the generic verify line.

Method: documentation only; no commands were run.
