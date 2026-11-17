---
id: computing-software.software-engineering.elixir.credo-custom-check-module
name: credo-custom-check-module
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, credo-check, use-credo-check, ast-traverse, issue-meta, custom-lint-rule, custom-credo-check]
level: advanced
status: draft
description: "Implement a custom Credo check with use Credo.Check, traverse the AST and register it via requires or checks in .credo.exs."
sources: ["https://hexdocs.pm/credo/adding_checks.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing custom Credo checks

**Goal:** enforce a team-specific rule automatically.

```elixir
defmodule MyApp.Checks.NoIOInspect do
  use Credo.Check, base_priority: :high, category: :warning,
    explanations: [check: "Remove IO.inspect calls before committing."]

  def run(%SourceFile{} = source_file, params) do
    issue_meta = IssueMeta.for(source_file, params)
    Credo.Code.prewalk(source_file, &traverse(&1, &2, issue_meta))
  end

  defp traverse({{:., _, [{:__aliases__, _, [:IO]}, :inspect]}, meta, _} = ast, issues, issue_meta) do
    {ast, [issue(issue_meta, meta[:line], "IO.inspect") | issues]}
  end
  defp traverse(ast, issues, _), do: {ast, issues}

  defp issue(issue_meta, line_no, trigger),
    do: format_issue(issue_meta, message: "Do not leave IO.inspect", line_no: line_no, trigger: trigger)
end
# .credo.exs: requires: ["./checks/"], checks: %{enabled: [{MyApp.Checks.NoIOInspect, []}]}
```

## Rules
- The exact helper API (`format_issue`, `IssueMeta`) is documented in Credo's "Adding checks" guide; check it for your Credo version.
- Test checks with `Credo.Test.Case` (`to_source_file |> run_check |> assert_issue`).
- Keep checks fast; they run on every file.

## Self-check
Add `IO.inspect(1)` to a file and confirm your check reports it.
