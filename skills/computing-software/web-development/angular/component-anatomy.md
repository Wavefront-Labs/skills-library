---
id: computing-software.web-development.angular.component-anatomy
name: component-anatomy
category: computing-software
field: web-development
product: angular
tags: [angular, component, decorator, standalone, imports, template, selector]
level: intro
status: docs-checked
description: "What every Angular component needs, the @Component metadata, separate template and style files, and importing components into other components."
sources:
  - https://angular.dev/guide/components/anatomy-of-components
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every Angular component has a TypeScript class (behavior), an HTML template (what renders into the DOM) and a CSS selector (how it is used in HTML). Angular-specific information goes in the `@Component` decorator; the object passed to it is the component's metadata.

```ts
@Component({
  selector: 'profile-photo',
  template: `<img src="profile-photo.jpg" alt="Your profile photo" />`,
  styles: `
    img {
      border-radius: 50%;
    }
  `,
})
export class ProfilePhoto {}
```

Template and styles can live in separate files instead:

```ts
@Component({
  selector: 'profile-photo',
  templateUrl: 'profile-photo.html',
  styleUrl: 'profile-photo.css',
})
export class ProfilePhoto {}
```

Both `templateUrl` and `styleUrl` are relative to the directory the component resides in. You can pick one approach for the whole project or per component.

Using a component:
- Add the component, directive or pipe to the `imports` array of the component that uses it: `imports: [ProfilePhoto]`.
- Create a matching HTML element in that component's template: `template: '<profile-photo />'`.
- Components are standalone by default. Older components may specify `standalone: false`; for those you import the `NgModule` that declares them. In Angular versions before 19.0.0, `standalone` defaults to `false`.

Terms: the DOM element matching the selector is the component's host element, the template contents render inside it, and the rendered DOM is the component's view. An application is a tree of components, which matters for dependency injection and child queries.

Component styles only affect elements in that component's own template by default (see `computing-software.web-development.angular.component-styling`).

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/components/anatomy-of-components (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
The live page fetch returned only a stub, so the claims were confirmed against the repository Markdown instead.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
