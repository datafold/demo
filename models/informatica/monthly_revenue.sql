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
    revenue::NUMBER(10,0) AS revenue,
    month::VARCHAR(10) AS month
FROM subscription_revenue 