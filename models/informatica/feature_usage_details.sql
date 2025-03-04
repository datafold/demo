{{
  config(
    materialized='table'
  )
}}

WITH org_data AS (
    SELECT 
        ORG_ID::DOUBLE AS ORG_ID,
        ORG_NAME,
        DOMAIN,
        EMPLOYEE_RANGE,
        CREATED_AT::TIMESTAMPNTZ AS CREATED_AT
    FROM {{ ref('org__created') }}
),

feature_usage AS (
    SELECT 
        ORG_ID::DOUBLE AS ORG_ID,
        EVENT_TIMESTAMP::TIMESTAMPNTZ AS EVENT_TIMESTAMP,
        ACTIVITY
    FROM {{ ref('feature__used') }}
)

SELECT 
    f.ORG_ID::NUMBER(38,0) AS "fu_ORG_ID",
    f.EVENT_TIMESTAMP::TIMESTAMPNTZ AS "fu_EVENT_TIMESTAMP",
    f.ACTIVITY::VARCHAR(16777216) AS "fu_ACTIVITY",
    o.ORG_ID::NUMBER(38,0) AS "oc_ORG_ID",
    o.ORG_NAME::VARCHAR(16777216) AS "oc_ORG_NAME",
    o.DOMAIN::VARCHAR(16777216) AS "oc_DOMAIN",
    o.EMPLOYEE_RANGE::VARCHAR(16777216) AS "oc_EMPLOYEE_RANGE",
    o.CREATED_AT::TIMESTAMPNTZ AS "oc_CREATED_AT"
FROM feature_usage f
JOIN org_data o ON f.ORG_ID = o.ORG_ID 