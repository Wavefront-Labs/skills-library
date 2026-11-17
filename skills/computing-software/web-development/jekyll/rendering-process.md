---
id: computing-software.web-development.jekyll.rendering-process
name: rendering-process
category: computing-software
field: web-development
product: jekyll
tags: [build-phases, rendering-stages, converters, liquid-rendering, layout-nesting]
level: advanced
status: docs-checked
description: "Understand the Jekyll build session phases and the three rendering stages (Liquid, converters, layouts) to explain why Markdown or Sass is or is not processed."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/rendering-process.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A build session runs these phases in order: set up plugins, read source files, run generators, render templates, write files to disk.

Rendering has three optional stages; each file passes through the ones its content, front matter and extension select, and each stage's output is the next one's input.

1. Interpreting Liquid. Liquid expressions in the file are evaluated. The interpretation is shallow: Liquid appearing in the resulting output is not interpreted again, and Liquid in the front matter is left untouched.
2. Converters. The converter mapped to the file's extension converts the string: Markdown to HTML, Sass/SCSS to CSS, CoffeeScript to JavaScript. Since this depends on the extension, Markdown or Sass inside a `.html` file stays untouched.
3. Layouts. The source file is now considered rendered and not revisited. Whether the output goes into a layout depends on the extension and front matter. Sass and CoffeeScript output is never placed in a layout; regular text goes in if a layout was assigned. Layouts nest like Russian dolls: the converted output is the core and each layout in the chain is rendered around it in turn.

Use this order when debugging: Liquid runs before Markdown conversion, and layouts are applied last.

## Checked

2026-11-04. Confirmed against the Jekyll rendering process doc: the five build phases, the three optional stages, shallow Liquid and untouched front matter, extension-based converters, `.html` files left alone, Sass and CoffeeScript never placed in layouts, and layout nesting. The final debugging sentence follows directly from the stage order.

Method: documentation only; no commands were run.
