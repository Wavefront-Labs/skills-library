---
id: computing-software.messaging-and-integration.node-red.node-red-messages-and-change-node
name: node-red-messages-and-change-node
category: computing-software
field: messaging-and-integration
product: node-red
tags: [node-red, msg, payload, change-node, jsonata, split, join, msg-parts, debug-node]
level: intro
status: docs-checked
description: "Understand the Node-RED message object, then reshape it with the Change node (set, change, delete, move), JSONata, and split and join sequences using msg.parts."
sources: ["https://nodered.org/docs/user-guide/messages"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Node-RED messages and the Change node

Flows pass messages between nodes: simple JavaScript objects with any set of properties. Most have `payload`, the default property most nodes work with, and Node-RED adds `_msgid`, an identifier for tracing a message through a flow. Property values can be any JavaScript type.

To understand a message, send it to a Debug node and open it in the Debug sidebar (by default it shows `msg.payload`, but it can show any property or the whole message). Hover over an element: one button copies its path (for example `payload.Phone[2].type`) for use in a Change or Function node, one copies the value as a JSON string (truncated for long arrays and Buffers), and one pins the element so it stays expanded.

A JSON string must be parsed to an object before its properties can be accessed; the JSON node does that conversion.

The Change node modifies messages without JavaScript and can access flow and global context. It has four operations: set a property (to a hardcoded value, to another message or flow/global property, or to the result of a JSONata expression), change a string property by search and replace, delete a property, and move a property. JSONata looks like JavaScript but differs; see jsonata.org. The Function node allows any JavaScript but needs familiarity with it.

Sequences: a message sequence is an ordered series of related messages. Each has `msg.parts` with `id` (sequence identifier), `index` (position) and `count` (total, if known); split also adds metadata the join node uses. Split turns one message into a sequence: a String or Buffer by a character (default `\n`), buffer sequence or fixed lengths; an Array into elements or fixed-length arrays; an Object into one message per key/value pair. Join turns a sequence into one message in Automatic (reverses a previous Split), Manual or Reduce (a JSONata expression run on each message, accumulated into one message) mode. Sort sorts a sequence by a property value or JSONata result; Batch creates new sequences from those received.

## Checked

2026-11-04. Confirmed against the Node-RED user guide page Working with messages. Removed: the typed-input list, the move example and JSONata formula, `type` in msg.parts, the 'own sequences' advice and the clone-on-branch claim, none of which are on the page.

Method: documentation only; no commands were run.
