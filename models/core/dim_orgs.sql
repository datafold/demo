WITH orgs AS (
    SELECT 
        org_id
        , MIN(event_timestamp) AS created_at
    FROM {{ ref('signed_in') }}
    GROUP BY 1
)

, raw_user_count AS (
    SELECT
        org_id
        , count(distinct user_id) AS num_users
    FROM {{ ref('user_created') }}
    GROUP BY 1
)

, user_count AS (
    SELECT
        org_id
        , case when num_users < 5 then 5
        else num_users end as num_users
    FROM raw_user_count
)

, subscriptions AS (
    SELECT
        org_id
        , event_timestamp AS sub_created_at
        , plan as sub_plan
        , price as sub_price
    FROM {{ ref('subscription_created') }}
)

, final AS (
    SELECT
        * 
    FROM orgs
    LEFT JOIN user_count USING (org_id)
    LEFT JOIN subscriptions USING (org_id)
)

SELECT * FROM final
WHERE sub_created_at > '2022-06-01'