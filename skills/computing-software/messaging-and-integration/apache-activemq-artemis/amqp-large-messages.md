---
id: computing-software.messaging-and-integration.apache-activemq-artemis.amqp-large-messages
name: amqp-large-messages
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,amqpminlargemessagesize,amqp,large-message,acceptor,activemq-artemis]
level: advanced
status: docs-checked
description: "Set the AMQP large message threshold per acceptor with amqpMinLargeMessageSize (default 102400) and know what -1 does."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/large-messages.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AMQP large message threshold

Large message handling also applies to AMQP. Configure it on the acceptor with `amqpMinLargeMessageSize`; the default is `102400` (100 KBytes).

```xml
<acceptors>
   <acceptor name="amqp">tcp://0.0.0.0:5672?amqpMinLargeMessageSize=102400</acceptor>
</acceptors>
```
Setting it to `-1` disables AMQP large message support. Warning from the manual: with `-1`, an AMQP message may still be stored as a Core large message if it does not fit into the journal; that is the former behaviour, kept for compatibility.

## Related settings
The Core protocol threshold is the separate client URL parameter `minLargeMessageSize` (default 100KiB), and the on-disk location is `large-messages-directory` (see `large-message-storage`). `amqpMinLargeMessageSize` is set on the acceptor.

## Checked
2026-11-03. Confirmed against the Artemis user manual page large-messages, section Configuring AMQP Acceptor: property, default 102400, -1 and its warning. Removed: the Verify step and unsupported advice on choosing thresholds.
Method: documentation only; no commands were run.
