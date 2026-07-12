<!-- Start SDK Example Usage [usage] -->
```python
# Synchronous Example
from clay import Clay
import os


with Clay(
    clay_api_key=os.getenv("CLAY_CLAY_API_KEY", ""),
) as c_client:

    res = c_client.me.get_public_api_me()

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asynchronous requests by importing asyncio.

```python
# Asynchronous Example
import asyncio
from clay import Clay
import os

async def main():

    async with Clay(
        clay_api_key=os.getenv("CLAY_CLAY_API_KEY", ""),
    ) as c_client:

        res = await c_client.me.get_public_api_me_async()

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->