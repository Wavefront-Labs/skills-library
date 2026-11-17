---
id: computing-software.software-engineering.clojure.regex-re-find-re-matches-re-seq-groups
name: regex-re-find-re-matches-re-seq-groups
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, regex, re-find, re-matches, re-seq, re-pattern, re-matcher, capture-groups, named-groups, regex-re-find-groups]
level: practitioner
status: docs-checked
description: "Use #'' patterns with re-find, re-matches, re-seq and capture groups, named groups via Matcher, flags like (?i), and know the full-match vs search distinction."
sources: ["https://clojure.org/guides/learn/syntax", "https://clojure.github.io/clojure/clojure.core-api.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regular expressions

**Goal:** match and extract text with java.util.regex through Clojure's helpers.

```clojure
(re-find #"\d+" "ab12cd34")             ;=> "12"           (first match anywhere)
(re-find #"(\w+)@(\w+)" "me@host")      ;=> ["me@host" "me" "host"]   (groups -> vector)
(re-matches #"\d+" "123")               ;=> "123"          (whole string must match)
(re-seq #"\d+" "a1b22")                 ;=> ("1" "22")
(re-pattern (str "^" (java.util.regex.Pattern/quote user-input)))
(re-find #"(?i)hello" "HeLLo")          ; flags inline: (?i) case-insens, (?s) dotall, (?m) multiline
(let [m (re-matcher #"(?<year>\d{4})" "in 2026")]
  (when (.find m) (.group m "year")))   ;=> "2026"   named groups need Matcher
```
- `re-find` searches; `re-matches` anchors to the whole string; `re-seq` returns all matches (vectors if groups).
- `#"..."` literals: backslashes are not escaped like in strings; write `#"\d"` not `#"\\d"`. In a string passed to
  `re-pattern` you need `"\\d"`.
- A literal pattern is compiled once at read time; patterns equal by identity, not value (`(= #"a" #"a")` is false).
- Always quote untrusted text: `Pattern/quote`.
- Patterns are java.util.regex.Pattern objects: check the JDK Pattern documentation for flags and backtracking cost on untrusted input.
- `str/replace` and `str/split` also take regexes.

## Failure modes
- Expecting `re-find` to return a string when groups exist (it returns a vector).
- Using `re-matches` when you meant "contains".

## Self-check
`(re-seq #"(\d)(\w)" "1a2b")` returns pairs of vectors; predict before running.

## Checked
2026-11-02. Confirmed: clojure.org/guides/learn/syntax (regex literals compile to java.util.regex.Pattern) and the clojure.core API: re-find, re-matches, re-seq, re-pattern, re-matcher, re-groups semantics (vector when groups exist). Replaced: the ReDoS bullet with a pointer to the JDK Pattern docs. Pattern syntax itself is JDK behaviour (java.util.regex.Pattern page not read).
Method: documentation only; no commands were run.
