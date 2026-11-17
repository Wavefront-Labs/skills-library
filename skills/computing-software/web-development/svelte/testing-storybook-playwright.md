---
id: computing-software.web-development.svelte.testing-storybook-playwright
name: testing-storybook-playwright
category: computing-software
field: web-development
product: svelte
tags: [storybook-play-function, playwright-e2e, sv-add-storybook, define-meta, web-server-config]
level: practitioner
status: docs-checked
description: "Svelte component tests in Storybook with play functions (Vitest browser mode) and end-to-end tests with Playwright, including the webServer config."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/07-misc/02-testing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Svelte is unopinionated about test frameworks (Vitest, Jasmine, Cypress, Playwright).

Storybook: tests run with Vitest's browser mode, rendering components in a real browser. Install with `npx sv add storybook` and choose the recommended configuration including testing features. Define stories with `defineMeta` from `@storybook/addon-svelte-csf` and simulate interactions in a `play` function:

```svelte
<script module>
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { expect, fn } from 'storybook/test';
  import LoginForm from './LoginForm.svelte';

  const { Story } = defineMeta({
    component: LoginForm,
    args: { onSubmit: fn() }
  });
</script>

<Story name="Empty Form" />
<Story
  name="Filled Form"
  play={async ({ args, canvas, userEvent }) => {
    await userEvent.type(canvas.getByTestId('email'), 'email@provider.com');
    await userEvent.click(canvas.getByRole('button'));
    await expect(args.onSubmit).toHaveBeenCalledTimes(1);
  }}
/>
```

Playwright: set up through the Svelte CLI or `npm init playwright`. If you ran `npm init playwright` or are not using Vite, you may need to adjust the config to tell Playwright how to start the app:

```js
const config = {
  webServer: { command: 'npm run build && npm run preview', port: 4173 },
  testDir: 'tests',
  testMatch: /(.+\.)?(test|spec)\.[jt]s/
};
export default config;
```

Tests are unaware of Svelte: drive the DOM, e.g. `await page.goto('/'); await expect(page.locator('h1')).toBeVisible();`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Svelte testing page: Storybook via npx sv add storybook running in Vitest browser mode, defineMeta and play function example, Playwright webServer config and Svelte-unaware tests. Corrected one claim: the page says the Playwright config may need adjusting if you ran npm init playwright or are not using Vite (the draft said only not using Vite).
