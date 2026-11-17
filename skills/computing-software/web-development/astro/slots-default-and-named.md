---
id: computing-software.web-development.astro.slots-default-and-named
name: slots-default-and-named
category: computing-software
field: web-development
product: astro
tags: [slot, named-slots, fragment, composition]
level: intro
status: docs-checked
description: "Inject child HTML into Astro components with the default slot, named slots, and Fragment for passing several elements without a wrapper."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/basics/astro-components.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default all child elements passed to a component render in its `<slot />`.

```astro
---
// src/components/Wrapper.astro
const { title } = Astro.props;
---
<div id="content-wrapper">
  <h1>{title}</h1>
  <slot />  <!-- children will go here -->
</div>
```

Name slots with the `name` attribute, and target them with a `slot` attribute on the child. Children without `slot` (or `slot="default"`) go to the unnamed slot.

```astro
<slot name="after-header" />
<slot />
<slot name="after-footer" />
```

```astro
<Wrapper title="Fred's Page">
  <img src="https://my.photo/fred.jpg" slot="after-header" />
  <h2>All about Fred</h2>
  <p slot="after-footer">Copyright 2022</p>
</Wrapper>
```

To pass multiple elements into one slot without a wrapping `<div>`, use `slot=""` on `<Fragment>`:

```astro
<CustomTable>
  <Fragment slot="header">
    <tr><th>Product name</th><th>Stock units</th></tr>
  </Fragment>
  <Fragment slot="body">
    <tr><td>Flip-flops</td><td>64</td></tr>
  </Fragment>
</CustomTable>
```

Named slots must be an immediate child of the component; you cannot pass them through nested elements. Named slots also work on UI framework components.

## Checked

2026-11-04. Confirmed against the Astro components page: default slot, name and slot attributes, slot="default", Fragment with slot, immediate-child rule, named slots on framework components. Nothing removed.

Method: documentation only; no commands were run.
