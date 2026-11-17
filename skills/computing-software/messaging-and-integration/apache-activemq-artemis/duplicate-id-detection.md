---
id: computing-software.messaging-and-integration.apache-activemq-artemis.duplicate-id-detection
name: duplicate-id-detection
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,duplicate-detection,amq-dupl-id,hdr-duplicate-detection-id,clearduplicateidcache,once-and-only-once,activemq-artemis]
level: practitioner
status: docs-checked
description: "Filter duplicate sends by setting the unique _AMQ_DUPL_ID string property; the broker keeps a circular per-address cache and logs AMQ222059."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/duplicate-detection.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Duplicate message detection (sending)

**Goal:** let producers safely resend after an ambiguous failure (the server or connection died before the send or commit reply arrived) without delivering the same message twice. Transactions do not solve this, because a commit can also be indeterminate.

## Use
Set the property `_AMQ_DUPL_ID` to a unique value; any scheme is fine, such as a UUID. Core clients can use `Message.HDR_DUPLICATE_DETECTION_ID`. In JMS the value must be a `String`; in the Core API it can be `String`, `SimpleString` or `byte[]`.
```java
ClientMessage message = session.createMessage(true);
SimpleString myUniqueID = SimpleString.of("This is my unique id");
message.putStringProperty(HDR_DUPLICATE_DETECTION_ID, myUniqueID);
```
In a transaction you only need to set it once; if any message in it is a duplicate, the whole transaction is ignored.

## Semantics
The broker keeps a circular, fixed-size, per-address cache of IDs. If the ID is already cached, the message is routed to no queue and the broker logs `AMQ222059: Duplicate message detected - message will not be routed`. Otherwise the ID is cached and the message routed. IDs leave the cache only when overwritten by the n+1th entry or when cleared with the `clearDuplicateIdCache` operation on the address's `AddressControl`. Acknowledgement or expiry of the message does not remove its ID.

Used to move messages between nodes, the manual says this gives once-and-only-once like XA with less overhead.

## Checked

Method: docs-checked 2026-11-09 against duplicate-detection.adoc (read in full). Removed the Verify step.
