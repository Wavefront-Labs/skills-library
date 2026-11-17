---
id: computing-software.systems-network-administration.apache-guacamole.deploy-web-app-tomcat
name: deploy-web-app-tomcat
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, web-application, tomcat, guacamole-war, maven, native-installation, webapps]
level: practitioner
status: docs-checked
description: "Install the Guacamole web application on Tomcat: download or build guacamole.war with Maven, copy it into webapps, restart Tomcat and start guacd."
sources:
  - https://guacamole.apache.org/doc/gug/guacamole-native.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploy the web application on Tomcat

Get the WAR either way:
- Download `guacamole.war` from the project site, or
- Build: 
```
tar -xzf guacamole-client-1.6.0.tar.gz && cd guacamole-client-1.6.0/
mvn package
# output: guacamole/target/guacamole-1.6.0.war
```

Deploy (Tomcat derives the URL path from the file name, so rename):
```
cp guacamole/target/guacamole-1.6.0.war /var/lib/tomcat/webapps/guacamole.war
systemctl restart tomcat9
systemctl start guacd
```
`CATALINA_HOME` is commonly `/var/lib/tomcat` or `/var/lib/tomcat9` depending on distribution.

Result: Tomcat derives the app's URL path from the WAR name, so `guacamole.war` is served at `/guacamole/`; it is unconfigured. You still need an authentication source, either `user-mapping.xml` (see apache-guacamole.user-mapping-xml) or a database or other extension, all under GUACAMOLE_HOME (default `/etc/guacamole`; see apache-guacamole.guacamole-home-layout).

To start on boot, enable the Tomcat and guacd services (with systemd: `systemctl enable tomcat9`, and likewise guacd).

Verify: browsing to the URL shows the Guacamole login screen once an authentication source is configured.

## Checked

2026-11-04. Confirmed against the Guacamole manual page guacamole-native: downloading guacamole.war or building with mvn package, output in guacamole/target/, renaming to guacamole.war because Tomcat derives the path from the file name, CATALINA_HOME commonly /var/lib/tomcat or /var/lib/tomcat9, the systemd restart and start commands, the enable-on-boot note, and that the freshly installed app is unconfigured. Changed: removed the URIEncoding claim, which this page does not make, and the Tomcat-log verification.

Method: documentation only; no commands were run.
