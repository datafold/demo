{{
  config(
    materialized='table'
  )
}}

WITH subscription_data AS (
    SELECT 
        ORG_ID::DOUBLE AS ORG_ID,
        PLAN
    FROM {{ ref('subscription__created') }}
),

feature_usage AS (
    SELECT 
        ORG_ID::DOUBLE AS ORG_ID,
        ACTIVITY,
        TO_CHAR((EVENT_TIMESTAMP::TIMESTAMPNTZ)::TIMESTAMPNTZ, 'MM')::NUMBER(10,0) AS month_num
    FROM {{ ref('feature__used') }}
    WHERE TO_CHAR((EVENT_TIMESTAMP::TIMESTAMPNTZ)::TIMESTAMPNTZ, 'MM')::NUMBER(10,0) = 1
)

SELECT 
    COUNT(f.ORG_ID)::NUMBER(10,0) AS org_cnt,
    ANY_VALUE(f.ORG_ID) AS fu_ORG_ID,
    f.ACTIVITY AS fu_ACTIVITY,
    s.PLAN AS sc_PLAN
FROM subscription_data s
JOIN feature_usage f ON f.ORG_ID = s.ORG_ID
GROUP BY s.PLAN, f.ACTIVITY 