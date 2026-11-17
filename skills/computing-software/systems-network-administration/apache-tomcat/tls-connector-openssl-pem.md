---
id: computing-software.systems-network-administration.apache-tomcat.tls-connector-openssl-pem
name: tls-connector-openssl-pem
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, tls, openssl, pem, tomcat-native, aprlifecyclelistener, sslimplementationname, certificatefile, certificatekeyfile]
level: advanced
status: docs-checked
description: "Use PEM certificates with the OpenSSL implementation in Tomcat 10.1: sslImplementationName, Certificate PEM attributes, AprLifecycleListener SSLEngine and SSLRandomSeed."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/ssl-howto.html
  - https://tomcat.apache.org/tomcat-10.1-doc/config/http.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# OpenSSL (Tomcat Native) with PEM files

```xml
<Connector protocol="org.apache.coyote.http11.Http11NioProtocol"
           port="8443" SSLEnabled="true"
           sslImplementationName="org.apache.tomcat.util.net.openssl.OpenSSLImplementation">
  <SSLHostConfig>
    <Certificate certificateKeyFile="conf/localhost-rsa-key.pem"
                 certificateFile="conf/localhost-rsa-cert.pem"
                 certificateChainFile="conf/localhost-rsa-chain.pem"
                 type="RSA"/>
  </SSLHostConfig>
</Connector>
```

- `certificateChainFile` must not contain the server certificate itself.
- `certificateKeyFile` defaults to `certificateFile` (not recommended); `certificateKeyPasswordFile` beats `certificateKeyPassword`.
- With the generic `protocol="HTTP/1.1"`, Tomcat chooses automatically: JSSE with OpenSSL if the Tomcat Native (APR) library is installed, otherwise Java JSSE. Naming a class in `protocol` avoids auto-selection; `org.apache.tomcat.util.net.jsse.JSSEImplementation` selects the Java implementation explicitly.
- With the OpenSSL implementation use either the JSSE attributes or the OpenSSL attributes, never a mix in the same `SSLHostConfig` or Connector.

Native engine switch in `server.xml`:
```xml
<Listener className="org.apache.catalina.core.AprLifecycleListener"
          SSLEngine="on" SSLRandomSeed="builtin"/>
```
The default is `SSLEngine="on" SSLRandomSeed="builtin"`; to enable OpenSSL, set `SSLEngine` to anything other than `off` (another value must be a valid OpenSSL engine name). `SSLRandomSeed` is the entropy source: production systems need a reliable one, while test systems can use a non-blocking source such as `/dev/urandom` for quicker starts.

OCSP needs an NIO or NIO2 connector with the OpenSSL-style configuration and either `OpenSSLImplementation` on a Tomcat Native build with OCSP enabled, or `org.apache.tomcat.util.net.openssl.panama.OpenSSLImplementation` (needs Java 25 or later). It is not supported with `JSSEImplementation` or the JSSE configuration style.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 SSL/TLS how-to and HTTP Connector reference (certificateKeyFile, certificateChainFile, certificateKeyPasswordFile). Rewrote the implementation-selection, entropy and OCSP notes; removed the generic verify line.

Method: documentation only; no commands were run.
