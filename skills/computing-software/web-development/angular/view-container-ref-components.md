---
id: computing-software.web-development.angular.view-container-ref-components
name: view-container-ref-components
category: computing-software
field: web-development
product: angular
tags: [angular, viewcontainerref, createcomponent, inputbinding, outputbinding, twowaybinding, dynamic-components]
level: advanced
status: docs-checked
description: "Create components from TypeScript with ViewContainerRef.createComponent or createComponent, using inputBinding, outputBinding, twoWayBinding, directives and onError."
sources:
  - https://angular.dev/guide/components/programmatic-rendering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A view container is a node in the component tree that can hold content. Any component or directive can `inject(ViewContainerRef)`. `createComponent` on it renders a component and appends it to the DOM as the next sibling of the injecting component or directive.

```ts
private viewContainer = inject(ViewContainerRef);
loadContent() {
  this.viewContainer.createComponent(LeafContent);
}
```

Bindings at creation: both `ViewContainerRef.createComponent` and the standalone `createComponent` accept a `bindings` array (`inputBinding()`, `outputBinding()`, `twoWayBinding()`) and a `directives` array for host directives.

```ts
const compRef = this.vcr.createComponent(AppWarning, {
  bindings: [
    inputBinding('canClose', this.canClose),
    twoWayBinding('isExpanded', this.isExpanded),
    outputBinding<boolean>('close', (confirmed) => console.log(confirmed)),
  ],
  directives: [
    FocusTrap,
    {type: ThemeDirective, bindings: [inputBinding('theme', () => 'warning')]},
  ],
});
```

`ViewContainerRef.createComponent` inserts the host view and element into the container at its location. The standalone `createComponent` does not attach to any existing view or DOM location; it returns a `ComponentRef` and you place the host element yourself.

Popup outside the view hierarchy: pass `environmentInjector` and a `hostElement` (Angular then does not create a new element matching the selector), attach the view, and append the element.

```ts
const host = document.createElement('popup-host');
const ref = createComponent(Popup, {
  environmentInjector: this.injector,
  hostElement: host,
  bindings: [inputBinding('message', () => message)],
});
this.appRef.attachView(ref.hostView);   // joins change detection
document.body.appendChild(host);
```

On close, the guide removes the host from `document.body`, calls `appRef.detachView(ref.hostView)` and `ref.destroy()`.

Errors: an `onError: (err, details) => ...` option (developer preview, with `ErrorDetails`) handles errors during rendering or change detection, the programmatic equivalent of an `@error` block. It does not catch errors during instantiation, such as in the constructor; those throw synchronously from the API call.

## Checked

Method: 2026-11-08 compared against the Angular programmatic rendering guide source markdown (adev guide components/programmatic-rendering). ViewContainerRef placement, bindings, directives, hostElement popup flow and onError notes match the page; no changes to the technical content.
