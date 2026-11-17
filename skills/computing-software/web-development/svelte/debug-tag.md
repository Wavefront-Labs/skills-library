---
id: computing-software.web-development.svelte.debug-tag
name: debug-tag
category: computing-software
field: web-development
product: svelte
tags: [debug-tag, at-debug, debugger-statement, variable-logging, template-debugging]
level: intro
status: docs-checked
description: "Use {@debug} in Svelte templates to log variables when they change and pause in devtools; only variable names are accepted, not expressions."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/11-%40debug.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`{@debug ...}` is an alternative to `console.log(...)`. It logs the values of specific variables whenever they change and pauses execution if devtools are open.

```svelte
<script>
  let user = { firstname: 'Ada', lastname: 'Lovelace' };
</script>

{@debug user}

<h1>Hello {user.firstname}!</h1>
```

It accepts a comma-separated list of variable names, not arbitrary expressions.

```svelte
<!-- Compiles -->
{@debug user}
{@debug user1, user2, user3}

<!-- WON'T compile -->
{@debug user.firstname}
{@debug myArray[0]}
{@debug !isReady}
{@debug typeof user === 'object'}
```

With no arguments, `{@debug}` inserts a `debugger` statement that triggers when any state changes, rather than for specified variables.

For tracking inside script code, see `inspect-rune`.

## Checked

2026-11-08. Read the {@debug} page in full. All claims matched; no claims changed.

Method: documentation only (raw page from the sveltejs/svelte repo); no commands were run.
