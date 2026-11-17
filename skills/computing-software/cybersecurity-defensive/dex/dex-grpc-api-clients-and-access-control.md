---
id: computing-software.cybersecurity-defensive.dex.dex-grpc-api-clients-and-access-control
name: dex-grpc-api-clients-and-access-control
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [grpc, api, protobuf, go-client]
level: advanced
status: docs-checked
description: "Call the Dex gRPC API from Go or generate bindings from api.proto, and put access checks in your own app because Dex adds none."
sources:
  - https://dexidp.io/docs/configuration/api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The canonical schema is `api/v2/api.proto` in the Dex source tree. Go bindings live in the same directory.

Go: import only the API module rather than all of Dex.

```bash
go get github.com/dexidp/dex/api/v2
```

Build a client with TLS credentials and create an OAuth2 client:

```go
creds, _ := credentials.NewClientTLSFromFile(caPath, "")
conn, _ := grpc.Dial("127.0.0.1:5557", grpc.WithTransportCredentials(creds))
client := api.NewDexClient(conn)
_, err := client.CreateClient(ctx, &api.CreateClientReq{
    Client: &api.Client{Id: "example-app", Name: "Example App",
        Secret: "ZXhhbXBsZS1hcHAtc2VjcmV0",
        RedirectUris: []string{"http://127.0.0.1:5555/callback"}},
})
```

Other languages: install `protoc` and a generator, download `api.proto` for a Dex version and generate bindings:

```bash
DEX_VERSION=v2.24.0
wget https://raw.githubusercontent.com/dexidp/dex/${DEX_VERSION}/api/v2/api.proto
protoc [YOUR LANG PARAMS] api.proto
```

Access control: the API has no authentication or authorization beyond TLS client auth. To add rules, build an app that checks them first. For a "change password" screen, a client app can use Dex's OIDC flow to authenticate the user, then call the API to update that user's password.

For testing, the `staticClients` config field is easier than the API.

## Checked

2026-11-08: Read the Dex API page in full. Confirmed api/v2/api.proto, the go get module path, the Go client example (shortened, errors elided), the protoc steps with the v2.24.0 example version, the access control statement and the staticClients note.
Method: documentation only; no commands were run.
