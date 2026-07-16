# Me

## Overview

Authenticated user and workspace endpoints.

### Available Operations

* [get](#get) - Get the authenticated user

## get

Returns the Clay user and workspace associated with the API key.

### Example Usage

<!-- UsageSnippet language="python" operationID="getPublicApiMe" method="get" path="/me" -->
```python
from clay import Clay
import os


with Clay(
    clay_api_key=os.getenv("CLAY_CLAY_API_KEY", ""),
) as c_client:

    res = c_client.me.get()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetPublicAPIMeResponse](../../models/getpublicapimeresponse.md)**

### Errors

| Error Type              | Status Code             | Content Type            |
| ----------------------- | ----------------------- | ----------------------- |
| errors.ErrorResponse    | 401, 403, 429           | application/json        |
| errors.ClayDefaultError | 4XX, 5XX                | \*/\*                   |