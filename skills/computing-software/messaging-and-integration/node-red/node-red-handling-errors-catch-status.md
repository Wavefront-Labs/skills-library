---
id: computing-software.messaging-and-integration.node-red.node-red-handling-errors-catch-status
name: node-red-handling-errors-catch-status
category: computing-software
field: messaging-and-integration
product: node-red
tags: [node-red, error-handling, catch-node, status-node, msg-error, uncaught-exception, complete-node]
level: practitioner
status: docs-checked
description: "Handle failures in Node-RED flows with the Catch and Status nodes, read msg.error, understand the loop limit, and know which errors cannot be caught."
sources: ["https://nodered.org/docs/user-guide/handling-errors"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Handling errors in Node-RED flows

A node can report an error in two ways: write to the log only, or notify the runtime so a flow can be triggered. Three kinds result:
- Catchable: the node notified the runtime (a Function node does this with `node.error("text", msg)`). A Catch node can handle it, and an error caught by a Catch node is not logged to the Debug sidebar.
- Uncatchable: the node only logs the error (shown in the Debug sidebar and log). A node may offer other signals, such as its status, which a Status node can watch, or a message with an extra property.
- `uncaughtException`: caused by bugs in nodes, usually an async task with no error handler. It shuts the whole runtime down and cannot be handled in a flow; identify the node and raise an issue against it.

The message leaving a Catch node is the one the failing node provided, with `msg.error`: `message`, and `source` with the node `id`, `type`, `name` and `count`. `count` is how many times the message was thrown by that node; the runtime lets a message loop 9 times before logging another, uncatchable error to break the loop, and deleting `count` disables the check. An earlier `msg.error` is moved to `msg._error`.

By default a Catch node is triggered by all nodes on its tab but can target specific nodes. Two Catch nodes targeting the same node both fire. A Catch node set to all nodes can be limited to errors not already caught by another Catch node, so you can add a catch-everything-else handler. For an error inside a subflow, the runtime first looks for Catch nodes in the subflow, then propagates to the flow containing the instance.

Not every problem is an error event: MQTT nodes losing their broker connection change status instead. The Status node reports those changes; its message has a `status` property (`fill`, `shape`, `text`, `source` with `id` and `type`).

## Checked

2026-11-04. Confirmed against the Node-RED user guide page Handling errors. Removed: the group-scoped Catch claim and 'sometimes extra detail' wording; corrected the loop-limit and uncatchable-error explanations.

Method: documentation only; no commands were run.
