SELECT
    symbol,
    toFloat64(price_usd)    AS price_usd,
    toFloat64(market_cap)   AS market_cap,
    toFloat64(total_volume) AS total_volume,
    ingestion_time
FROM bronze.crypto_prices