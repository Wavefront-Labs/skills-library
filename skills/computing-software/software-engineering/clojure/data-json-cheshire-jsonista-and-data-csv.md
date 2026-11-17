---
id: computing-software.software-engineering.clojure.data-json-cheshire-jsonista-and-data-csv
name: data-json-cheshire-jsonista-and-data-csv
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, json, csv, data.json, cheshire, jsonista, data.csv, parse-string, generate-string, serialization, json-csv-libs]
level: practitioner
status: docs-checked
description: "Parse and generate JSON and CSV with clojure.data.json and clojure.data.csv; handle key-fn keywordization, value-fn, dates, lazy CSV reading and separators."
sources: ["https://github.com/clojure/data.json", "https://github.com/clojure/data.csv"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON and CSV

**Goal:** exchange data with the outside world; the core language has no JSON.

```clojure
;; org.clojure/data.json
(require '[clojure.data.json :as json])
(json/read-str "{\"a\":1}" :key-fn keyword)         ;=> {:a 1}
(json/write-str {:a 1 :b [1 2]})
(json/write-str m :value-fn (fn [k v] (if (inst? v) (str v) v)))
;; org.clojure/data.csv
(require '[clojure.data.csv :as csv])
(with-open [r (io/reader "in.csv")] (doall (csv/read-csv r)))        ;=> lazy seq of vectors of strings
(with-open [w (io/writer "out.csv")] (csv/write-csv w [["a" "b"] [1 2]]))
```
- Keywordize with `:key-fn keyword`; `:value-fn` is called with the key and value (on read the key is before `:key-fn`, on write after it).
- `write-str` writes `java.util.Date`, `java.time.Instant` and `java.sql.Date` as ISO strings by default (`:date-formatter` defaults to ISO_INSTANT); `read-str` does not turn them back into dates, so decode explicitly.
- `read-csv` takes a String or `java.io.Reader` and returns a lazy sequence of vectors of strings; convert types and handle any header row yourself.
- data.csv follows RFC 4180 but is more relaxed; options include `:separator` (default `,`), `:quote` (default `"`), and for `write-csv` `:newline` (`:lf` default or `:cr+lf`) and `:quote?`. Pass `:separator \tab` for TSV.
- Large files: laziness lets you process files bigger than memory, but consume the sequence inside `with-open`.

## Failure modes
- Realising the lazy CSV sequence after the reader has been closed (the README warns about this); use `doall` or process inside `with-open`.

## Self-check
Round-trip a map with nested vectors through `write-str`/`read-str` and compare after keywordizing.

## Checked
2026-11-03. Confirmed against the data.json API page and README (read-str, write-str, :key-fn, :value-fn semantics, date writing and :date-formatter) and the data.csv API page and README (read-csv input and lazy result, :separator, :quote, :newline, :quote?, RFC 4180 note, closed-reader warning). Removed: cheshire and jsonista claims, the `JSON error (unexpected character)` text, the "Stream closed" message, the header/zipmap remark and the untrusted-JSON advice (not in the pages read).
Method: documentation only; no commands were run.
