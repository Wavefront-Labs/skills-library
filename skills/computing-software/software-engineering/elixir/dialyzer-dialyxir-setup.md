---
id: computing-software.software-engineering.elixir.dialyzer-dialyxir-setup
name: dialyzer-dialyxir-setup
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, dialyzer, dialyxir, plt, success-typing, mix-dialyzer, ignore-warnings]
level: advanced
status: draft
description: "Add dialyxir, build the PLT, read warnings and silence known ones in .dialyzer_ignore.exs; understand Dialyzer reports only definite discrepancies."
sources: ["https://hexdocs.pm/dialyxir", "https://www.erlang.org/doc/apps/dialyzer/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dialyzer with dialyxir

**Goal:** run Dialyzer in an Elixir project and keep CI clean.

```elixir
# mix.exs
defp deps, do: [{:dialyxir, "~> 1.4", only: [:dev, :test], runtime: false}]   # check the current version on Hex
def project do
  [dialyzer: [plt_add_apps: [:mix, :ex_unit], plt_local_path: "priv/plts",
              flags: [:error_handling, :unmatched_returns]]]
end
```
```bash
mix dialyzer                       # first run builds the PLT (slow), later runs are fast
mix dialyzer --format short
mix dialyzer.explain unknown_function
```
```elixir
# .dialyzer_ignore.exs  (list of strings, regexes or {file, warning_type} tuples)
[~r/lib\/generated_.*/, {"lib/foo.ex", :no_return}]
```

## Rules
- Dialyzer uses success typing: it only warns when code can never succeed; absence of warnings is not proof of correctness.
- Cache the PLT in CI (keyed on OTP + Elixir versions and mix.lock) because building takes minutes.
- Add the apps you depend on to `plt_add_apps` if their types are missing ("unknown function" warnings).
- Treat warnings as bugs or fix the spec; ignore only with a comment.

## Failure modes
- Stale PLT after upgrading OTP/Elixir: delete `_build/*/dialyxir_*` or the local PLT path and rebuild.

## Self-check
Introduce a call with a wrong argument type to a function that has a spec and confirm `mix dialyzer` reports it.
