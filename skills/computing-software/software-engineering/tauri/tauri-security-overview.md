---
id: computing-software.software-engineering.tauri.tauri-security-overview
name: tauri-security-overview
category: computing-software
field: software-engineering
product: tauri
tags: [security-overview, tauri, trust-boundaries, disclosure]
level: intro
status: docs-checked
description: "Understand Tauri's security model: trust boundaries, the IPC layer, OS-provided WebViews and how to report vulnerabilities."
sources:
  - "https://v2.tauri.app/security/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri security overview

Goal: understand where Tauri draws its security lines. The security of your app is the sum of Tauri itself, all Rust and npm dependencies, your code, and the devices that run it.

## Trust boundaries

Tauri separates Rust code written for the application core from frontend code in any framework or language the system WebView understands. Data passed between the two must be inspected and strongly defined; without access control at the boundary, attackers can elevate and abuse privileges. The IPC layer bridges the two groups and enforces the boundary.

- Code run by plugins or the application core has full access to system resources and is not constrained.
- Code in the WebView only reaches resources exposed through the well-defined IPC layer.
- Access to core commands is restricted by capabilities in the application configuration; individual command implementations enforce the optional fine-grained access levels also defined there.

Components of boundary enforcement: Permissions, Scopes, Capabilities, Runtime Authority. Tauri cannot provide a hardening guide for every frontend stack, but offers generic features to contain the attack surface: Content Security Policy (CSP) and the Isolation Pattern.

## Not bundling WebViews

Tauri relies on the OS WebView rather than bundling one. The main security reason is the time from publication of a patched WebView to rollout to end users: WebView and OS package maintainers have on average been significantly faster at patching than application developers who bundle the WebView. Tauri does not call bundling inherently insecure; the current design is a trade-off that significantly reduces known vulnerabilities in the wild.

## Ecosystem documents

Ecosystem Security, Application Lifecycle Threats, and Future Work describe how Tauri secures its development process and known threats.

## Coordinated disclosure

Do not comment publicly on a suspected security issue. Preferred: GitHub Vulnerability Disclosure (private reporting) on the affected repository, or the Tauri repository at https://github.com/tauri-apps/tauri/security/advisories/new if in doubt. Alternatively email security@tauri.app. There is no budget for security bounties, though coordinated disclosure may sometimes be rewarded.

## Checked
2026-11-08. Read the Tauri v2 security overview page (tauri-docs, v2 branch) in full; claims match. Linked sub-pages were not read.
Method: documentation only; no commands were run.
