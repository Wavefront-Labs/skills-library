---
id: computing-software.web-development.astro.template-directives-class-list-set-html
name: template-directives-class-list-set-html
category: computing-software
field: web-development
product: astro
tags: [template-directives, class-list, set-html, set-text, xss]
level: intro
status: docs-checked
description: "Use class:list to build class strings and set:html or set:text to inject content, including the unescaped-HTML XSS warning."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/reference/directives-reference.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Template directives are `X:Y` attributes (e.g. `client:load`) that must be visible to the compiler (`<X {...attr}>` hiding a directive does not work) and never appear in output HTML.

`class:list` takes an array: strings added, objects add truthy keys, arrays flattened, `false`/`null`/`undefined` skipped (powered by clsx).

```astro
<span class:list={[ 'hello goodbye', { world: true }, [ 'friend' ] ]} />
<!-- Becomes -->
<span class="hello goodbye world friend"></span>
```

`set:html` injects an HTML string like `innerHTML`. The value is not escaped; trust it or escape it, or you risk Cross Site Scripting (XSS).

```astro
---
const rawHTMLString = "Hello <strong>World</strong>"
---
<h1>{rawHTMLString}</h1>
  <!-- Output: <h1>Hello &lt;strong&gt;World&lt;/strong&gt;</h1> -->
<h1 set:html={rawHTMLString} />
  <!-- Output: <h1>Hello <strong>World</strong></h1> -->
```

Use it on `<Fragment>` to avoid a wrapper element, e.g. `<Fragment set:html={cmsContent}>`. It also accepts a `Promise<string>` or `Promise<Response>` (e.g. `fetch(...)`), and works on any tag, such as JSON-LD:

```astro
<script type="application/ld+json" set:html={JSON.stringify({
  "@context": "https://schema.org/",
  "@type": "Person",
  name: "Houston",
})}/>
```

`set:text` injects an automatically escaped string like `innerText`; it equals `{someText}` so is rarely used.

## Checked

2026-11-04. Confirmed against the Astro template directives reference: directive rules, class:list value kinds and clsx, set:html (string, Promise, Response, Fragment, JSON-LD) and the XSS warning, set:text. Nothing removed.

Method: documentation only; no commands were run.
