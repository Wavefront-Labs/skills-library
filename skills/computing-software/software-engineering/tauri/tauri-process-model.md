---
id: computing-software.software-engineering.tauri.tauri-process-model
name: tauri-process-model
category: computing-software
field: software-engineering
product: tauri
tags: [process-model, tauri, core-process, webview]
level: intro
status: draft
description: "Understand Tauri's multi-process model: a privileged Rust Core process orchestrating sandboxed WebView processes, and why that limits blast radius."
sources:
  - "https://v2.tauri.app/concept/process-model/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tauri process model

Goal: decide what code belongs in the Core process and what in the WebView.

## Why multiple processes

A single-process app freezes its UI during long computation, and one failing component crashes everything. Separate processes isolate crashes (an invalid process can be restarted), use multi-core CPUs better, and let you limit the blast radius of exploits by granting each process the minimum permissions it needs (the Principle of Least Privilege).

## Core process

Every Tauri app has one Core process: the entry point and the only component with full access to the operating system. It:

- creates and orchestrates windows, system-tray menus and notifications, via Tauri's cross-platform abstractions;
- routes all Inter-Process Communication, so you can intercept, filter and manipulate IPC messages in one central place;
- should manage global state such as settings or database connections, which synchronizes state between windows and protects business-sensitive data from the Frontend.

Tauri is implemented in Rust because Ownership guarantees memory safety with excellent performance.

One Core process manages one or more WebView processes, each reached through Events and Commands.

## WebView process

The Core does not render the UI. It spins up WebView processes using the operating system's WebView libraries, a browser-like environment executing HTML, CSS and JavaScript. Ordinary web tooling applies (many examples use Svelte and Vite).

- Always sanitize user input.
- Never handle secrets in the Frontend.
- Ideally defer as much business logic as possible to the Core to keep the attack surface small.

WebView libraries are not included in the executable but dynamically linked at runtime, which makes the app significantly smaller but means platform differences must be kept in mind. Currently: Microsoft Edge WebView2 on Windows, WKWebView on macOS, webkitgtk on Linux.
