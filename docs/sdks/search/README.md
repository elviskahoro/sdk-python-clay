# Search

## Overview

### Available Operations

* [create_filters](#create_filters) - Create a search from structured filters
* [fields](#fields) - List the filter fields available for a search source type
* [run](#run) - Run the search iterator and return the next page of results

## create_filters

Starts a new Clay search from a source type and structured filter fields.

### Example Usage

<!-- UsageSnippet language="python" operationID="createFilters" method="post" path="/search/filters-mode" -->
```python
from clay import Clay
import os


with Clay(
    clay_api_key=os.getenv("CLAY_CLAY_API_KEY", ""),
) as c_client:

    res = c_client.search.create_filters()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `request`                                                           | [models.CreateSearchRequest](../../models/createsearchrequest.md)   | :heavy_check_mark:                                                  | The request object to use for the request.                          |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.CreateSearchResponse](../../models/createsearchresponse.md)**

### Errors

| Error Type              | Status Code             | Content Type            |
| ----------------------- | ----------------------- | ----------------------- |
| errors.ErrorResponse    | 400, 401, 403, 404, 429 | application/json        |
| errors.ClayDefaultError | 4XX, 5XX                | \*/\*                   |

## fields

Returns every filter field accepted by POST /search/filters-mode for the given source type, including each field's type, description, allowed values, and usage guidance. Call this before creating a search to build valid filters.

### Example Usage

<!-- UsageSnippet language="python" operationID="fields" method="get" path="/search/filters-mode/fields" -->
```python
from clay import Clay
import os


with Clay(
    clay_api_key=os.getenv("CLAY_CLAY_API_KEY", ""),
) as c_client:

    res = c_client.search.fields(source_type="companies")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `source_type`                                                       | [models.FieldsSourceType](../../models/fieldssourcetype.md)         | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.SearchFieldsResponse](../../models/searchfieldsresponse.md)**

### Errors

| Error Type              | Status Code             | Content Type            |
| ----------------------- | ----------------------- | ----------------------- |
| errors.ErrorResponse    | 400, 401, 403, 429      | application/json        |
| errors.ClayDefaultError | 4XX, 5XX                | \*/\*                   |

## run

Returns the next page of records for an existing filter-mode search.

### Example Usage

<!-- UsageSnippet language="python" operationID="run" method="post" path="/search/filters-mode/{search_id}/run" -->
```python
from clay import Clay
import os


with Clay(
    clay_api_key=os.getenv("CLAY_CLAY_API_KEY", ""),
) as c_client:

    res = c_client.search.run(search_id="<id>", limit=20)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `search_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `limit`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.NextSearchResultsResponse](../../models/nextsearchresultsresponse.md)**

### Errors

| Error Type              | Status Code             | Content Type            |
| ----------------------- | ----------------------- | ----------------------- |
| errors.ErrorResponse    | 400, 401, 403, 404, 429 | application/json        |
| errors.ClayDefaultError | 4XX, 5XX                | \*/\*                   |