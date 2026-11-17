---
id: computing-software.software-engineering.tauri.tauri-ipc-concepts
name: tauri-ipc-concepts
category: computing-software
field: software-engineering
product: tauri
tags: [ipc-concepts, tauri, events, commands]
level: intro
status: docs-checked
description: "Choose between Tauri's two IPC primitives, Events and Commands, and understand why asynchronous message passing is safer than shared memory."
sources:
  - "https://v2.tauri.app/concept/inter-process-communication/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri inter-process communication (IPC)

Goal: pick the right IPC primitive between the Frontend (WebView) and the Core.

## Model

Tauri uses Asynchronous Message Passing: processes exchange requests and responses serialized in a simple data representation, much like client-server communication on the internet. It is safer than shared memory or direct function access because the recipient is free to reject or discard requests. If the Core decides a request is malicious, it discards it and never executes the corresponding function.

Two patterns have their own guides: Brownfield and Isolation.

## Events

- Fire-and-forget, one-way messages.
- Best suited to lifecycle events and state changes.
- Unlike Commands, can be emitted by both the Frontend and the Tauri Core.
- Under the hood events still use Commands; access to the events API is controlled by the Event permissions.

## Commands

- A foreign-function-interface-like abstraction over IPC messages. Because they still use message passing, they do not share the security pitfalls of real FFI.
- The primary API, `invoke`, is similar to the browser's `fetch` API: the Frontend invokes Rust functions, passes arguments and receives data.
- A JSON-RPC-like protocol serializes requests and responses, so all arguments and return data must be serializable to JSON.

## Choosing

- Need a result back, or to call Rust with arguments: Command (`invoke`).
- Need to notify about a lifecycle event or state change, possibly from the Core to the Frontend: Event.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/concept/inter-process-communication/ (page text including code blocks and tabs read in full).
Removed: the ACL core-permissions pointer and the command invocation flow sentence (the flow is only shown in an image on the page).
Method: documentation only; no commands were run.
