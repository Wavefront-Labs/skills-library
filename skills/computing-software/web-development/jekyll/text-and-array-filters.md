---
id: computing-software.web-development.jekyll.text-and-array-filters
name: text-and-array-filters
category: computing-software
field: web-development
product: jekyll
tags: [markdownify, jsonify, number-of-words, sort-filter, array-filters, escape-filters]
level: practitioner
status: docs-checked
description: "Use Jekyll's text and array Liquid filters: markdownify, smartify, sassify, jsonify, xml/cgi/uri escape, number_of_words, sort, sample, push/pop, inspect."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_data/jekyll_filters.yml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Conversion: `markdownify` (Markdown to HTML), `smartify` (smart quotes), `sassify` / `scssify` (Sass or SCSS to CSS), `jsonify` (hash or array to JSON), `to_integer` (string or boolean to integer), `normalize_whitespace` (collapse whitespace to one space), `inspect` (string form for debugging).

Escaping:

- `xml_escape` for XML text.
- `cgi_escape`: `"foo, bar; baz?"` gives `foo%2C+bar%3B+baz%3F`; spaces become `+`.
- `uri_escape`: percent-encodes, spaces become `%20`, reserved characters are not escaped.

`number_of_words`: `"Hello world!"` gives 2. From 4.1.0 an argument handles CJK text: `'cjk'` counts every CJK character as a word; `'auto'` does the same but is faster when the string may not contain CJK.

`array_to_sentence_string`: `foo, bar, and baz`; `array_to_sentence_string: "or"` gives `foo, bar, or baz`.

`sort` takes optional arguments for hashes: a property name and nils order (`first` or `last`):

```liquid
{{ site.pages | sort: "title", "last" }}
```

`sample` picks a random value, or `sample: 2` picks two.

`push`, `pop`, `shift` and `unshift` are non-destructive: they copy the array and change the copy.

```liquid
{{ page.tags | push: "Spokane" }}
```

## Checked

2026-11-04. Confirmed against the Jekyll Liquid filters data: conversion, escape, number_of_words, array_to_sentence_string, sort, sample and array filters. Nothing removed.

Method: documentation only; no commands were run.
