---
id: computing-software.software-engineering.ruby.ruby-csv-processing
name: ruby-csv-processing
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, csv-processing, csv]
level: practitioner
status: draft
description: "Stream, parse and write CSV in Ruby with headers, converters, encodings and formula-injection protection."
sources: ["https://ruby.github.io/csv/", "https://docs.ruby-lang.org/en/master/CSV.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CSV parsing and generation

`csv` became a bundled gem in Ruby 3.4, so add `gem "csv"` to the Gemfile when running under Bundler on 3.4 or later (earlier versions ship it in the default set; confirm for your Ruby).

```ruby
require "csv"
CSV.foreach("in.csv", headers: true, header_converters: :symbol,
            converters: :numeric, encoding: "bom|utf-8") do |row|
  puts row[:email]          # CSV::Row; row.to_h for a Hash
end

CSV.open("out.csv", "w", write_headers: true, headers: %w[id name]) do |csv|
  records.each { |r| csv << [r.id, r.name] }
end

CSV.parse(str, col_sep: ";", liberal_parsing: true)
```
Use `CSV.foreach` (streaming) for large files; `CSV.read` / `CSV.table` loads everything into memory.

## Gotchas
- `CSV::MalformedCSVError` usually means a stray quote or the wrong `col_sep`/`quote_char`; report `e.message` (it includes the line number).
- Excel files start with a BOM; open with `encoding: "bom|utf-8"` or the first header will contain an invisible character.
- Built-in converters such as `:numeric` and `:date` mutate data (leading zeros are lost on `"007"`); keep ID columns as strings with a custom converter.
- Formula injection: cells beginning with `=`, `+`, `-` or `@` run as formulas when opened in a spreadsheet. Prefix such user-supplied values with `'` when exporting.

Verify: round-trip a file containing a quoted newline, a comma and a leading-zero ID, and diff the output with the input.
