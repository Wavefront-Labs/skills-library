---
id: computing-software.web-development.astro.client-scripts-processing
name: client-scripts-processing
category: computing-software
field: web-development
product: astro
tags: [script-tag, is-inline, bundling, external-scripts]
level: practitioner
status: docs-checked
description: "Know how Astro processes plain script tags (TypeScript, bundling, dedup, inlining), when it does not, and how to load local or external scripts."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/client-side-scripts.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Add interactivity with `<script>` tags in the component template; no UI framework needed.

```astro title="src/components/ConfettiButton.astro"
<button data-confetti-button>Celebrate!</button>

<script>
  import confetti from 'canvas-confetti';

  const buttons = document.querySelectorAll('[data-confetti-button]');

  buttons.forEach((button) => {
    button.addEventListener('click', () => confetti());
  });
</script>
```

A `<script>` with no attributes (other than `src`) is processed: TypeScript by default; local and npm imports bundled; made `type="module"`; deduplicated when the component is used several times; inlined if small.

Any other attribute means it is not processed. Opt out deliberately with `is:inline`; the code is rendered as written, with no TypeScript or import resolution, and duplicated per component instance:

```astro
<script is:inline>
  // Will be rendered into the HTML exactly as written!
</script>
```

Local scripts under `src/` via `src`, which Astro processes:

```astro
<script src="../scripts/local.js"></script>
<script src="./script-with-types.ts"></script>
```

Scripts in `public/` or on a CDN need `is:inline`, skipping bundling and optimization:

```astro
<script is:inline src="/my-script.js"></script>
<script is:inline src="https://my-analytics.com/script.js"></script>
```

## Checked

2026-11-04. Confirmed against the Astro scripts and event handling guide: processing rules, unprocessed scripts, is:inline, local src scripts, public and CDN scripts. Nothing removed.

Method: documentation only; no commands were run.
