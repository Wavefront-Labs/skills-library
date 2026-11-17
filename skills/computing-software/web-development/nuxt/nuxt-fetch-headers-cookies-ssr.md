---
id: computing-software.web-development.nuxt.nuxt-fetch-headers-cookies-ssr
name: nuxt-fetch-headers-cookies-ssr
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, usefetch, cookies, headers, userequestfetch]
level: advanced
status: docs-checked
description: "Forward client headers and cookies during SSR with useFetch, useRequestFetch or useRequestHeaders, and pass Set-Cookie back to the client."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/10.data-fetching.md
  - https://github.com/nuxt/nuxt/blob/main/docs/4.api/2.composables/use-request-fetch.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When `$fetch` is called in the browser, user headers like `cookie` are sent directly to the API. During server-side rendering, due to security considerations, `$fetch` does not include the user's browser cookies, nor pass on cookies from the fetch response.

`useFetch` with a relative URL on the server uses `useRequestFetch` to proxy headers and cookies, except headers not meant to be forwarded. This is only needed by hand when you are not using `useFetch`:

```ts
const headers = useRequestHeaders(['cookie'])
const me = await $fetch('/api/me', { headers })
```

Or use `useRequestFetch()`, which proxies headers to the call automatically (`const requestFetch = useRequestFetch()` then `requestFetch('/api/cookies')`). Per its page, headers that are not meant to be forwarded are not included, for example `transfer-encoding`, `connection`, `keep-alive`, `upgrade`, `expect`, `host` and `accept`. In the browser during client-side navigation it behaves like regular `$fetch`.

Be very careful before proxying headers to an external API and include only the headers you need. The data fetching docs list common headers that are NOT to be proxied: `host`, `accept`, `content-length`, `content-md5`, `content-type`, `x-forwarded-host`, `x-forwarded-port`, `x-forwarded-proto`, `cf-connecting-ip`, `cf-ray`.

The reverse direction (cookies from an internal API response back to the browser) you must handle yourself:

```ts
export const fetchWithCookie = async (event: H3Event, url: string) => {
  const res = await $fetch.raw(url)
  for (const cookie of res.headers.getSetCookie()) {
    event.res.headers.append('set-cookie', cookie)
  }
  return res._data
}
// const event = useRequestEvent()
// await useAsyncData(() => fetchWithCookie(event!, '/api/with-cookie'))
```

## Checked

2026-11-04. Confirmed against the Nuxt data fetching page and the useRequestFetch page: browser versus SSR cookie behaviour, useFetch proxying via useRequestFetch, useRequestHeaders example, the do-not-proxy list, the fetchWithCookie recipe, the list of non-forwarded headers. Removed the Verify step.

Method: documentation only; no commands were run.
