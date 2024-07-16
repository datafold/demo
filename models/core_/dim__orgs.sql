WITH orgs AS (
--prod
    SELECT
        org_id
        , MIN(event_timestamp) AS created_at
    FROM {{ ref('signed__in') }}
    GROUP BY 1

-- --dev
--    SELECT
--         org_id
--         , org_name
--         , employee_range
--         , created_at
--     FROM {{ ref('org__created') }}
)

, user_count AS (
    SELECT
        org_id
        , count(distinct user_id) + 1 AS num_users
    FROM {{ ref('user__created') }}
    GROUP BY 1
)

, subscriptions AS (
    SELECT
        org_id
        , event_timestamp AS sub_created_at
        , plan as sub_plan
        , price as sub_price
    FROM {{ ref('subscription__created') }}
)


SELECT
    org_id
    , created_at
    , num_users
    , sub_created_at
    , sub_plan
    , sub_price
FROM orgs
LEFT JOIN user_count USING (org_id)
LEFT JOIN subscriptions USING (org_id)
