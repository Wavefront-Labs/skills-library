---
id: computing-software.messaging-and-integration.apache-pulsar.basic-authentication
name: basic-authentication
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [basic-authentication, htpasswd, basic-auth-conf, authentication-provider-basic, password-file]
level: practitioner
status: docs-checked
description: "Enable Pulsar basic username/password authentication: create an htpasswd file (MD5 or CRYPT), set basicAuthConf on brokers and proxies, and configure CLI and clients."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/security-basic-auth.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: authenticate clients with user and password pairs stored in an Apache htpasswd file.

Prerequisite: the `htpasswd` tool (`apt install apache2-utils` on Debian/Ubuntu, `yum install httpd-tools` on CentOS/RHEL).

Create the password file. MD5 is recommended; CRYPT is also supported:
```bash
htpasswd -cmb /path/to/.htpasswd superuser admin   # MD5
htpasswd -cdb /path/to/.htpasswd superuser admin   # CRYPT
```
The entry looks like `superuser:$apr1$...`. Use placeholder credentials only in examples; choose real passwords in practice.

Brokers and proxies (`broker.conf` and `proxy.conf`, or `standalone.conf`):
```conf
authenticationEnabled=true
authenticationProviders=org.apache.pulsar.broker.authentication.AuthenticationProviderBasic
basicAuthConf=file:///path/to/.htpasswd
brokerClientAuthenticationPlugin=org.apache.pulsar.client.impl.auth.AuthenticationBasic
brokerClientAuthenticationParameters={"userId":"superuser","password":"admin"}
```
`basicAuthConf` also accepts a plain path, `data:;base64,<base64 of the file>` or the bare base64 string. Alternative: set the environment variable `PULSAR_EXTRA_OPTS` to `-Dpulsar.auth.basic.conf=/path/to/.htpasswd`.

CLI tools (`client.conf`):
```conf
authPlugin=org.apache.pulsar.client.impl.auth.AuthenticationBasic
authParams={"userId":"superuser","password":"admin"}
```

Java client:
```java
AuthenticationBasic auth = new AuthenticationBasic();
auth.configure("{\"userId\":\"superuser\",\"password\":\"admin\"}");
PulsarClient client = PulsarClient.builder().serviceUrl("pulsar://broker.example.com:6650").authentication(auth).build();
```
Python: `Client(url, authentication=AuthenticationBasic("user", "password"))`; Go: `pulsar.NewAuthenticationBasic(user, password)`; C++: `pulsar::AuthBasic::create(user, password)`.

Basic authentication uses base64-encoded username and password pairs. It only identifies the client; authorization is enabled separately.

## Checked

2026-11-03. Confirmed against the pulsar-site page security-basic-auth: htpasswd prerequisites and commands, MD5 (recommended) and CRYPT, broker, proxy and client settings, `basicAuthConf` forms, `PULSAR_EXTRA_OPTS`, and the Java, Python, C++ and Go client calls. Removed the unsourced TLS advice and the invented Verify step.

Method: documentation only; no commands were run.
