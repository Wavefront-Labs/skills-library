---
id: computing-software.messaging-and-integration.apache-activemq-artemis.large-message-compression-and-streaming
name: large-message-compression-and-streaming
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,compresslargemessage,compressionlevel,jms-amq-inputstream,saveoutputstream,large-message-streaming,activemq-artemis]
level: advanced
status: docs-checked
description: "Compress Core large messages with compressLargeMessage and compressionLevel and stream bodies with InputStream/OutputStream or the JMS_AMQ_* object properties."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/large-messages.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Large message compression and streaming

## Compression (Core)
Set the boolean URL parameter `compressLargeMessage=true` to ZIP-compress the body as it is transferred. All compression and decompression happens in the client; the server does nothing special. `compressionLevel` accepts `-1` (default, about level 6-7) or 0-9; higher compresses more at the cost of speed and CPU. If the compressed size falls below `minLargeMessageSize` it is sent as a regular message, avoiding disk I/O in the server's large-message directory.

## Streaming
Bodies can be sent and received with `java.io` streams.
| Core method | JMS object property |
|---|---|
| `setBodyInputStream(InputStream)` | `JMS_AMQ_InputStream` |
| `setOutputStream(OutputStream)` (non-blocking) | `JMS_AMQ_OutputStream` |
| `saveOutputStream(OutputStream)` (blocks until done) | `JMS_AMQ_SaveStream` |

JMS sending example:
```java
BytesMessage message = session.createBytesMessage();
message.setObjectProperty("JMS_AMQ_InputStream", bufferedInput);
someProducer.send(message);
```
Receiving blocking: `messageReceived.setObjectProperty("JMS_AMQ_SaveStream", bufferedOutput);`. If you use the non-blocking output stream, keep the consumer alive until the message is fully received. In JMS, streaming works only with `StreamMessage` and `BytesMessage`.

For bodies over 2GiB, `getBodySize()` overflows an int; use the property `_AMQ_LARGE_SIZE`.

## Checked
2026-11-03. Confirmed against the Artemis user manual page large-messages, sections Compressed Large Messages, Streaming large messages and Streaming over JMS: parameters, levels, method and property table, JMS examples, StreamMessage and BytesMessage restriction, 2GiB note. Removed: the Verify step and a memory claim.
Method: documentation only; no commands were run.
