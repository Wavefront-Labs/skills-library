---
id: computing-software.messaging-and-integration.apache-pulsar.pulsar-proxy-configuration
name: pulsar-proxy-configuration
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [pulsar-proxy, proxy-conf, broker-service-url, service-discovery, forward-authorization-credentials]
level: practitioner
status: docs-checked
description: "Configure the Pulsar proxy gateway: broker URLs vs service discovery, TLS URLs, separate proxy and client identities, credential forwarding and the perimeter-security caveat."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/administration-proxy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: put an optional gateway in front of brokers when clients cannot or should not reach them directly (cloud, Kubernetes).

Security stance: the proxy is not intended for the public internet; its design assumes network perimeter security (private networks). If that is not possible, the alternative is the proxy SNI routing feature with a properly secured solution. Multiple advertised listeners is another way to expose a cluster, also needing perimeter security.

Option 1, broker URLs (more secure; `conf/proxy.conf`):
```properties
brokerServiceURL=pulsar://brokers.example.com:6650
brokerWebServiceURL=http://brokers.example.com:8080
functionWorkerWebServiceURL=http://function-workers.example.com:8080
```
TLS variant: `brokerServiceURLTLS=pulsar+ssl://brokers.example.com:6651`, `brokerWebServiceURLTLS=https://brokers.example.com:8443`, and an https `functionWorkerWebServiceURL`. Skip `functionWorkerWebServiceURL` if you do not use functions. The hostnames should be a DNS entry or virtual IP backed by several brokers so one broker failure does not cut the proxy off. Open ports 6650 and 8080 (6651 and 8443 for TLS). Proxy authorization needs metadata-store access; without it, disable authorization at the proxy (brokers still authorize forwarded requests).

Option 2, service discovery through the metadata store (not recommended in production):
```properties
metadataStoreUrl=oxia://oxia-1.example.com:6648/broker
configurationMetadataStoreUrl=oxia://oxia-1.example.com:6648/broker
```
or ZooKeeper hosts on port 2181 and the configuration store on 2184. Opening those ACLs lets a compromised proxy reach the metadata store.

Authentication and TLS: client-to-proxy and proxy-to-broker use separate identities. Set `brokerClientAuthenticationPlugin` and `brokerClientAuthenticationParameters` for the proxy's own broker connection and list its role in the broker's proxy roles. For token auth set `forwardAuthorizationCredentials=true` on the proxy (brokers default to `authenticateOriginalAuthData=true`); for TLS client-certificate or SASL set it false on the brokers. For TLS to brokers set `tlsEnabledWithBroker=true`; hostname verification is on by default.

Target restriction: the proxy trusts clients to supply target broker addresses, so limit proxied connections with `brokerProxyAllowedHostNames` (a `*` wildcard matches any character, including dots) and optionally `brokerProxyAllowedIPAddresses`; the page ties this to CVE-2022-24280.

## Checked

2026-11-03. Confirmed against the pulsar-site page administration-proxy: security warning, broker-URL and service-discovery settings, ports, authentication and TLS settings, and the target-restriction settings. Removed the invented Verify step.

Method: documentation only; no commands were run.
