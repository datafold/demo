WITH orgs AS (
    SELECT
        org_id
        , MIN(event_timestamp) AS created_at
    FROM DB.PR_NUM_123.signed_in
    GROUP BY 1
)

, user_count AS (
    SELECT
        org_id
        , count(distinct user_id) AS num_users
    FROM DB.PR_NUM_123.user_created
    GROUP BY 1
)

, subscriptions AS (
    SELECT
        org_id
        , event_timestamp AS sub_created_at
        , plan as sub_plan
        , price as sub_price
    FROM DB.PR_NUM_123.subscription_created
)

, final AS (
    SELECT
        * 
    FROM orgs
    LEFT JOIN user_count USING (org_id)
    LEFT JOIN subscriptions USING (org_id)
)

SELECT * FROM final