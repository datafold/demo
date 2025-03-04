{{
  config(
    materialized='table'
  )
}}

WITH subscription_revenue AS (
    SELECT 
        SUBSTR(TO_CHAR((EVENT_TIMESTAMP::TIMESTAMPNTZ)::TIMESTAMPNTZ, 'YYYY-MM'), 0, 10) AS month,
        SUM(PRICE::DOUBLE)::NUMBER(10,0) AS revenue
    FROM {{ ref('subscription__created') }}
    GROUP BY 1
)

SELECT 
    month,
    revenue::NUMBER(18,0) AS revenue
FROM subscription_revenue 