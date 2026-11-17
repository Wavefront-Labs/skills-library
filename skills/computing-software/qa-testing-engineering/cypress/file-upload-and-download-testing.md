---
id: computing-software.qa-testing-engineering.cypress.file-upload-and-download-testing
name: file-upload-and-download-testing
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [selectfile, cypress-downloads, file-upload, file-download, cy-readfile]
level: practitioner
status: verified
description: "Test file uploads with selectFile (input and drag-drop) and downloads by checking downloadsFolder with cy.readFile, plus parsing CSV, PDF and Excel downloads via tasks."
sources:
  - https://docs.cypress.io/api/commands/selectfile
  - https://docs.cypress.io/api/commands/readfile
  - https://github.com/cypress-io/cypress-example-recipes/tree/master/examples/testing-dom__download
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File upload and download testing (Cypress)

## Uploads with selectFile (added in Cypress 9.3.0; `mimeType` in the object form since 9.4.0)
```js
cy.get('input[type=file]').selectFile('cypress/fixtures/invoice.pdf');
cy.get('input[type=file]').selectFile(['a.csv', 'b.csv'].map((f) => `cypress/fixtures/${f}`));
cy.get('[data-cy=dropzone]').selectFile('cypress/fixtures/photo.jpg', { action: 'drag-drop' });
cy.get('input[type=file]').selectFile({
  contents: Cypress.Buffer.from('id,qty\n1,2\n'), fileName: 'orders.csv', mimeType: 'text/csv',
});
cy.get('input[type=file]').selectFile('@invoiceAlias');   // alias of cy.fixture(..., null)
```
Hidden inputs: `{ force: true }`. Then assert the upload request: `cy.wait('@upload').its('request.headers').should('have.property', 'content-type')`.

## Downloads
Files go to `downloadsFolder` (default `cypress/downloads`, cleared before each run with `trashAssetsBeforeRuns`).
```js
const folder = Cypress.config('downloadsFolder');
cy.get('[data-cy=export-csv]').click();
cy.readFile(`${folder}/orders.csv`, { timeout: 15000 })     // retries until file exists
  .should('contain', 'id,qty')
  .then((csv) => expect(csv.trim().split('\n')).to.have.length(3));
```
- Binary: `cy.readFile(path, null)` yields a Buffer (a `Buffer` instance in a 16.2.0 run). `cy.readFile` is a query since 13.0.0, so it retries until the file exists or `defaultCommandTimeout`/`timeout` ends.
- Unknown file names: list the folder with a `cy.task` using `fs.readdirSync`, or use `cy-verify-downloads`.
- PDFs/Excel: parse in a task (`pdf-parse`, `xlsx`) and return text/rows.

## Alternative for downloads
Often better: intercept the download request and assert the response (`cy.intercept('GET', '/export*').as('export')`), or request the URL directly with `cy.request` and check headers (`content-disposition`) and body.

## Gotchas
- A download triggered by clicking `<a download href="/export.csv">` in headless Electron landed in `downloadsFolder` as `orders.csv` (from `content-disposition`), the only browser tried.
- Downloads opening in a new tab escape Cypress; remove `target=_blank` or request the URL.

## Verify
Run on Cypress 16.2.0: single, array, object-with-contents, alias (`cy.fixture('a.csv', null).as(...)`) and `drag-drop` uploads; the page saw `a.csv:text/csv` and `orders.csv:text/csv:11`; download read back and asserted. Upload test asserts both UI and request payload, and download test checks content, not just existence.
