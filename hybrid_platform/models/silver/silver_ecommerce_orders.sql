SELECT
    InvoiceNo,
    StockCode,
    Description,
    toInt32(Quantity)                       AS quantity,
    InvoiceDate,
    toFloat64(UnitPrice)                    AS unit_price,
    CustomerID,
    Country,
    Quantity * UnitPrice                    AS total_revenue,
    ingested_at
FROM bronze.ecommerce_orders_raw
WHERE Quantity > 0