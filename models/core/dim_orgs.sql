WITH orgs AS (
    SELECT 
        org_id
        , org_name
        , employee_range
        , created_at
    FROM {{ source('EVENTS', 'ORG_CREATED') }}
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
        * 
    FROM orgs
    LEFT JOIN user_count USING (org_id)
    LEFT JOIN subscriptions USING (org_id)
)

SELECT * FROM final