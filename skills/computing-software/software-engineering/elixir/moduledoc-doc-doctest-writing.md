---
id: computing-software.software-engineering.elixir.moduledoc-doc-doctest-writing
name: moduledoc-doc-doctest-writing
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, moduledoc, doc, doctest, since, deprecated, iex-prompt, docs-hidden, moduledoc-doctest, elixir-docs]
level: practitioner
status: docs-checked
description: "Write @moduledoc/@doc with examples as iex> doctests, mark since metadata and @deprecated and hide internals with @doc false."
sources: ["https://hexdocs.pm/elixir/writing-documentation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @moduledoc, @doc and doctests

**Goal:** documentation that doubles as tests, following the Elixir writing-documentation guide and `ExUnit.DocTest`.

```elixir
defmodule MyApp.Hello do
  @moduledoc """
  This is the Hello module.
  """
  @moduledoc since: "1.0.0"

  @doc """
  Says hello to the given `name`.

  Returns `:ok`.

  ## Examples

      iex> MyApp.Hello.world(:john)
      :ok

      iex> raise "some error"
      ** (RuntimeError) some error
  """
  @doc since: "1.3.0"
  def world(name) do
    IO.puts("hello #{name}")
  end

  @doc false                       # hidden from docs, but still public
  def internal, do: :ok

  @deprecated "Use world/1"        # emits a compile warning at call sites
  def hello(name), do: world(name)
end

defmodule MyModuleTest do
  use ExUnit.Case, async: true
  doctest MyApp.Hello
end
```

## Rules
- Documentation is Markdown, attached to `@moduledoc` (module), `@doc` (function or macro) and `@typedoc` (types). Metadata goes in a keyword list (`@doc since: "1.3.0"`, `@doc group: "Query"`).
- `@doc deprecated: "..."` only warns in the documentation; use the `@deprecated` attribute to warn when code calls the function.
- Recommendations: keep the first paragraph to one concise line (tools use it as the summary); reference modules by full name, local functions as `world/1`, external ones as `MyApp.Hello.world/1`, callbacks as `c:world/1`, types as `t:values/0`; start sections with `##` (first-level headers are reserved for module and function names); put the doc before the first clause of a multi-clause function (docs are per function and arity).
- Include examples under `## Examples`. Doctests: each new test starts on its own line with an `iex>` prefix; continue multi-line expressions with `...>`; the expected result is on the following line(s). Consecutive `iex>` expressions share bindings; an empty line between them makes separate tests. Expected exceptions start with `** (`.
- Doctests run through `doctest MyModule` inside an ExUnit case.
- `@moduledoc false` / `@doc false` hide a module or function from docs but do not make it private; imports still pull the function in. Alternatives: move it to a hidden module, or start the name with an underscore (such functions are treated as hidden and not imported).
- A private function with `@doc` triggers a warning and the content is discarded; use code comments for private functions.
- Documentation is a contract with API users; code comments are for readers of the source.

## Self-check
Change an expected result in an example and run `mix test`; the doctest fails.

## Checked
Date: 2026-11-02. Confirmed against the Elixir writing-documentation guide and ExUnit.DocTest docs (attributes, metadata, :deprecated vs @deprecated, recommendations, @doc false limits, doctest syntax, separate tests by empty line). Removed: four-space indentation rule, ArithmeticError example, ExDoc-specific claims, ## Options heading advice.
Method: documentation only; no commands were run.
