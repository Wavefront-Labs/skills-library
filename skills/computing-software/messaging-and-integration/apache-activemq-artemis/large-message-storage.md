---
id: computing-software.messaging-and-integration.apache-activemq-artemis.large-message-storage
name: large-message-storage
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,large-messages,large-messages-directory,large-message-sync,large-message-table-name,minlargemessagesize,activemq-artemis]
level: practitioner
status: docs-checked
description: "Store large messages as files outside memory with large-messages-directory, large-message-sync and the JDBC large message table; split by minLargeMessageSize."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/large-messages.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Large message storage

Messages beyond a configured size are held as a thin object on the queue with a reference to the content (file or database table) instead of in memory. Supported on Core and AMQP.

## Server
With the file journal, content lives in `large-messages-directory` (default `data/largemessages`; the example in the manual uses `data/large-messages`):
```xml
<core>
   <large-messages-directory>data/large-messages</large-messages-directory>
   <large-message-sync>true</large-message-sync>
</core>
```
`large-message-sync` (default `true`) syncs the final-bytes write to storage. For best performance put the large messages directory on a different physical volume from the journal and paging directory.

JDBC persistence uses `large-message-table-name` inside `<store><database-store>` (default `LARGE_MESSAGE_TABLE`).

## Client threshold
The Core client splits messages above `minLargeMessageSize` into fragments (default 100KiB). Messages are encoded at 2 bytes per character, so ASCII text roughly doubles: a body that seems under the limit can become large after encoding.

## Checked
2026-11-03. Confirmed against the Artemis user manual page large-messages: directory and default, large-message-sync, JDBC table setting and default, minLargeMessageSize and encoding note. Removed: the Verify step.
Method: documentation only; no commands were run.
