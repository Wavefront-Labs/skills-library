---
id: computing-software.cloud-infrastructure-engineering.aws.amazon-mq-activemq-network-of-brokers-and-migration
name: amazon-mq-activemq-network-of-brokers-and-migration
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, amazon-mq, activemq, network-of-brokers, mq-migration, rabbitmq-federation, message-broker]
level: practitioner
status: docs-checked
description: "Design Amazon MQ for ActiveMQ networks of brokers (hub-and-spoke, mesh, duplex connectors) and migrate from self-managed ActiveMQ or RabbitMQ with minimal downtime."
sources: ["https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/network-of-brokers.html", "https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/amazon-mq-creating-configuring-network-of-brokers.html", "https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/child-element-details.html", "https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/rabbitmq-basic-elements-plugins.html", "https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/best-practices-activemq.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Amazon MQ: ActiveMQ network of brokers and migration

## When to use a network of brokers
- Spread load and improve availability and fault tolerance across several simultaneously active
  brokers (single-instance or active/standby, mixed freely).
- Connect brokers in different regions, or partly migrate from on-premises to Amazon MQ (duplex
  connections are useful for that).
A network connector forwards messages on demand from one broker to another. For HA alone, an
**active/standby** broker is enough.

## Configure (broker XML configuration revision)
```xml
<networkConnectors>
  <networkConnector name="to-broker2" duplex="true" conduitSubscriptions="false"
      userName="netuser"
      uri="static:(ssl://b-xxxx-2.mq.eu-west-1.amazonaws.com:61617)"/>
</networkConnectors>
```
- The permitted `networkConnector` attributes in Amazon MQ are `name` (default `bridge`), `uri`,
  `userName`, `duplex` (default `false`) and `conduitSubscriptions` (default `true`); use only those.
- `duplex="true"`: broker B can send messages back to broker A over the same connection without its
  own connector, so define the connector on one side.
- `conduitSubscriptions` merges multiple consumers on one destination into a single logical
  subscription, which cuts network traffic but can disturb load balancing across consumers and
  misbehave with JMS selectors or durable topics; set `false` when fair distribution matters.
- `uri`: `static:(...)` is a one-to-one connection; AWS recommends the `masterslave:(url1,url2)`
  prefix for failover between brokers (it equals `static:failover:()?randomize=false&maxReconnectAttempts=0`).
- Credentials: create a user on each broker with the same username and password and give only
  `userName` in the connector. Do not set a `password` attribute; Amazon MQ adds it at runtime.
- Both brokers must be in the same VPC or peered VPCs, and the target broker's security group must
  allow the OpenWire port 61617 from the source broker.
- Apply by creating a new configuration revision and rebooting the broker (or waiting for the maintenance window).
- Optional client failover: `updateClusterClients`, `rebalanceClusterClients` and
  `updateClusterClientsOnRemove` on the `openwire` `transportConnector`.

## Migration from self-managed ActiveMQ
1. Create Amazon MQ broker with the same destinations and users (configuration XML).
2. Add a network connector from the old broker to Amazon MQ so messages on old queues drain to the new broker.
3. Move consumers to Amazon MQ first, then producers (change the failover URL:
   `failover:(ssl://b-1...:61617,ssl://b-2...:61617)`).
4. When old queues are empty, remove the connector and decommission.
Only the elements and attributes on the Amazon MQ "Permitted elements" pages are accepted in the
configuration, so remove anything else from the old `activemq.xml`.

## RabbitMQ engine
Amazon MQ for RabbitMQ has no ActiveMQ network connectors; it supports the **federation** plugin
(federated exchanges and queues) and the **shovel** plugin to move messages between brokers.
Only dynamic shovels are supported (configured through the management API at
`/api/parameters/shovel/{vhost}/{name}`), and a shovel cannot target a private broker.

## Gotchas
- Network connectors forward messages on demand.
- Do not disable advisory messages on brokers (AWS best practice), and do not rely on multicast
  broker discovery; Amazon MQ does not support it.
- The network of brokers page documents `networkConnector` support, while an introductory line on
  the broker configurations page says creating networks of brokers is not supported. The
  permitted-elements pages and the tutorial support the connector.

## Verify
- [ ] A message sent on broker 1 is consumed by a consumer on broker 2.
- [ ] Migration: old broker queue depth reaches 0 before cutover of producers.

## Checked

2026-10-27, AWS documentation (current release as read on that date). Amazon MQ Developer Guide network of brokers, network-of-brokers tutorial, networkConnector child element, RabbitMQ plugins, ActiveMQ best practices and broker configuration pages (table of contents read to find real page names). Fixed: networkTTL is not among the permitted networkConnector attributes (name, uri, userName, duplex, conduitSubscriptions) so it was removed; conduitSubscriptions defaults to true and the trade-off is documented; the recommended uri prefix is masterslave:; replaced the unsourced topology table and the unsupported-feature list. The "Migrating to Amazon MQ" source page does not exist in the guide table of contents and was dropped. Added: identical users on both brokers with no password attribute, same or peered VPCs, port 61617, advisory messages must not be disabled, RabbitMQ supports only dynamic shovels and not toward private brokers. Conflict noted between the network of brokers page and an introductory line on the broker configurations page. Removed the claim that ordering is not preserved across brokers.
Method: documentation only; no commands were run.
