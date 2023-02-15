WITH orgs AS (
    SELECT 
        org_id
        , MIN(event_timestamp) AS created_at
    FROM {{ source('EVENTS', 'SIGNED_IN') }}
    GROUP BY 1
)

, user_count AS (
    SELECT
        org_id
        , count(distinct user_id) AS num_users
    FROM {{ source('EVENTS', 'USER_CREATED') }}
    GROUP BY 1
)

, subscriptions AS (
    SELECT
        org_id
        , event_timestamp AS sub_created_at
        , plan as sub_plan
        , price as sub_price
    FROM {{ source('EVENTS', 'SUBSCRIPTION_CREATED') }}
)

, final AS (
    SELECT
        org_id
        , created_at
        , num_users
        , CASE WHEN sub_created_at IS NULL THEN 0::TIMESTAMP_NTZ ELSE sub_created_at END AS sub_created_at
        , CASE WHEN num_users = 1 THEN 'Individual' ELSE sub_plan END AS sub_plan
        , sub_price
    FROM orgs
    LEFT JOIN user_count USING (org_id)
    LEFT JOIN subscriptions USING (org_id)
)

SELECT * FROM final