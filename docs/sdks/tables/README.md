# Tables

## Overview

Structured table query endpoints.

### Available Operations

* [query](#query) - Run a structured query across one or more tables

## query

Runs a structured query against Clay table data and returns records with field metadata.

### Example Usage

<!-- UsageSnippet language="python" operationID="query" method="post" path="/tables/query" -->
```python
from clay import Clay
import os


with Clay(
    clay_api_key=os.getenv("CLAY_CLAY_API_KEY", ""),
) as c_client:

    res = c_client.tables.query()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                               | Type                                                                    | Required                                                                | Description                                                             |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `request`                                                               | [models.StructuredQueryRequest](../../models/structuredqueryrequest.md) | :heavy_check_mark:                                                      | The request object to use for the request.                              |
| `retries`                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)        | :heavy_minus_sign:                                                      | Configuration to override the default retry behavior of the client.     |

### Response

**[models.QueryResponse](../../models/queryresponse.md)**

### Errors

| Error Type                   | Status Code                  | Content Type                 |
| ---------------------------- | ---------------------------- | ---------------------------- |
| errors.ErrorResponse         | 400, 401, 403, 404, 422, 429 | application/json             |
| errors.ClayDefaultError      | 4XX, 5XX                     | \*/\*                        |