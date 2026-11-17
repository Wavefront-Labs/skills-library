---
id: computing-software.software-engineering.elixir.exdoc-generate-hexdocs
name: exdoc-generate-hexdocs
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, exdoc, mix-docs, groups-for-modules, extras, hexdocs, source-url]
level: practitioner
status: draft
description: "Add ex_doc, configure docs: in mix.exs (main, extras, groups) and run mix docs; hex publish uploads docs to HexDocs."
sources: ["https://hexdocs.pm/ex_doc"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Generating docs with ExDoc

**Goal:** produce navigable HTML docs for a library.

```elixir
# mix.exs
defp deps, do: [{:ex_doc, "~> 0.34", only: :dev, runtime: false}]   # check current version
def project do
  [name: "MyLib", source_url: "https://example.com/mylib", docs: [
     main: "readme", extras: ["README.md", "CHANGELOG.md", "guides/intro.md"],
     groups_for_modules: [Core: [MyLib, MyLib.Parser], Internal: ~r/Internal/],
     source_ref: "v#{@version}"]]
end
```
```bash
mix docs            # output in doc/index.html
mix hex.publish docs   # or `mix hex.publish` which also publishes docs
```

## Rules
- `main:` sets the landing page: a module name or an extra page basename.
- Cross-reference with backticks: `` `Enum.map/2` `` , `` `t:Account.t/0` `` , `` `c:Parser.parse/1` `` (callbacks), `` `m:Mod` `` is not needed.
- `mix docs` warns about unresolved references and hidden-module links; fix them.
- Livebooks and guides can be extras; keep `doc/` out of version control.

## Self-check
Run `mix docs` and click a `t:` link to confirm type cross-references resolve.
