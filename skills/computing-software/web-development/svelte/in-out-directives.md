---
id: computing-software.web-development.svelte.in-out-directives
name: in-out-directives
category: computing-software
field: web-development
product: svelte
tags: [in-directive, out-directive, unidirectional-transition, fly-fade, aborted-outro]
level: intro
status: docs-checked
description: "Svelte in: and out: are non-bidirectional transitions: in keeps playing alongside out; aborted outs restart."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/15-in-and-out.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`in:` and `out:` are identical to `transition:` except the resulting transitions are not bidirectional. If a block is outroed while the `in` transition is in progress, the `in` keeps playing alongside the `out` rather than reversing. If an out transition is aborted, transitions restart from scratch.

```svelte
<script>
  import { fade, fly } from 'svelte/transition';
  let visible = $state(false);
</script>

<label>
  <input type="checkbox" bind:checked={visible}>
  visible
</label>

{#if visible}
  <div in:fly={{ y: 200 }} out:fade>flies in, fades out</div>
{/if}
```

Different functions can be used for entering and leaving, as above. Otherwise they are identical to `transition:` (see `transition-directive`).

## Checked

2026-11-08. Read in full the cited Svelte docs page (documentation/docs/03-template-syntax/15-in-and-out.md): behaviour text and example. Removed the specific claim about parameters, local vs global and events, which that page does not spell out.

Method: documentation only; no commands were run.
