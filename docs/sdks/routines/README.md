# Routines

## Overview

Routine discovery and execution endpoints.

### Available Operations

* [get_routine_run_batch_results](#get_routine_run_batch_results) - Fetch progress and results for a batch run
* [get_run_results](#get_run_results) - Fetch progress and results for a routine run
* [run_routine](#run_routine) - Execute a routine against 1-100 items
* [start_routine_run_batch](#start_routine_run_batch) - Start an async routine run-batch over an uploaded JSONL file
* [run_routine_batch_upload_url](#run_routine_batch_upload_url) - Issue a presigned PUT URL for uploading a batch input JSONL

## get_routine_run_batch_results

Returns current status and results for an asynchronous batch routine run.

### Example Usage

<!-- UsageSnippet language="python" operationID="getRoutineRunBatchResults" method="get" path="/routines/run-batch/{routine_run_id}/results" -->
```python
from clay import Clay
import os


with Clay(
    clay_api_key=os.getenv("CLAY_CLAY_API_KEY", ""),
) as c_client:

    res = c_client.routines.get_routine_run_batch_results(routine_run_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `routine_run_id`                                                    | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetRoutineRunBatchResultsResponse](../../models/getroutinerunbatchresultsresponse.md)**

### Errors

| Error Type              | Status Code             | Content Type            |
| ----------------------- | ----------------------- | ----------------------- |
| errors.ErrorResponse    | 401, 404, 429           | application/json        |
| errors.ClayDefaultError | 4XX, 5XX                | \*/\*                   |

## get_run_results

Returns current status and paginated results for an asynchronous routine run.

### Example Usage

<!-- UsageSnippet language="python" operationID="getRunResults" method="get" path="/routines/run/{routine_run_id}/results" -->
```python
from clay import Clay
import os


with Clay(
    clay_api_key=os.getenv("CLAY_CLAY_API_KEY", ""),
) as c_client:

    res = c_client.routines.get_run_results(routine_run_id="<id>", limit=20)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `routine_run_id`                                                    | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `cursor`                                                            | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `limit`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetRunResultsResponse](../../models/getrunresultsresponse.md)**

### Errors

| Error Type              | Status Code             | Content Type            |
| ----------------------- | ----------------------- | ----------------------- |
| errors.ErrorResponse    | 401, 404, 429           | application/json        |
| errors.ClayDefaultError | 4XX, 5XX                | \*/\*                   |

## run_routine

Starts an asynchronous routine run for up to 100 input items.

### Example Usage

<!-- UsageSnippet language="python" operationID="runRoutine" method="post" path="/routines/{routine_id}/run" -->
```python
from clay import Clay
import os


with Clay(
    clay_api_key=os.getenv("CLAY_CLAY_API_KEY", ""),
) as c_client:

    res = c_client.routines.run_routine(routine_id="<id>", items=[])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `routine_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `items`                                                             | List[[models.Item](../../models/item.md)]                           | :heavy_check_mark:                                                  | N/A                                                                 |
| `webhook_id`                                                        | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | ID of a registered Clay webhook to notify when the run finishes.    |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.RunRoutineResponse](../../models/runroutineresponse.md)**

### Errors

| Error Type              | Status Code             | Content Type            |
| ----------------------- | ----------------------- | ----------------------- |
| errors.ErrorResponse    | 400, 401, 403, 404, 429 | application/json        |
| errors.ClayDefaultError | 4XX, 5XX                | \*/\*                   |

## start_routine_run_batch

Starts an asynchronous batch routine run over a previously uploaded JSONL file.

### Example Usage

<!-- UsageSnippet language="python" operationID="startRoutineRunBatch" method="post" path="/routines/{routine_id}/run-batch/start" -->
```python
from clay import Clay
import os


with Clay(
    clay_api_key=os.getenv("CLAY_CLAY_API_KEY", ""),
) as c_client:

    res = c_client.routines.start_routine_run_batch(routine_id="<id>", file_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `routine_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `file_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `webhook_id`                                                        | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | ID of a registered Clay webhook to notify when the run finishes.    |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.StartBatchResponse](../../models/startbatchresponse.md)**

### Errors

| Error Type              | Status Code             | Content Type            |
| ----------------------- | ----------------------- | ----------------------- |
| errors.ErrorResponse    | 400, 401, 403, 404, 429 | application/json        |
| errors.ClayDefaultError | 4XX, 5XX                | \*/\*                   |

## run_routine_batch_upload_url

Creates a presigned URL for uploading a JSONL file used by a batch routine run.

### Example Usage

<!-- UsageSnippet language="python" operationID="runRoutineBatchUploadUrl" method="post" path="/routines/{routine_id}/run-batch/upload-url" -->
```python
from clay import Clay
import os


with Clay(
    clay_api_key=os.getenv("CLAY_CLAY_API_KEY", ""),
) as c_client:

    res = c_client.routines.run_routine_batch_upload_url(routine_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `routine_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.BatchUploadURLResponse](../../models/batchuploadurlresponse.md)**

### Errors

| Error Type              | Status Code             | Content Type            |
| ----------------------- | ----------------------- | ----------------------- |
| errors.ErrorResponse    | 401, 403, 404, 429      | application/json        |
| errors.ClayDefaultError | 4XX, 5XX                | \*/\*                   |