---
id: computing-software.software-engineering.tauri.tauri-frontend-configuration
name: tauri-frontend-configuration
category: computing-software
field: software-engineering
product: tauri
tags: [frontend-config, tauri]
level: intro
status: docs-checked
description: "Check that a frontend framework fits Tauri's static-host model: SSG, SPA or MPA only, a mobile dev server, and a client-server split."
sources:
  - "https://v2.tauri.app/start/frontend/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri frontend configuration

Goal: integrate any frontend framework with Tauri.

Tauri is frontend agnostic and conceptually acts as a static web host. You give it a folder containing some mix of HTML, CSS, JavaScript and possibly WASM to serve to the webview it provides. Some frameworks need extra configuration to integrate.

## Configuration checklist

- Use static site generation (SSG), single-page applications (SPA) or classic multi-page apps (MPA). Tauri does not natively support server-based alternatives such as SSR.
- For mobile development, a development server of some kind is necessary that can host the frontend on your internal IP.
- Use a proper client-server relationship between your app and your APIs (no hybrid solutions with SSR).

## Framework guides

- JavaScript: Vite is recommended for SPA frameworks such as React, Vue, Svelte and Solid, and for plain JavaScript or TypeScript projects. Guides also exist for the meta-frameworks Next.js, Nuxt, Qwik and SvelteKit, which are typically designed for SSR and therefore need special configuration.
- Rust: guides exist for Leptos and Trunk.

If a framework is not listed, it may work with no additional configuration, or it may not be documented yet. Work through the checklist above to find common settings to check.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/start/frontend/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
