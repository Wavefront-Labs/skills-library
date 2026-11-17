---
id: computing-software.web-development.angular.decorator-queries
name: decorator-queries
category: computing-software
field: web-development
product: angular
tags: [angular, queries, viewchild-decorator, contentchild-decorator, querylist, static-query]
level: practitioner
status: docs-checked
description: "Decorator-based queries @ViewChild, @ViewChildren, @ContentChild, @ContentChildren: availability by lifecycle hook, static option and QueryList."
sources:
  - https://angular.dev/guide/components/queries
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The signal-based query functions are recommended for new projects, but the decorator APIs remain fully supported and behave the same except as noted here.

```ts
export class CustomCard implements AfterViewInit {
  @ViewChild(CustomCardHeader) header: CustomCardHeader;
  @ViewChildren(CustomCardAction) actions: QueryList<CustomCardAction>;

  ngAfterViewInit() {
    console.log(this.header.text);
    this.actions.forEach((action) => console.log(action.text));
  }
}

export class CustomExpando implements AfterContentInit {
  @ContentChild(CustomToggle) toggle: CustomToggle;
  ngAfterContentInit() { console.log(this.toggle.text); }
}
```

When results are available:
- View query results (`@ViewChild`, `@ViewChildren`) become available in `ngAfterViewInit`; before that the value is `undefined`.
- Content query results (`@ContentChild`, `@ContentChildren`) become available in `ngAfterContentInit`; before that the value is `undefined`.
- Angular keeps results up to date as application state changes.

Static queries: `@ViewChild` and `@ContentChild` accept `static`.

```ts
@ViewChild(CustomCardHeader, {static: true}) header: CustomCardHeader;
ngOnInit() { console.log(this.header.text); }
```

`static: true` is a guarantee to Angular that the target is always present and not conditionally rendered. The result is then available earlier, in `ngOnInit`, and does not update after initialization. The option is not available for `@ViewChildren` and `@ContentChildren`.

`QueryList`: `@ViewChildren` and `@ContentChildren` yield a `QueryList` with array-like helpers such as `map`, `reduce` and `forEach`. `toArray()` returns the current results, and you can subscribe to its `changes` property to react whenever results change.

All decorators accept the same options object as second parameter as the signal versions (`read`, `descendants`, etc.). See `computing-software.web-development.angular.signal-queries`.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/components/queries (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
