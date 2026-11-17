---
id: computing-software.web-development.frontend-development.file-inputs-drag-drop-and-previews
name: file-inputs-drag-drop-and-previews
category: computing-software
field: web-development
product: frontend-development
tags: [html-forms, file-input, file-upload-client, drag-and-drop, accept-attribute, url-createobjecturl, filereader, image-preview]
level: practitioner
status: docs-checked
description: "Building accessible file pickers: accept/multiple/capture, drag-and-drop zones, client-side previews and size checks before upload."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/file
  - https://developer.mozilla.org/en-US/docs/Web/API/File_API/Using_files_from_web_applications
  - https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API/File_drag_and_drop
  - https://www.w3.org/TR/FileAPI/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File inputs, drag-and-drop and previews

**Goal:** users can choose files by button, keyboard or drop, see previews, and get immediate feedback on wrong type/size.

## 1. The input
```html
<label for="photos">Photos (JPEG/PNG, max 10 MB each)</label>
<input id="photos" name="photos" type="file" accept="image/jpeg,image/png" multiple>
```
- `accept` takes unique file type specifiers (extensions, MIME types, `image/*`); treat it as a hint and re-check type and size in JS **and** on the server (see file-upload security).
- `capture="environment"` (or `"user"`) asks for the rear (or front) camera when `accept` indicates image or video; omit it if users should also pick existing files.

## 2. Validate client-side
```js
input.addEventListener('change', () => {
  for (const f of input.files) {
    if (!['image/jpeg','image/png'].includes(f.type)) return fail(`${f.name}: not a JPEG/PNG`);
    if (f.size > 10 * 1024 * 1024) return fail(`${f.name}: over 10 MB`);
  }
});
```
`file.type` is an empty string when the type cannot be determined (File API); treat it as a hint.

## 3. Previews without memory leaks
```js
const url = URL.createObjectURL(file);
img.src = url;
img.onload = () => URL.revokeObjectURL(url);
```
Each `createObjectURL()` call makes a new URL that must be released with `revokeObjectURL()`. For file types the browser cannot render, show a filename tile instead of a preview.

## 4. Drop zone
```js
zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('over'); });
zone.addEventListener('dragleave', () => zone.classList.remove('over'));
zone.addEventListener('drop', e => {
  e.preventDefault(); zone.classList.remove('over');
  const dt = new DataTransfer();
  for (const f of e.dataTransfer.files) dt.items.add(f);
  input.files = dt.files;               // keep the real input as the source of truth
  input.dispatchEvent(new Event('change', { bubbles: true }));
});
```
The element must cancel `dragover` for `drop` to fire. Also cancel `drop` (and `dragover`) on `window` for file drags, otherwise the browser may open or download a file dropped outside the zone. The drop zone is an enhancement; the button must stay.

## 5. Removing a file from a multiple selection
`FileList` is read-only: rebuild with `DataTransfer` minus the removed item and reassign `input.files`.

## Verify
- [ ] Keyboard-only: Tab to the control, Enter/Space opens picker.
- [ ] Dropping a wrong type shows an error and does not navigate.
- [ ] Memory tab shows no growing blob URLs after adding/removing many images.

## Checked

Checked 2026-10-26 against mdn/content (main) input type=file, Using files from web applications, File drag and drop, DataTransfer and HTMLInputElement.files, the W3C File API draft and mdn/browser-compat-data.

- Confirmed: `accept` specifier forms; `capture` values `user` and `environment`; object URLs must be released with `revokeObjectURL()`; a drop needs `dragover` cancelled, and file drops should be cancelled on `window` to stop the browser opening them; `new DataTransfer()` (Chrome 59, Firefox 62, Safari 14.1) and `items.add` are available to build a file list.
- Changed: `file.type` is the empty string when the type cannot be determined (it was said to come from the extension).
- Removed: claims that users can still choose "All files", the visually-hidden input restyling advice, "object URLs are faster" and the HEIC preview remark, none of which the pages checked state.

Method: documentation only; no commands were run.
