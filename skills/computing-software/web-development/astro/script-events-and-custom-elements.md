---
id: computing-software.web-development.astro.script-events-and-custom-elements
name: script-events-and-custom-elements
category: computing-software
field: web-development
product: astro
tags: [custom-elements, web-components, add-event-listener, data-attributes]
level: practitioner
status: docs-checked
description: "Handle events with addEventListener, wrap behavior in custom elements, and pass frontmatter values to client scripts through data attributes."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/client-side-scripts.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Astro uses no custom event syntax; use `addEventListener`. A bundled script runs once per page even with many component instances, so select all matching elements:

```astro
<button class="alert">Click me!</button>

<script>
  const buttons = document.querySelectorAll('button.alert');

  buttons.forEach((button) => {
    button.addEventListener('click', () => {
      alert('Button was clicked!');
    });
  });
</script>
```

Custom elements scope behavior to one instance: `this.querySelector()` searches only inside it, and `connectedCallback()` runs each time the element is found, even though the script runs once.

```astro
<astro-heart>
  <button aria-label="Heart">💜</button> × <span>0</span>
</astro-heart>

<script>
  class AstroHeart extends HTMLElement {
    connectedCallback() {
      let count = 0;
      const heartButton = this.querySelector("button");
      const countSpan = this.querySelector("span");
      if (heartButton && countSpan) {
        heartButton.addEventListener("click", () => {
          count++;
          countSpan.textContent = count.toString();
        });
      }
    }
  }
  customElements.define("astro-heart", AstroHeart);
</script>
```

Frontmatter runs on the server and is unavailable in the browser. Pass values with `data-*` attributes and read `this.dataset`:

```astro
---
const { message = 'Welcome, world!' } = Astro.props;
---
<astro-greet data-message={message}>
  <button>Say hi!</button>
</astro-greet>
```

Elements rendered by a UI framework may not exist yet when a script runs; a custom element is recommended there.

## Checked

2026-11-04. Confirmed against the Astro scripts and event handling guide: addEventListener, once-per-page bundling, custom element connectedCallback, data-* attributes, UI framework note. Nothing removed.

Method: documentation only; no commands were run.
