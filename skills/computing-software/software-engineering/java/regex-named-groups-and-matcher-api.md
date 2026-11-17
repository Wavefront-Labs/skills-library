---
id: computing-software.software-engineering.java.regex-named-groups-and-matcher-api
name: regex-named-groups-and-matcher-api
category: computing-software
field: software-engineering
product: java
tags: [java, java-strings-text, regex, named-groups, pattern, matcher]
level: practitioner
status: docs-checked
description: "Use java.util.regex properly: precompiled Pattern, named groups and their naming rules, matches vs find vs lookingAt, replaceAll with a function, quoting and flags."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/regex/Pattern.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/regex/Matcher.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regex in Java: Pattern, Matcher and named groups

## Basics
```java
private static final Pattern DATE =
    Pattern.compile("(?<year>\\d{4})-(?<month>\\d{2})-(?<day>\\d{2})");

Matcher m = DATE.matcher(input);
if (m.matches()) {            // the entire region must match
    int y = Integer.parseInt(m.group("year"));
}
while (m.find()) { ... }      // each next matching subsequence in a longer text
```
- `matches()` matches the entire region, `find()` scans for the next matching subsequence, `lookingAt()` matches starting at the beginning without needing to match the whole input.
- `Pattern` instances are immutable and safe for multiple threads; `Matcher` instances are not. Share the compiled `Pattern`, create a `Matcher` per use.
- `Pattern.quote(String)` turns a literal string into a pattern fragment (also writable as `\Q...\E`).

## Named groups
- Syntax `(?<name>X)`; back-reference with `\k<name>`; read with `m.group("name")`. Named groups are still numbered like ordinary capturing groups. `Pattern.namedGroups()` and `Matcher.namedGroups()` return a map from names to numbers (see the Javadoc for the Java version where they were added).
- Group names may contain only ASCII letters and digits, and the first character must be a letter: no underscores or hyphens.

## Replacement
```java
String out = DATE.matcher(text).replaceAll(r -> r.group("day") + "/" + r.group("month"));   // Java 9+
m.appendReplacement(sb, Matcher.quoteReplacement(userText));   // sb is a StringBuilder (Java 9+ overload)
```
- A replacement string is interpreted: `$` refers to captured groups and `\` escapes characters. This also applies to what a `replaceAll` function returns; wrap untrusted text with `Matcher.quoteReplacement`.
- `replaceAll(Function)` resets the matcher first and changes its state. The function should not modify the matcher state; a `ConcurrentModificationException` is thrown on a best-effort basis if it does.
- `results()` returns a `Stream<MatchResult>` in match order and does not reset the matcher. `Pattern.asPredicate()` and `asMatchPredicate()` give `Predicate<String>` filters (find-style and whole-string-style respectively).

## Flags and classes
- `Pattern.UNICODE_CHARACTER_CLASS` (or embedded `(?U)`) makes predefined classes Unicode-aware: without it `\d` is `[0-9]`, `\w` is `[a-zA-Z_0-9]` and `\s` is `[ \t\n\x0B\f\r]`.
- Embedded flag syntax: `(?i)`, `(?idmsuxU-idmsuxU)`, or scoped `(?i:X)`.

## Backtracking controls
The syntax table lists possessive quantifiers (`X*+`, `X++`, `X?+`, `X{n,m}+`) and independent non-capturing groups `(?>X)`; these stop the engine from backtracking into the quantified part and are the tools to reach for when a pattern is too slow.

## Verify
Run each pattern against a few matching and non-matching samples, and against a long non-matching string to confirm it returns quickly.

## Checked
2026-11-03. Confirmed against the Java SE 21 Pattern and Matcher Javadoc: matches/find/lookingAt semantics, thread-safety statement, named-group syntax and naming rules, `\k<name>`, replaceAll(Function) and results() behaviour, `$`/`\` in replacements, quote and quoteReplacement, predicates, UNICODE_CHARACTER_CLASS and `\d`/`\w`/`\s` definitions, embedded flags, possessive quantifiers and `(?>X)`.
Removed (not in the pages read): the claim that String.matches/replaceAll/split recompile on every call, the text-block advice, the exponential-backtracking (ReDoS) examples, the statement that the JDK has no regex timeout, the 30 to 50 character hostile-string verify step, and `Pattern.UNICODE_CASE` guidance.
Method: documentation only; no commands were run.
