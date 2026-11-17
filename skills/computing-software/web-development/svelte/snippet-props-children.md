---
id: computing-software.web-development.svelte.snippet-props-children
name: snippet-props-children
category: computing-software
field: web-development
product: svelte
tags: [snippet-props, children-snippet, implicit-snippet-props, optional-snippet, slots-replacement]
level: practitioner
status: docs-checked
description: "Pass snippets to Svelte components: explicit props, implicit props from snippets declared inside the tag, the implicit children snippet, and optional snippets."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/06-snippet.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Snippets are values, so they can be passed as props (like content rather than data; similar to web component slots):

```svelte
<Table data={fruits} {header} {row} />
```

Implicit props: snippets declared directly inside a component's tags become props on it:

```svelte
<Table data={fruits}>
  {#snippet header()}<th>fruit</th>{/snippet}
  {#snippet row(d)}<td>{d.name}</td>{/snippet}
</Table>
```

The receiver reads them with `$props` and uses `{@render header()}` and `{@render row(d)}`.

Implicit children: content inside the tags that is not a snippet declaration becomes the `children` snippet.

```svelte
<!-- Button.svelte -->
<script>
  let { children } = $props();
</script>
<button>{@render children()}</button>
```

`<Button>click me</Button>` yields `<button>click me</button>`. You cannot have a prop named `children` if you also pass content inside the tags, so avoid that name.

Optional snippets: use optional chaining, or an `{#if}` for fallback content.

```svelte
{@render children?.()}
```

```svelte
{#if children}{@render children()}{:else}fallback content{/if}
```

## Checked

2026-11-08. Read the {#snippet} page in full. All claims matched; no claims changed.

Method: documentation only (raw page from the sveltejs/svelte repo); no commands were run.
