---
id: computing-software.messaging-and-integration.node-red.node-red-function-node-patterns
name: node-red-function-node-patterns
category: computing-software
field: messaging-and-integration
product: node-red
tags: [node-red, function-node, javascript, msg, multiple-outputs, node-send, async, on-start, on-stop]
level: practitioner
status: docs-checked
description: "Write Node-RED Function nodes correctly: return rules, multiple outputs, sending several messages, async callbacks with node.send and node.done, and the On Start and On Stop tabs."
sources: ["https://nodered.org/docs/user-guide/writing-functions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Writing Function nodes in Node-RED

The Function node body is the body of a JavaScript function that receives `msg`. It must return a message object (not a number or string, which is an error), an array of messages, or `null`, which sends nothing and ends the flow. The returned object can be a new one, but that loses properties of the received message and breaks flows such as HTTP In/Response that need `msg.req` and `msg.res`; normally return the message you were given.

Multiple outputs: set the output count in the edit dialog and return an array with one entry per output, for example `return [ null, msg ];` sends only to the second output. An entry can itself be an array of messages, which the next nodes receive one at a time in order. `node.outputCount` is the configured number of outputs.

Asynchronous work: you cannot return the message at the end; call `node.send(msg)` instead, with the same message arrangement as a return, then `return;`. The node clones every message passed to `node.send`; pass `false` as a second argument (`node.send(msg, false)`) to ask the runtime not to clone the first message, for uncloneable content or to cut overhead. Call `node.done()` when the async work finishes so the runtime can track the message.

Start and stop: the On Start tab (labelled Setup before 1.3.0, available since 1.1.0) runs whenever the node starts, for example to initialise context; it can return a Promise, and messages arriving earlier are queued. To tidy up async work on redeploy, either register `node.on('close', function() { ... })` or use the On Stop tab.

Logging: `node.log`, `node.warn` and `node.error` write to the console; warn and error also appear in the debug sidebar. `node.trace` and `node.debug` are not seen unless a logger captures those levels. To trigger a Catch node on the same tab, call `node.error("hit an error", msg)` with the original message and return nothing.

Context from a Function node uses the `context`, `flow` and `global` variables; see the context skill.

## Checked

2026-11-04. Confirmed against the Node-RED user guide page Writing Functions. Removed: the claims that skipping the clone is faster for big payloads and makes later changes visible downstream, the Complete node wording and the leak-on-redeploy remark.

Method: documentation only; no commands were run.
