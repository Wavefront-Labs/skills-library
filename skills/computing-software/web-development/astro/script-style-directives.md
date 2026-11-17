---
id: computing-software.web-development.astro.script-style-directives
name: script-style-directives
category: computing-software
field: web-development
product: astro
tags: [is-global, is-inline, define-vars, is-raw, scoped-styles]
level: practitioner
status: docs-checked
description: "Use is:global, is:inline, define:vars and is:raw on style and script tags, and know what each disables: scoping, bundling, deduplication."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/reference/directives-reference.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`is:global`: Astro scopes `<style>` rules to the component by default; this makes the tag's rules global (like wrapping selectors in `:global()`). You can mix `<style>` and `<style is:global>` in one component.

```astro
<style is:global>
  body a { color: red; }
</style>
```

`is:inline`: leaves the tag as-is in output, unprocessed and unbundled. Consequences: `defer` has no effect, not deduplicated, imports are not resolved relative to the `.astro` file, rendered where authored, styles are global. It is implied by any attribute other than `src` (exception: `define:vars` on `<style>`).

```astro
<style is:inline>
  @import '/assets/some-public-styles.css';
  span { color: green; }
</style>
<script is:inline>
  console.log('I am inlined right here in the final output HTML.');
</script>
```

`define:vars` passes JSON-serializable frontmatter values (including props) into `<style>` or `<script>`:

```astro
---
const foregroundColor = "rgb(221 243 228)";
const backgroundColor = "rgb(24 121 78)";
const message = "Astro is awesome!";
---
<style define:vars={{ textColor: foregroundColor, backgroundColor }}>
  h1 {
    background-color: var(--backgroundColor);
    color: var(--textColor);
  }
</style>
<script define:vars={{ message }}>
  alert(message);
</script>
```

On a script, `define:vars` implies `is:inline` (needed to re-run per value set); the page suggests passing variables to scripts manually instead.

`is:raw` treats an element's children as text, ignoring Astro template syntax: `<Katex is:raw>Some conflicting {syntax} here</Katex>`.

## Checked

2026-11-04. Confirmed against the Astro template directives reference: is:global, is:inline consequences and implied-by rule, define:vars, is:raw. Reworded the data-attributes advice to what the page says.

Method: documentation only; no commands were run.
