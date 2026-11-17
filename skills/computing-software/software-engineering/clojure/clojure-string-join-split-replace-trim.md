---
id: computing-software.software-engineering.clojure.clojure-string-join-split-replace-trim
name: clojure-string-join-split-replace-trim
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, clojure.string, join, split, replace, trim, upper-case, starts-with, includes, blank, format, clojure-string-api, clojure-strings-regex]
level: intro
status: docs-checked
description: "Manipulate strings with clojure.string (join, split, replace, trim, blank?, includes?, starts-with?, capitalize) and str/format/pr-str; know nil-handling."
sources: ["https://clojure.github.io/clojure/clojure.string-api.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# clojure.string

**Goal:** the everyday string toolkit.

```clojure
(require '[clojure.string :as str])
(str/join ", " ["a" "b"])        (str/split "a,b,,c" #",")    ;=> ["a" "b" "" "c"]  (trailing empties dropped)
(str/split "a,b,c" #"," 2)       (str/trim " x ")  (str/triml s)  (str/trimr s)
(str/replace "a.b" "." "-")      (str/replace s #"\d+" #(str "<" % ">"))   ; fn replacement receives match
(str/replace-first s "x" "y")    (str/blank? nil)  ;=> true
(str/includes? s "x")  (str/starts-with? s "x")  (str/ends-with? s "x")
(str/upper-case s)  (str/lower-case s)  (str/capitalize s)  (str/reverse s)
(str/split-lines s)  (str/index-of s "x")  (str/last-index-of s "x")
(str "a" 1 :k nil)               ;=> "a1:k"  (nil prints as empty)
(format "%05.2f|%s" 3.14159 "x")
```
- `str` on a lazy seq prints the object, not the elements: use `(apply str coll)` or `str/join`.
- `str/replace` with a string pattern is literal; with a regex, `$1` group references work in string replacements
  (use `str/re-quote-replacement` when the replacement has `$` or `\`).
- These functions expect strings; only `blank?` is documented to accept nil.
- Use `pr-str` for readable, `str` for display, `with-out-str` to capture printing.

## Failure modes
- `str/split` takes a regex pattern as its second argument, not a plain string.

## Self-check
Predict `(str/split "a,b,," #",")` and `(str/split "a,b,," #"," -1)`.

## Checked
2026-11-02. Confirmed: clojure.string API page and clojure.core API (str, format, pr-str, with-out-str, apply): join, split (with limit, trailing empties dropped), trim/triml/trimr, replace (string, regex, function replacement; $ group references; re-quote-replacement), replace-first, blank?, includes?, starts-with?, ends-with?, index-of, last-index-of, split-lines, upper-case, lower-case, capitalize, reverse. Removed: the empty-string split result, the NullPointerException on nil, the ClassCastException claim and the Locale note.
Method: documentation only; no commands were run.
