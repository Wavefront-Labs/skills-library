---
id: computing-software.web-development.webassembly.blazor-and-rust-ui
name: blazor-and-rust-ui
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, blazor-webassembly, yew-leptos, aot-compilation, wasm]
level: practitioner
status: docs-checked
description: ".NET and Rust frontends"
sources: ["https://raw.githubusercontent.com/dotnet/AspNetCore.Docs/main/aspnetcore/blazor/webassembly-build-tools-and-aot.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blazor WebAssembly and non-JS UI frameworks

Goal: build apps in non-JS languages.
- Blazor WebAssembly without AOT runs your .NET IL on an interpreter implemented in Wasm (with partial JIT support from .NET 8, informally the Jiterpreter).
- AOT compiles the .NET code to Wasm: faster at runtime, larger download. The page says most AOT apps are about twice the IL size, and AOT does not trim managed DLLs on publish. Publishing in `Release` also runs IL linking to shrink the app.
- Enable with `<RunAOTCompilation>true</RunAOTCompilation>`; AOT happens on publish only.
- Rust UI frameworks (Yew, Leptos, Dioxus) are not covered by a source here: check each project's own documentation for bundle size and rendering model before committing.
- Evaluate bundle size, load time and ecosystem before choosing.
Verify: initial load size is within budget.

## Checked

2026-11-08. Confirmed in the ASP.NET Core Blazor WebAssembly build tools and AOT page (read in full).
Removed as unconfirmed: all Rust framework claims beyond naming them as an option to evaluate, and the statement about hydration.
Method: documentation only; no commands were run.
