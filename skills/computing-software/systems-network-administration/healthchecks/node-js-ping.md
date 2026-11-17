---
id: computing-software.systems-network-administration.healthchecks.node-js-ping
name: node-js-ping
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, nodejs, axios, async-await, browser-xhr]
level: practitioner
status: docs-checked
description: "Ping Healthchecks from Node.js and browsers: https.get, an axios async/await start-success-fail pattern that avoids ordering races, and XMLHttpRequest."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/javascript.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Basic Node.js request:

```js
var https = require('https');
https.get('<ping-url>').on('error', (err) => {
    console.log('Ping failed: ' + err)
});
```

The `https` module executes requests asynchronously, so a success ping could arrive before a start ping. Use callbacks, promises or async/await to order them. With axios:

```js
const axios = require("axios");

async function ping(url) {
    try {
        await axios.get(url, {timeout: 5000});
    } catch(error) {
        console.error("Ping failed: " + error);
    }
}

async function runJob() {
    var pingUrl = "<ping-url>";
    await ping(pingUrl + "/start");
    try {
        // run the job here
        await ping(pingUrl); // success
    } catch(error) {
        await ping(pingUrl + "/fail");
    }
}
```

Each ping catches its own error, so a failed ping is logged and never stops the job.

Browser:

```js
var xhr = new XMLHttpRequest();
xhr.open('GET', '<ping-url>', true);
xhr.send(null);
```

The service sends a CORS header allowing cross-origin requests.

## Checked

2026-11-04: confirmed against the Javascript page (https.get, async race condition note, axios example, XMLHttpRequest, Access-Control-Allow-Origin header).
Method: documentation only; no commands were run.
