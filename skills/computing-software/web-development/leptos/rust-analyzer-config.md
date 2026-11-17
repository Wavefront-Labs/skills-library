---
id: computing-software.web-development.leptos.rust-analyzer-config
name: rust-analyzer-config
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, rust-analyzer, editor, macros, features, vscode, neovim, developer-experience]
level: practitioner
status: docs-checked
description: "Configure rust-analyzer for Leptos: ignore the server (and optionally component) proc macros and enable csr, ssr or hydrate features per editor."
sources: [https://book.leptos.dev/getting_started/leptos_dx.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configure rust-analyzer for Leptos projects

Goal: get working autocompletion inside `#[component]` and `#[server]`, and make feature-gated code show as active.

## 1. Ignore proc macros

Macros can expand to anything, so rust-analyzer struggles when input is mid-edit. Tell it to ignore Leptos macros, especially `#[server]` (it annotates function bodies but does not transform anything inside them). Since Leptos 0.5.3 rust-analyzer supports `#[component]`, but if you hit issues you may also ignore `component`; the cost is that rust-analyzer then does not know your props, which can produce its own warnings.

VSCode `settings.json`:

```json
"rust-analyzer.procMacro.ignored": {
	"leptos_macro": [
        // optional:
		// "component",
		"server"
	],
}
```

Helix, in `.helix/languages.toml`:

```toml
[[language]]
name = "rust"

[language-server.rust-analyzer]
config = { procMacro = { ignored = { leptos_macro = [
	# Optional:
	# "component",
	"server"
] } } }
```

Neovim (via `vim.lsp.config('rust_analyzer', ...)`), Zed and SublimeText use the same `procMacro.ignored.leptos_macro` setting; the book gives their exact blocks.

## 2. Enable Cargo features

By default rust-analyzer only uses default features. Leptos uses `csr` for client-side apps, and `ssr` (server code) and `hydrate` (browser-only code) for SSR apps. With cargo-leptos, if `ssr`-gated code shows as inactive, add `"rust-analyzer.cargo.features": ["ssr"]` (or use `rust-analyzer.cargo.allFeatures`). To enable everything, VSCode `settings.json`:

```json
{
  "rust-analyzer.cargo.features": "all"
}
```

For other editors search for `rust-analyzer.cargo.features` or `rust-analyzer.cargo.allFeatures` (Helix uses `allFeatures = true` under `[language-server.rust-analyzer.config.cargo]`).

## Related

- Formatting `view!` code: `computing-software.web-development.leptos.leptosfmt-setup`

## Checked

2026-11-07: Read in full: getting_started/leptos_dx.md (the 0.5.3 note, the procMacro.ignored setting for leptos_macro, and the cargo features setting with ssr and allFeatures). Config keys and values in the skill match the page text. No claims were trimmed. No editor was run.

Method: documentation only; no commands were run.
