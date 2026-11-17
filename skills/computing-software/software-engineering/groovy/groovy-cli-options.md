---
id: computing-software.software-engineering.groovy.groovy-cli-options
name: groovy-cli-options
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, groovy-cli-options, groovy-tools]
level: practitioner
status: docs-checked
description: "Use the groovy runner (-e, -n, -p, -cp, -D), groovyc compiler and groovydoc generator."
sources:
  - https://docs.groovy-lang.org/latest/html/documentation/tools-groovy.html
  - https://groovy-lang.org/groovysh.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/tools-groovy.adoc
  - https://github.com/apache/groovy/blob/master/src/spec/doc/tools-groovyc.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# groovy, groovyc and groovydoc commands
- Run: `groovy script.groovy args`; inline: `groovy -e "println 42"`; `-n` processes files line by line with an implicit `line` variable, `-p` also prints the result, `-i <ext>` modifies files in place (backup if an extension is given).
- Classpath: `groovy -cp <path> script.groovy` (must be the first argument) or `CLASSPATH`; system properties `-Dname=value`; JVM options via `JAVA_OPTS`.
- Compile: `groovyc -d <dir> A.groovy` (`-d` sets where class files go); joint compile with `groovyc -j A.groovy B.java`.
- Version: `groovy -v` or `groovy --version`.

## Gotchas
- See the groovy and groovyc pages for the full option tables of your release.

## Checked

2026-11-02. Confirmed against the groovy command and groovyc pages (option tables). Removed: `groovydoc`, SDKMAN, and the script class-name claims.

Method: documentation only; no commands were run.

## Self-check
`groovy --version` and `groovy -e "println 1+1"`.
