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
        , case when plan is null then 'Null' else plan end as sub_plan
        , price as sub_price
    FROM {{ source('EVENTS', 'SUBSCRIPTION_CREATED') }}
)

, final AS (
    SELECT
        * 
    FROM orgs
    LEFT JOIN user_count USING (org_id)
    INNER JOIN subscriptions USING (org_id)
)

SELECT * FROM final