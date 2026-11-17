---
id: computing-software.messaging-and-integration.node-red.node-red-context-scopes-and-storage
name: node-red-context-scopes-and-storage
category: computing-software
field: messaging-and-integration
product: node-red
tags: [node-red, context, flow-context, global-context, context-storage, localfilesystem, persistence, subflows]
level: practitioner
status: docs-checked
description: "Share state between Node-RED nodes with node, flow and global context, and make it survive restarts with a localfilesystem context store in settings.js."
sources: ["https://nodered.org/docs/user-guide/context", "https://nodered.org/docs/user-guide/writing-functions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Node-RED context: scopes and persistent storage

Context shares information between nodes without using messages. There are three scopes: node (only the node that set the value), flow (all nodes on the same flow tab) and global (all nodes). The global context can be preconfigured with values through `functionGlobalContext` in the settings file.

In a Function node the predefined variables `context`, `flow` and `global` give access: `flow.set("count", 123)` and `flow.get("count")`. In a subflow, flow context is shared by the subflow's nodes rather than the flow the subflow sits on. Since 0.20 prepend `$parent.` to the key to reach the parent flow's context, for example `flow.get("$parent.colour")`.

By default context is held in memory and cleared when Node-RED restarts. Since 0.19 `contextStorage` in `settings.js` can save it. The built-in modules are `memory` and `localfilesystem`; custom store plugins are possible. This makes the localfilesystem store the default:

```javascript
contextStorage: {
    default: {
        module: "localfilesystem"
    }
}
```

With defaults it stores files under `~/.node-red/context/` and caches values in memory, writing to disk only every 30 seconds. For several stores, `default` names the store used when a request does not specify one:

```javascript
contextStorage: {
    default: "memoryOnly",
    memoryOnly: { module: 'memory' },
    file: { module: 'localfilesystem' }
}
```

Several localfilesystem stores need different `dir` options. In a Function node pass the store name last: `flow.get("count", "file")`, `flow.set("count", 123, "file")`. The Change node set rule stores context values; with several stores the UI lets you pick the store. A Change node set to delete permanently removes context from the file store.

## Checked

2026-11-04. Confirmed against the Node-RED user guide pages Working with context and Writing Functions. Removed: the claim that context is lost on redeploy (page says restart) and the wrong description of $parent in Change nodes.

Method: documentation only; no commands were run.
