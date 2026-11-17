---
id: computing-software.web-development.angular.custom-event-plugins
name: custom-event-plugins
category: computing-software
field: web-development
product: angular
tags: [angular, events, event-manager-plugin, event-manager-plugins, debounce, platform-browser]
level: advanced
status: docs-checked
description: "Extend Angular event handling by subclassing EventManagerPlugin and registering it with EVENT_MANAGER_PLUGINS, for example a debounce event syntax."
sources:
  - https://angular.dev/guide/templates/event-listeners
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Angular's event system is extensible through custom event plugins registered with the `EVENT_MANAGER_PLUGINS` injection token.

Implement by extending `EventManagerPlugin` from `@angular/platform-browser`, declaring which event names it supports and how to add the listener. `addEventListener` returns a cleanup function.

```ts
@Injectable()
export class DebounceEventPlugin extends EventManagerPlugin {
  constructor() {
    super(document);
  }

  override supports(eventName: string) {
    return /debounce/.test(eventName);
  }

  override addEventListener(element: HTMLElement, eventName: string, handler: Function) {
    // "click.debounce.500" -> event: "click", delay: 500
    const [event, , delay = '300'] = eventName.split('.');
    let timeoutId: ReturnType<typeof setTimeout>;
    const listener = (e: Event) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => handler(e), Number(delay));
    };
    element.addEventListener(event, listener);
    return () => {
      clearTimeout(timeoutId);
      element.removeEventListener(event, listener);
    };
  }
}
```

Register it in the application providers with `multi: true`:

```ts
bootstrapApplication(App, {
  providers: [
    {
      provide: EVENT_MANAGER_PLUGINS,
      useClass: DebounceEventPlugin,
      multi: true,
    },
  ],
});
```

Then use the custom syntax in templates and in the `host` property:

```html
<input type="text" (input.debounce.500)="onSearch($event.target.value)" placeholder="Search..." />
```
```ts
host: {
  '(click.debounce.500)': 'handleDebouncedClick()',
},
```

The standard listener features are covered in `computing-software.web-development.angular.template-event-listeners`.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/templates/event-listeners (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
