{{ config(
    database='gold',
    schema='gold',
    materialized='table'
) }}

SELECT
    Country,
    count(*)                               AS total_orders,
    round(sum(total_revenue), 2)           AS total_sales,
    round(avg(total_revenue), 2)           AS avg_order_value
FROM {{ ref('silver_ecommerce_orders') }}
GROUP BY Country
ORDER BY total_sales DESC