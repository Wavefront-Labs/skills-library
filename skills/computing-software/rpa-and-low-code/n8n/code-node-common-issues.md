---
id: computing-software.rpa-and-low-code.n8n.code-node-common-issues
name: code-node-common-issues
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, code-node, return-format, require, static-data, credentials]
level: practitioner
status: docs-checked
description: "Troubleshoot the n8n Code node: required json item structure, import vs require, cannot find module, static data for globals and why credentials are inaccessible."
sources:
  - https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/common-issues
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: fix the usual Code node failures.

## Return format
Data between nodes is an array of objects each wrapping a `json` object:
```javascript
[ { "json": { /* your data */ } } ]
```
- `A 'json' property isn't an object`: you set `json` to an array. It must be an object.
- `Code doesn't return an object`: nothing was returned, or the result is `undefined`; check that referenced data exists in every execution.

## Modules
`'import' and 'export' may only appear at the top level`: the sandbox does not support them. Use `const express = require("express");`.
`Cannot find module '<module>'`: self-hosted only (modules are unsupported on Cloud). Install the module in the n8n environment (for Docker, extend the official image) and set `NODE_FUNCTION_ALLOW_BUILTIN` and `NODE_FUNCTION_ALLOW_EXTERNAL`.

## Global data
Use the workflow static data functions to keep simple values across and within executions (global or per node). If the aim is to avoid reprocessing items, the **Remove Duplicates** node can remember items across executions instead.

## Credentials
Code nodes cannot access credentials by design; `this.getCredentials()` fails with `this.getCredentials is not a function` and `$getCredentials` with `$getCredentials is not defined`. For authenticated calls use the HTTP Request node. For dynamic credentials, route with a Switch node, use expressions in credential fields, or use HTTP Request with Custom Auth to set headers, query or body from expressions.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/common-issues

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Removed the external task runner allowlist sentence (not on the page).

Method: documentation only; no commands were run.
