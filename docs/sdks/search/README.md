# Search

## Overview

Search creation and pagination endpoints.

### Available Operations

* [create_filters](#create_filters) - Create a search from structured filters
* [fields](#fields) - List the filter fields available for a search source type
* [run](#run) - Run the search iterator and return the next page of results
* [create_query_mode](#create_query_mode) - Create a search from a Clay search query (beta)
* [query_mode_reference](#query_mode_reference) - Get the Clay search query reference (beta)
* [run_query_mode](#run_query_mode) - Run the query-mode iterator and return the next page of results (beta)

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

    res = c_client.search.create_filters(filters={
        "key": "<value>",
        "key1": "<value>",
    }, source_type="people")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                             | Type                                                                                  | Required                                                                              | Description                                                                           |
| ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `filters`                                                                             | Dict[str, *Any*]                                                                      | :heavy_check_mark:                                                                    | N/A                                                                                   |
| `source_type`                                                                         | [models.CreateSearchRequestSourceType](../../models/createsearchrequestsourcetype.md) | :heavy_check_mark:                                                                    | N/A                                                                                   |
| `retries`                                                                             | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                      | :heavy_minus_sign:                                                                    | Configuration to override the default retry behavior of the client.                   |

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

| Error Type                        | Status Code                       | Content Type                      |
| --------------------------------- | --------------------------------- | --------------------------------- |
| errors.ErrorResponse              | 400, 401, 402, 403, 404, 413, 429 | application/json                  |
| errors.ClayDefaultError           | 4XX, 5XX                          | \*/\*                             |

## create_query_mode

Starts a new Clay search from a Clay advanced search query. The source type is detected from the query and returned in the response. Count-mode and jobs queries are not supported.

### Example Usage

<!-- UsageSnippet language="python" operationID="createQueryMode" method="post" path="/search/query-mode" -->
```python
from clay import Clay
import os


with Clay(
    clay_api_key=os.getenv("CLAY_CLAY_API_KEY", ""),
) as c_client:

    res = c_client.search.create_query_mode(query="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `query`                                                             | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.CreateQueryModeResponse](../../models/createquerymoderesponse.md)**

### Errors

| Error Type              | Status Code             | Content Type            |
| ----------------------- | ----------------------- | ----------------------- |
| errors.ErrorResponse    | 400, 401, 403, 404, 429 | application/json        |
| errors.ClayDefaultError | 4XX, 5XX                | \*/\*                   |

## query_mode_reference

Returns the Clay search query reference document (markdown), covering the queryable fields and the query grammar. Use it to author a Clay advanced search query before creating a query-mode search.

### Example Usage

<!-- UsageSnippet language="python" operationID="queryModeReference" method="get" path="/search/query-mode/reference" -->
```python
from clay import Clay
import os


with Clay(
    clay_api_key=os.getenv("CLAY_CLAY_API_KEY", ""),
) as c_client:

    res = c_client.search.query_mode_reference()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.QueryModeReferenceResponse](../../models/querymodereferenceresponse.md)**

### Errors

| Error Type              | Status Code             | Content Type            |
| ----------------------- | ----------------------- | ----------------------- |
| errors.ErrorResponse    | 400, 401, 403, 429      | application/json        |
| errors.ClayDefaultError | 4XX, 5XX                | \*/\*                   |

## run_query_mode

Returns the next page of records for an existing query-mode search.

### Example Usage

<!-- UsageSnippet language="python" operationID="runQueryMode" method="post" path="/search/query-mode/{search_id}/run" -->
```python
from clay import Clay
import os


with Clay(
    clay_api_key=os.getenv("CLAY_CLAY_API_KEY", ""),
) as c_client:

    res = c_client.search.run_query_mode(search_id="<id>", limit=20)

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

**[models.NextQueryModeResultsResponse](../../models/nextquerymoderesultsresponse.md)**

### Errors

| Error Type              | Status Code             | Content Type            |
| ----------------------- | ----------------------- | ----------------------- |
| errors.ErrorResponse    | 400, 401, 403, 404, 429 | application/json        |
| errors.ClayDefaultError | 4XX, 5XX                | \*/\*                   |