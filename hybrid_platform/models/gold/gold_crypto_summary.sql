{{ config(
    database='gold',
    schema='gold',
    materialized='table'
) }}

SELECT
    symbol,
    round(avg(price_usd), 2)    AS avg_price,
    max(price_usd)              AS max_price,
    min(price_usd)              AS min_price,
    count(*)                    AS records_ingested
FROM {{ ref('silver_crypto_prices') }}
GROUP BY symbol