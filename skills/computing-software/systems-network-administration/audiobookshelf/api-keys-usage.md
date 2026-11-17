---
id: computing-software.systems-network-administration.audiobookshelf.api-keys-usage
name: api-keys-usage
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [api-keys, bearer-token, curl, rest-api, authorization-header]
level: practitioner
status: docs-checked
description: "Call the Audiobookshelf API with an API key in the Authorization Bearer header, using curl, JavaScript or Python."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/api-keys.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/book-library/2.book-metadata.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Send the key in the `Authorization` header of each request:

```bash
Authorization: Bearer <your_api_key_here>
```

curl:

```bash
curl -H "Authorization: Bearer <your_api_key>" \
     https://your-server:port/api/libraries
```

JavaScript:

```javascript
const response = await fetch("https://your-server:port/api/libraries", {
  headers: { Authorization: "Bearer <your_api_key>" },
});
const data = await response.json();
```

Python:

```python
import requests
response = requests.get("https://your-server:port/api/libraries",
                        headers={"Authorization": "Bearer <your_api_key>"})
data = response.json()
```

The request runs with the permissions of the user the key was created for. Remember that matching against online metadata providers is a manual action that "must be performed by the server admin or through the use of the API", so scripts using an admin-linked key can drive matching.

Keys can be deactivated, deleted or given an expiration date, so create a new key as an admin if one stops working. The full key is only shown at creation, so keep it in a secrets store rather than in scripts committed to version control. Use the Authorization header on every call.

## Checked

Method: docs-checked 2026-11-09 against the API Keys page and the Book Metadata page (manual match via API quote) of the Audiobookshelf docs repo. Dropped the unconfirmed rejection and HTTPS claims.
