# OpenAPI spec

`openapi.json` is vendored, not fetched at build time. `.speakeasy/workflow.yaml` points at
it as a relative path.

Upstream: <https://developers.clay.com/openapi.json> — served publicly, no auth.

Note that the API host itself (`https://api.clay.com/public/v0`) does **not** serve the
spec; every path there sits behind an auth wall and 404s even with a valid key. Use the
docs host above.

To refresh with the Dagger pipeline:

```shell
dagger run uv run python ci/pipeline.py generate
```

This fetches the current document, runs Speakeasy, and exports the generated
SDK back to the checkout. Set `SPEAKEASY_API_KEY` for fully isolated Dagger
generation, or authenticate the local Speakeasy CLI with `speakeasy auth login`.

To fetch only, run `dagger run uv run python ci/pipeline.py fetch-openapi`.

To build and publish the latest generated package to PyPI, add `PYPI_TOKEN` to
the untracked `.env.local` file, then run:

```shell
dagger run uv run python ci/pipeline.py publish
```

Publishing uses the shared
[`sdk-python-publish-to-pypi`](https://github.com/elviskahoro/sdk-python-publish-to-pypi)
Dagger module. The token is supplied as a Dagger secret and is not copied into
the SDK or distribution artifacts. To generate, validate, build, and publish in
one command, use `dagger run uv run python ci/pipeline.py ci --publish`.

The manual equivalent is:

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
