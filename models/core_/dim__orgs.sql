WITH orgs AS (
--prod
--    SELECT
--        org_id
--        , MIN(event_timestamp) AS created_at
--    FROM {{ ref('signed__in') }}
--    GROUP BY 1

 --dev
    SELECT
         org_id
         , org_name
         , employee_range
         , created_at
     FROM {{ ref('org__created') }}
)

, user_count AS (
    SELECT
        org_id
        , count(distinct user_id) AS num_users
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
    orgs.org_id
    , created_at
    , case when num_users > 4 then 4 else num_users end as num_users
    , sub_created_at
    , case when num_users = 1 then 'Individual' else sub_plan end as sub_plan
    , case when sub_price = 99 then 100 else sub_price end as sub_price
FROM orgs
LEFT JOIN user_count on orgs.org_id = user_count.org_id
LEFT JOIN subscriptions on orgs.org_id = subscriptions.org_id
