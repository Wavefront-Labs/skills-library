---
id: computing-software.messaging-and-integration.apache-zookeeper.admin-server-hardening
name: admin-server-hardening
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, adminserver, hardening, forcehttps, needclientauth, tls-protocols]
level: advanced
status: docs-checked
description: "Harden the ZooKeeper AdminServer: default insecure posture, binding to a management address, forceHttps, needClientAuth, TLS protocol and cipher restriction."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AdminServer hardening

Default posture (Administrator's Guide, Security Considerations): enabled, listening on 0.0.0.0 port 8080, plain HTTP, client authentication disabled. Many commands (stat, srvr, conf, cons) need no authentication. The guide says this default suits trusted environments and is not secure for untrusted networks.

Defaults listed by the guide: `admin.enableServer=true`, `admin.serverAddress=0.0.0.0`, `admin.serverPort=8080`, `admin.forceHttps=false`, `admin.needClientAuth=false`.

Recommended practices from the guide:
- Minimum: bind `admin.serverAddress` to localhost or a management-network address, and restrict the port with firewall rules (iptables, firewalld, cloud security groups).
- Set `admin.forceHttps=true` to allow only HTTPS (it overwrites `admin.portUnification`).
- Set `admin.needClientAuth=true` so only clients presenting trusted X.509 certificates connect (x509 auth requires true).
- Production configuration the guide recommends: `admin.forceHttps=true`, `admin.needClientAuth=true`, `admin.serverAddress=<management-network-ip>`, plus firewall rules.
- If unused, disable it with `admin.enableServer=false` (or the `zookeeper.admin.enableServer` system property, or remove Jetty from the classpath). The TCP four-letter-word interface stays available.

TLS protocols and ciphers: new in 3.9.6 the AdminServer reuses `ssl.quorum.enabledProtocols` and `ssl.quorum.ciphersuites` (both default to the Jetty default for the AdminServer). The guide's example sets `ssl.quorum.enabledProtocols=TLSv1.2,TLSv1.3`.

Check: raise the `JettyAdminServer` log level to DEBUG and look for the "Setting enabled protocols" and "Setting enabled cipherSuites" entries.

## Checked

Confirmed against the Administrator's Guide (AdminServer, Security Considerations, SSL/TLS and AdminServer configuration sections). Removed the unsourced "Verify" test and the statement that the unlisted admin.* properties were checked beyond those quoted.

Method: docs-only read of cited pages, 2026-11-08
