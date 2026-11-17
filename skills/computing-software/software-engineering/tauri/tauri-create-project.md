---
id: computing-software.software-engineering.tauri.tauri-create-project
name: tauri-create-project
category: computing-software
field: software-engineering
product: tauri
tags: [create-project, tauri]
level: intro
status: docs-checked
description: "Scaffold a Tauri app with create-tauri-app, or add Tauri to an existing frontend with the Tauri CLI."
sources:
  - "https://v2.tauri.app/start/create-project/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create a Tauri project

Goal: a running Tauri app, either from a template or on top of an existing frontend.

## Option 1: create-tauri-app

Run one of: `sh <(curl https://create.tauri.app/sh)` (Bash), `irm https://create.tauri.app/ps | iex` (PowerShell), `npm create tauri-app@latest`, `yarn create tauri-app`, `pnpm create tauri-app`, `deno run -A npm:create-tauri-app`, `bun create tauri-app`, or `cargo install create-tauri-app --locked` then `cargo create-tauri-app`.

Prompts: project name, identifier (default `com.tauri-app.app`), frontend language (Rust, TypeScript / JavaScript, .NET), package manager, UI template (for example Vanilla, Vue, Svelte, React, Solid, Angular, Preact; Yew, Leptos, Sycamore for Rust; Blazor for .NET) and flavor (TypeScript or JavaScript). If unsure, the page suggests TypeScript / JavaScript, pnpm, Vanilla, TypeScript.

Then run, for example with pnpm: `cd tauri-app`, `pnpm install`, `pnpm tauri dev`. With Cargo: `cargo install tauri-cli --version "^2.0.0" --locked`, then `cargo tauri dev`.

## Option 2: manual setup with the Tauri CLI

1. Create the frontend (for example `npm create vite@latest .` in a new `tauri-app` directory).
2. Install the CLI: `npm install -D @tauri-apps/cli@latest` (or the pnpm/yarn/bun/deno equivalent; with cargo, `cargo install tauri-cli --version "^2.0.0" --locked`, which must be installed globally).
3. Find the dev server URL; Vite's default is `http://localhost:5173`.
4. Run `npx tauri init` (or `pnpm tauri init`, `cargo tauri init`, ...). It asks for app name, window title, web assets location (`..`), dev server URL, frontend dev command and frontend build command, and creates a `src-tauri` directory.
5. In `vite.config.ts`, set `server.watch.ignored` to `["**/src-tauri/**"]` so Vite does not watch `src-tauri`.
6. Verify with `npx tauri dev` (or the equivalent); it compiles the Rust code and opens a window with your web content.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/start/create-project/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
