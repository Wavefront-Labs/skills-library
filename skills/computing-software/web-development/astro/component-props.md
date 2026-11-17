---
id: computing-software.web-development.astro.component-props
name: component-props
category: computing-software
field: web-development
product: astro
tags: [props, astro-props, typescript-props, default-values]
level: intro
status: docs-checked
description: "Pass props into Astro components, read them from Astro.props, type them with a Props interface, and give them default values."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/basics/astro-components.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Props are available on the `Astro.props` global in the component script. Destructure what you need:

```astro
---
// src/components/GreetingHeadline.astro
// Usage: <GreetingHeadline greeting="Howdy" name="Partner" />
const { greeting, name } = Astro.props;
---
<h2>{greeting}, {name}!</h2>
```

Pass props as attributes when using the component:

```astro
---
// src/components/GreetingCard.astro
import GreetingHeadline from './GreetingHeadline.astro';
const name = 'Astro';
---
<h1>Greeting Card</h1>
<GreetingHeadline greeting="Hi" name={name} />
```

Define a `Props` interface in the frontmatter and Astro picks it up automatically, giving type warnings and errors:

```astro
---
interface Props {
  name: string;
  greeting?: string;
}

const { greeting = "Hello", name } = Astro.props;
---
<h2>{greeting}, {name}!</h2>
```

Default values are set when destructuring from `Astro.props`:

```astro
---
const { greeting = "Hello", name = "Astronaut" } = Astro.props;
---
```

Props are attributes; slots instead render child HTML where it is written.

## Checked

2026-11-04. Confirmed against the Astro components page: Astro.props, passing props as attributes, Props interface, default values when destructuring. Nothing removed.

Method: documentation only; no commands were run.
