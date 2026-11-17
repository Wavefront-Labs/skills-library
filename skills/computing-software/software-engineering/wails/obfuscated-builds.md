---
id: computing-software.software-engineering.wails.obfuscated-builds
name: obfuscated-builds
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, obfuscation, garble, build, bindings]
level: practitioner
status: docs-checked
description: "Produce an obfuscated Wails build with garble, customise garble arguments, and keep bound method calls working by using the generated wailsjs bindings."
sources: [https://wails.io/docs/guides/obfuscated]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Obfuscated builds with garble

Goal: build a Wails app obfuscated by garble without breaking calls from the frontend to Go.

## Method

```bash
wails build -obfuscated
wails build -obfuscated -garbleargs "-literals -tiny -seed=myrandomseed"
```
The page's prose and first snippet disagree on the flag spelling (`-obfuscate` in the text, `-obfuscated` in the command); the commands shown use `-obfuscated`. `-garbleargs` passes custom garble settings. Both settings can be persisted in the project config (project-config reference).

## How bindings change

In a normal build, bound methods are reachable under `window.go` and called by fully qualified function name. In an obfuscated build, methods are bound by ID instead of name, and the generated bindings in the `wailsjs` directory use those IDs.

## Rule

Your app must call backend methods through the generated `wailsjs` bindings to work in obfuscated mode. Do not call `window.go...` by name. Example of a safe import:
```js
import { Greet } from "../../wailsjs/go/main/App";
Greet("World");
```
The bindings are regenerated with IDs, so this call works unchanged in both modes.

## Gaps

The page does not describe garble installation or which garble flags are recommended.

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Obfuscated Builds" guide.

Corrected or removed: Nothing needed removing; every concrete claim matched the page text.

Method: documentation only; no commands were run.
