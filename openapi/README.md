# OpenAPI spec

`openapi.json` is vendored, not fetched at build time. `.speakeasy/workflow.yaml` points at
it as a relative path.

Upstream: <https://developers.clay.com/openapi.json> — served publicly, no auth.

Note that the API host itself (`https://api.clay.com/public/v0`) does **not** serve the
spec; every path there sits behind an auth wall and 404s even with a valid key. Use the
docs host above.

To refresh:

```shell
curl -sL https://developers.clay.com/openapi.json \
  | python3 -c 'import json,sys; print(json.dumps(json.load(sys.stdin), indent=2))' \
  > openapi/openapi.json
speakeasy run -t all
```

The upstream document is served with keys already sorted, so plain `indent=2` round-tripping
produces a minimal diff.

## After a refresh

Clay's spec omits `requestBody.required` on every POST, which would generate
`request: Optional[...] = None` and let callers skip a body the API demands.
`.speakeasy/overlays/required-bodies.overlay.yaml` corrects this per-operation, so
**if the refresh added a POST, add it to that overlay** — but only if its body schema
has required fields. Check with:

```shell
python3 -c "
import json; d = json.load(open('openapi/openapi.json'))
for p, ops in d['paths'].items():
    for m, op in ops.items():
        rb = op.get('requestBody')
        if not rb: continue
        s = rb['content']['application/json']['schema']
        while '\$ref' in s: s = d['components']['schemas'][s['\$ref'].split('/')[-1]]
        print(f'{m.upper():5} {p:45} required={s.get(\"required\")}')"
```

## Notes

`info.version` is pinned at `"0"` and does not move when the API changes, so it is not a
useful signal for whether a refresh is needed — diff the file instead.
