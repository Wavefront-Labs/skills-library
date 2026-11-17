---
id: computing-software.messaging-and-integration.apache-camel.poll-enrich
name: poll-enrich
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, pollenrich, polling-consumer, timeout, file]
level: practitioner
status: docs-checked
description: "Camel Poll Enrich EIP: polling-consumer enrichment, timeout semantics (-1 blocks, 0 no wait, positive waits), dynamic file URIs, variableReceive and eagerLimitMaxMessagesPerPoll."
sources:
  - https://camel.apache.org/components/next/eips/pollEnrich-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Poll Enrich

Uses a Polling Consumer to fetch extra data, e.g. reading a file or downloading over FTP. Enrich uses a Producer instead.

`timeout` (default -1, milliseconds):
- negative: `receive`, waits until a message is available and may block forever
- zero: `receiveNoWait`, returns `null` if nothing is there
- positive: `receive(timeout)`, returns `null` on expiry

Other defaults: `aggregateOnException` false, `allowOptimisedComponents` true, `autoStartComponents` true, `ignoreInvalidEndpoint` false, `cacheSize` 0 (-1 off), `allowedSchemes` unset.

With no `aggregationStrategy` the polled message becomes the result (`file:inbox?fileName=data.txt` with a 10 second timeout makes the file content the body). With a strategy, `aggregate` receives the original first and the resource second; handle a null resource.

Dynamic URIs: `simple("seda:${header.queueName}")`. A file named `${body[customer]}.json` with `noop=true` stays in place; without it Camel moves it to `.camel`. `noop=true` alone turns on idempotent, so the file is skipped the next time; add `idempotent=false` to read it again. With `variableReceive` the body is unchanged and the variable is `null` if nothing arrived in time.

File components: from Camel 4.13 `eagerLimitMaxMessagesPerPoll` defaults to `true`; set `false` if files must be sorted before polling. File functions like `${file:onlyname.noext}` are evaluated per found file; other `fileName` expressions run against the message being enriched. `allowOptimisedComponents=false` evaluates the whole URI per message.

Verify: with a 10000 ms timeout and no file, the poll gives up at the timeout and yields null (the variable is null when `variableReceive` is used).

## Checked

Method: docs-only read of cited pages, 2026-11-08

Compared against the Camel Poll Enrich EIP page: timeout semantics (negative receive, zero receiveNoWait, positive receive(timeout)), defaults (timeout -1, aggregateOnException false, allowOptimisedComponents true, autoStartComponents true, ignoreInvalidEndpoint false, cacheSize 0 or -1, allowedSchemes unset), aggregate parameter order, null handling, dynamic URI examples, noop and idempotent behaviour, variableReceive and the Camel 4.13 eagerLimitMaxMessagesPerPoll default change all match. An idempotent caveat the page gives was added. No commands were run.
