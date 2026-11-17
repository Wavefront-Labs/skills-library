---
id: computing-software.web-development.astro.component-script-and-template
name: component-script-and-template
category: computing-software
field: web-development
product: astro
tags: [astro-component, component-script, code-fence, template, class-list]
level: intro
status: docs-checked
description: "Structure an Astro component: the code fence for the component script, the HTML template below it, and what runs at build time versus in the browser."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/basics/astro-components.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Astro components (`.astro`) are HTML-only templating components with no client-side runtime. They render to HTML at build time or on demand; JavaScript in the component script is stripped from the page sent to browsers.

```astro title="src/components/EmptyComponent.astro"
---
// Component Script (JavaScript)
---
<!-- Component Template (HTML + JS Expressions) -->
```

The code fence (`---`) holds the component script. Use it to import components or data, fetch content from an API or database, and create variables for the template. Expensive or sensitive code stays fenced in:

```astro
---
import SomeAstroComponent from '../components/SomeAstroComponent.astro';
import someData from '../data/pokemon.json';

// Access passed-in component props, like `<X title="Hello, World" />`
const { title } = Astro.props;

// Fetch external data, even from a private API or database
const data = await fetch('SOME_SECRET_API_URL/users').then(r => r.json());
---
```

The template supports HTML, JavaScript expressions, imported components, `<style>`, `<script>` and directives:

```astro
<ul>
  {myFavoritePokemon.map((data) => <li>{data.name}</li>)}
</ul>
<p class:list={["add", "dynamic", { classNames: true }]} />
```

The component script is TypeScript. For client interactivity, add `<script>` tags or framework components with a `client:` directive.

## Checked

2026-11-04. Confirmed against the Astro components page: HTML-only components, code fence, what the component script may do, template contents, TypeScript note, script tags and client: directives. Nothing removed.

Method: documentation only; no commands were run.
