---
id: computing-software.software-engineering.groovy.clibuilder-usage
name: clibuilder-usage
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, clibuilder-usage, groovy-cli-builder]
level: practitioner
status: docs-checked
description: "Parse command-line options with CliBuilder: dynamic API, annotated interface or class specs, usage output and the picocli and commons-cli variants."
sources:
  - https://groovy-lang.org/dsls.html
  - https://github.com/apache/groovy/blob/master/subprojects/groovy-cli-picocli/src/main/groovy/groovy/cli/picocli/CliBuilder.groovy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parsing command-line options with CliBuilder
```groovy
def cli = new CliBuilder(name:'ls')
cli.a('display all files')
cli.l('use a long listing format')
cli.t('sort by modification time')
def options = cli.parse(args)
assert options // would be null (false) on failure
assert options.arguments() == ['*.groovy']
assert options.a && options.l && options.t
```
- The example is the picocli `CliBuilder` Javadoc, run with the arguments `-alt *.groovy`.
- Set the `usage` property in the constructor to control the synopsis; `cli.usage()` prints the usage message.
- Annotation style: an interface whose methods carry `@Option(shortName=..., description=...)`, with `@Unparsed List remaining()` for leftover arguments, passed to `cli.parseFromSpec(OptionInterface, args)`. Both annotations come from `groovy.cli`.
- Annotation style with a class: annotate properties the same way and call `cli.parseFromInstance(options, args)`.
- Since Groovy 2.5 the old `groovy.util.CliBuilder` is deprecated: choose the `groovy.cli.picocli` or `groovy.cli.commons` version. The `groovy.util` version was removed in Groovy 3.0.

## Gotchas
- `parse` returns null on a bad command line after printing the usage message.

## Checked

2026-11-03. Confirmed against the picocli CliBuilder source Javadoc (dynamic and annotation styles, `parse` returning null, `usage()`) and the DSLs chapter (CliBuilder section, deprecation note). Removed: the claim about `opts.n` returning false, the plural-accessor claim, the module artifact names and the self-check.

Method: documentation only; no commands were run.
