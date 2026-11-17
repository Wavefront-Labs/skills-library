---
id: computing-software.messaging-and-integration.node-red.node-red-subflows-and-reuse
name: node-red-subflows-and-reuse
category: computing-software
field: messaging-and-integration
product: node-red
tags: [node-red, subflow, subflow-properties, status-output, flow-reuse, selection-to-subflow]
level: practitioner
status: docs-checked
description: "Package Node-RED logic as reusable subflows: create or convert a selection, wire one input and many outputs, add a status output, and define per-instance properties."
sources: ["https://nodered.org/docs/user-guide/editor/workspace/subflows"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Node-RED subflows

A subflow collapses a collection of nodes into a single node, to reduce visual complexity or package a reusable flow. It is added to the palette and instances are added like any node. A subflow cannot contain an instance of itself, directly or indirectly.

Create a blank one with menu Subflows, Create subflow, or convert a selection with Subflows, Selection to Subflow (the nodes are replaced by an instance). The conversion only works if wires coming into the selection connect to one node, because a subflow has at most one input; outputs can be many.

Edit by double clicking the subflow in the palette or by the Edit flow template button in an instance's dialog. It opens in a new tab, and unlike regular flow tabs subflow tabs can be closed. Inputs and outputs are grey square nodes wired as normal; the toolbar adds and removes them. The toolbar can add a status output, which updates the status of instance nodes from `msg.payload` as a string or a Status Object. The delete subflow button removes the subflow and all its instances.

The edit properties dialog has tabs for Properties (per-instance properties exposed as environment variables inside the subflow), Module Properties (version, licence and module name, for packaging as an npm module), Description (Markdown, shown in the Information sidebar) and Appearance (category, label, colour, icon, port labels).

## Checked

2026-11-04. Confirmed against the Node-RED user guide page Subflows. Removed: the 'context is per instance' and '$parent.' remarks (not on this page; see the context skill) and the closing advice to prefer properties over copying.

Method: documentation only; no commands were run.
