---
id: computing-software.web-development.angular.custom-pipes
name: custom-pipes
category: computing-software
field: web-development
product: angular
tags: [angular, pipes, custom-pipe, pipetransform, impure-pipe, formatdate, services]
level: practitioner
status: docs-checked
description: "Write custom Angular pipes with @Pipe and PipeTransform, naming rules, parameters, impure pipes, and sharing pipe logic with services via plain functions."
sources:
  - https://angular.dev/guide/templates/pipes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A custom pipe is a class with `@Pipe` carrying a `name`, and a `transform` method; it should implement `PipeTransform`.

```ts
import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'kebabCase',
})
export class KebabCasePipe implements PipeTransform {
  transform(value: string): string {
    return value.toLowerCase().replace(/ /g, '-');
  }
}
```

Naming: `name` in camelCase (no hyphens); class name is the PascalCase name with `Pipe` appended. The first `transform` parameter is the incoming value; extra parameters become pipe arguments: `transform(value: string, format: string)` used as `{{ x | myCustomTransformation: 'uppercase' }}`.

Impure pipes: to detect changes inside arrays or objects, set `pure: false`. Avoid impure pipes unless absolutely necessary because of the performance penalty. Convention is to include `Impure` in the name and class name.

```ts
@Pipe({
  name: 'joinNamesImpure',
  pure: false,
})
export class JoinNamesImpurePipe implements PipeTransform {
  transform(names: string[]): string {
    return names.join();
  }
}
```

Logic outside templates: do not inject pipe classes into services; pipes are not designed as injectable services. Extract the transformation into a standalone function, have `transform()` call it, and import the function elsewhere:

```ts
export function toKebabCase(value: string): string {
  return value.toLowerCase().replace(/ /g, '-');
}
```

Built-in locale-aware pipes have standalone functions exported from `@angular/common`: `DatePipe` has `formatDate`, `CurrencyPipe` has `formatCurrency`, `DecimalPipe` has `formatNumber`, `PercentPipe` has `formatPercent`.

```ts
private locale = inject(LOCALE_ID);
format(value: number) {
  return formatNumber(value, this.locale, '1.2-2');
}
```

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/templates/pipes (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
