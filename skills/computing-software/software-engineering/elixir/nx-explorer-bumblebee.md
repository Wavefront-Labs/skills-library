---
id: computing-software.software-engineering.elixir.nx-explorer-bumblebee
name: nx-explorer-bumblebee
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, nx, tensor, explorer, dataframe, bumblebee, exla, axon, numerical-elixir, nx-explorer]
level: advanced
status: draft
description: "Understand Nx tensors and defn, backends (EXLA), Explorer dataframes and where Bumblebee/Axon fit for ML in Elixir."
sources: ["https://hexdocs.pm/nx", "https://hexdocs.pm/explorer"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Numerical Elixir (Nx), Explorer and Bumblebee overview

**Goal:** know the numeric/ML stack and its basic usage.

```elixir
Mix.install([{:nx, "~> 0.9"}, {:exla, "~> 0.9"}])      # check current versions
Nx.global_default_backend(EXLA.Backend)
t = Nx.tensor([[1, 2], [3, 4]], type: :f32)
Nx.dot(t, t) ; Nx.sum(t, axes: [0]) ; Nx.shape(t)
defmodule M do
  import Nx.Defn
  defn softmax(x), do: Nx.exp(x) / Nx.sum(Nx.exp(x))   # numerical definitions compile to the backend
end
# Explorer: df = Explorer.DataFrame.from_csv!("data.csv"); DataFrame.filter(df, col > 3)
```

## Rules
- Nx tensors are immutable and typed (`:f32`, `:s64`); the default backend is slow and binary-based; use EXLA or Torchx for performance.
- `defn` restricts to a numerical subset of Elixir and is JIT-compiled.
- Explorer wraps the Polars engine (a Rust NIF) for dataframes.
- Bumblebee loads pre-trained models (for example from Hugging Face) on top of Nx/Axon.
- API versions move quickly; consult the current docs.

## Self-check
Create two tensors, add them, and inspect their shape and type.
