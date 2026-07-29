# Tables

## Overview

Structured table query endpoints.

### Available Operations

* [query](#query) - Run a structured query across one or more tables

## query

Runs a structured query against Clay table data and returns records with field metadata. Results are paginated: pass the returned cursor back to fetch the next page. Scans return rows in least-recently-updated-first order and reflect writes that land while you paginate — a scan returns every record visible when it started and picks up records written while it runs, and a record updated mid-scan can be returned again with fresher data, so deduplicate by id if you need each record once.

### Example Usage

<!-- UsageSnippet language="python" operationID="query" method="post" path="/tables/query" -->
```python
from clay import Clay, models
import os


with Clay(
    clay_api_key=os.getenv("CLAY_CLAY_API_KEY", ""),
) as c_client:

    res = c_client.tables.query(query=models.StructuredQuery(
        tables=[],
    ), limit=50)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                        | Type                                                                                                                                                                                             | Required                                                                                                                                                                                         | Description                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `query`                                                                                                                                                                                          | [models.StructuredQuery](../../models/structuredquery.md)                                                                                                                                        | :heavy_check_mark:                                                                                                                                                                               | N/A                                                                                                                                                                                              |
| `cursor`                                                                                                                                                                                         | *Optional[str]*                                                                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                                               | Opaque cursor from the previous response. Scans page in least-recently-updated-first order and reflect concurrent writes: a record updated mid-scan can be returned again, so deduplicate by id. |
| `limit`                                                                                                                                                                                          | *Optional[int]*                                                                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                                               | N/A                                                                                                                                                                                              |
| `retries`                                                                                                                                                                                        | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                                               | Configuration to override the default retry behavior of the client.                                                                                                                              |

### Response

**[models.QueryResponse](../../models/queryresponse.md)**

### Errors

| Error Type                   | Status Code                  | Content Type                 |
| ---------------------------- | ---------------------------- | ---------------------------- |
| errors.ErrorResponse         | 400, 401, 403, 404, 422, 429 | application/json             |
| errors.ClayDefaultError      | 4XX, 5XX                     | \*/\*                        |