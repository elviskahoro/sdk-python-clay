# CellPendingStatus

## Example Usage

```python
from clay.models import CellPendingStatus

# Open enum: unrecognized values are captured as UnrecognizedStr
value: CellPendingStatus = "running"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"running"`
- `"queued"`
- `"retry"`
- `"rate_limited"`
- `"awaiting_callback"`
