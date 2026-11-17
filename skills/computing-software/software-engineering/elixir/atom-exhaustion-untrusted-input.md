---
id: computing-software.software-engineering.elixir.atom-exhaustion-untrusted-input
name: atom-exhaustion-untrusted-input
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, atom-exhaustion, to-existing-atom, binary-to-term-safe, untrusted-input, path-traversal, zip-slip, safe-parse]
level: advanced
status: gated
description: "Never convert untrusted strings to atoms or deserialise arbitrary terms; sanitise file paths and use explicit allow-lists."
sources: ["https://hexdocs.pm/elixir/String.html#to_existing_atom/1", "https://erlef.github.io/security-wg/secure_coding_and_deployment_hardening/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Atom exhaustion and untrusted data

**Goal:** avoid the VM-specific classes of vulnerability.

```elixir
String.to_existing_atom(param)                    # raises if the atom does not exist
@allowed %{"asc" => :asc, "desc" => :desc}
dir = Map.fetch!(@allowed, param)                 # explicit allow-list is best
:erlang.binary_to_term(data, [:safe])             # still unsafe for function values; avoid for untrusted input
Path.safe_relative(user_path, base_dir)           # {:ok, path} | :error  (rejects ../ escapes)
Plug.Conn.get_req_header / Plug.Upload             # never trust the original filename: generate your own
Jason.decode(json, keys: :strings)                # default keeps string keys: do not use keys: :atoms on user JSON
```

## Rules
- Atoms are never collected, so creating them from user input lets an attacker crash the VM.
- `Code.eval_string`, `apply(String.to_atom(...))`, and `:erlang.binary_to_term/1` on untrusted data are remote code execution or DoS risks.
- Build file paths from IDs you control; check traversal with `Path.safe_relative/2`; extract archives with entry-name checks.
- Treat `System.cmd` arguments as data but never feed user input to a shell.
- The Erlang Ecosystem Foundation security working group publishes hardening guidance.

## Self-check
Try `String.to_existing_atom("never_seen_atom_xyz")` and read the ArgumentError.

## Checked

- Date: 2026-11-02.
- Source pages listed in `sources` were fetched where possible; String page fetched; the Plug, Path, :erlang and Jason calls and the ERLEF hardening page (only 930 characters readable) are not covered. Treat the specific names, flags and figures as unconfirmed (gated: unconfirmed, source is paywalled or blocked).

Method: documentation only; no commands were run.
