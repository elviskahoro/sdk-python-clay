# StructuredQuery


## Fields

| Field                                                              | Type                                                               | Required                                                           | Description                                                        |
| ------------------------------------------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| `field_mode`                                                       | [Optional[models.FieldMode]](../models/fieldmode.md)               | :heavy_minus_sign:                                                 | N/A                                                                |
| `filter_`                                                          | [Optional[models.FilterExpression]](../models/filterexpression.md) | :heavy_minus_sign:                                                 | N/A                                                                |
| `group_by`                                                         | List[*str*]                                                        | :heavy_minus_sign:                                                 | N/A                                                                |
| `join`                                                             | List[[models.Join](../models/join.md)]                             | :heavy_minus_sign:                                                 | N/A                                                                |
| `order_by`                                                         | List[[models.OrderBy](../models/orderby.md)]                       | :heavy_minus_sign:                                                 | N/A                                                                |
| `select`                                                           | List[[models.Select](../models/select.md)]                         | :heavy_minus_sign:                                                 | N/A                                                                |
| `tables`                                                           | List[[models.Table](../models/table.md)]                           | :heavy_check_mark:                                                 | N/A                                                                |