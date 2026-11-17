---
id: computing-software.web-development.svelte.bind-select-files-media
name: bind-select-files-media
category: computing-software
field: web-development
product: svelte
tags: [bind-files, bind-select, bind-audio-video, bind-details-open, bind-contenteditable]
level: practitioner
status: docs-checked
description: "Svelte bindings for file inputs (FileList via DataTransfer), select and select multiple, audio and video, img natural size, details open and contenteditable."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/12-bind.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`<input type="file" bind:files>` gives a `FileList`. To set it programmatically you need a `FileList`; since it cannot be constructed directly, use `new DataTransfer().files` (`null` or `undefined` does not work). `FileList` objects are immutable, so to delete one file build a new `DataTransfer` with the files to keep. `DataTransfer` may be missing in server-side runtimes, so leave the bound state uninitialised (`let files = $state();`).

`<select bind:value>`: the value is the selected `<option>`'s `value`, which can be any value, not just a string. `<select multiple>` binds an array. If an option's value matches its text, omit the attribute. A `selected` attribute sets the default (restored on form reset); the binding wins on initial render if not `undefined`. Since 5.57.0, a `<select>` with `defaultValue` in a form reverts to it on reset.

`<audio>`: two-way `currentTime`, `playbackRate`, `paused`, `volume`, `muted`; readonly `duration`, `buffered`, `seekable`, `seeking`, `ended`, `readyState`, `played`.

```svelte
<audio src={clip} bind:duration bind:currentTime bind:paused></audio>
```

`<video>` adds readonly `videoWidth` and `videoHeight`. `<img>` has readonly `naturalWidth` and `naturalHeight`. `<details bind:open={isOpen}>` binds `open`.

`contenteditable` elements support `innerHTML`, `innerText` and `textContent`.

## Checked

Read the full template-syntax bind page (12-bind.md). Confirmed bind:files with DataTransfer, immutable FileList and the server-side note, select value and multiple bindings, selected and defaultValue reset behaviour (the page says since 5.57.0), the audio bindings, video, img, details open and contenteditable bindings. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
