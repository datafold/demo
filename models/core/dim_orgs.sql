WITH orgs AS (
--prod
    SELECT
        org_id
        , org_name
        , employee_range
        , created_at
    FROM {{ ref('org_created') }}

-- --dev
--    SELECT
--         org_id
--         , org_name
--         , employee_range
--         , created_at
--     FROM {{ ref('org_created') }}
)

, user_count AS (
    SELECT
        org_id
        , count(distinct user_id) AS num_users
    FROM {{ ref('user_created') }}
    GROUP BY 1
)

, subscriptions AS (
    SELECT
        org_id
        , event_timestamp AS sub_created_at
        , plan as sub_plan
        , coalesce(price, 0) as sub_price
    FROM {{ ref('subscription_created') }}
)


SELECT
    org_id
    , created_at
    , num_users
    , sub_created_at
    , case when num_users = 1 then 'Individual' else sub_plan end as sub_plan
    , sub_price
FROM orgs
LEFT JOIN user_count USING (org_id)
LEFT JOIN subscriptions USING (org_id)
