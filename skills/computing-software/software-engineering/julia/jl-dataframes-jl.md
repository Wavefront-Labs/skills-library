---
id: computing-software.software-engineering.julia.jl-dataframes-jl
name: jl-dataframes-jl
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-dataframes, dataframes-jl]
level: practitioner
status: draft
description: "Manipulate tables with the select/transform/combine mini-language, groupby and join functions."
sources: ["https://docs.julialang.org/en/v1/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DataFrames.jl select, transform, groupby and joins
- `df = DataFrame(a = 1:3, b = ["x","y","z"])`; `df.a`, `df[!, :a]` (no copy) vs `df[:, :a]` (copy); `df[df.a .> 1, :]`.
- `select(df, :a, :b => ByRow(uppercase) => :c)`, `transform`, `combine(groupby(df, :g), :x => mean => :m)`; `subset(df, :a => ByRow(>(1)))`.
- `innerjoin`, `leftjoin`, `outerjoin`, `antijoin(df1, df2, on = :id)`; `stack`/`unstack` reshape.
- Missing values are `missing`; `skipmissing`, `coalesce.(x, 0)`, `dropmissing(df)`; Statistics functions propagate `missing`.
- Read/write CSV: `CSV.read("f.csv", DataFrame)`, `CSV.write("o.csv", df)`; Arrow.jl or Parquet2.jl for columnar files.
Verify: `describe(df)` and `nrow` after joins.
