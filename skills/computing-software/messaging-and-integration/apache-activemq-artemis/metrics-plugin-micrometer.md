---
id: computing-software.messaging-and-integration.apache-activemq-artemis.metrics-plugin-micrometer
name: metrics-plugin-micrometer
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,metrics,micrometer,activemqmetricsplugin,meterregistry,loggingmetricsplugin,monitoring,activemq-artemis]
level: advanced
status: docs-checked
description: "Export broker metrics through Micrometer by configuring an ActiveMQMetricsPlugin in the broker.xml metrics element, with key/value plugin properties."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/metrics.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metrics via a Micrometer plugin

**Goal:** publish broker metrics to your monitoring system through the Micrometer facade.

Implement `org.apache.activemq.artemis.core.server.metrics.ActiveMQMetricsPlugin`:
```java
public interface ActiveMQMetricsPlugin extends Serializable {
   ActiveMQMetricsPlugin init(Map<String, String> options);
   MeterRegistry getRegistry();
   default void registered(ActiveMQServer server) { }
}
```
At startup the broker calls `init` with the options from XML, where the plugin should create and configure a `io.micrometer.core.instrument.MeterRegistry` (implementations come from the Micrometer code base). Later it calls `getRegistry`, then `registered` to give you a handle on the server, so the plugin can check whether the broker is operational and not starting up or shutting down.

## Shipped plugins
- `org.apache.activemq.artemis.core.server.metrics.plugins.LoggingMetricsPlugin`: logs metrics; a demo, not for production; no properties.
- `org.apache.activemq.artemis.core.server.metrics.plugins.SimpleMetricsPlugin`: in-memory, for testing; no properties.

## Configure
```xml
<metrics>
   <plugin class-name="org.example.MyMetricsPlugin">
      <property key="host" value="example.org" />
      <property key="port" value="5162" />
   </plugin>
</metrics>
```
Metrics for all addresses and queues are on by default; disable them for matching addresses with the `enable-metrics` address-setting set to `false`.

## Checked

Method: docs-checked 2026-11-09 against metrics.adoc (read in full). Removed the Verify step.
