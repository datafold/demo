WITH org_events AS (
  SELECT
     *
  FROM {{ ref('dim_orgs') }}
  LEFT JOIN {{ ref('feature_used') }} USING (org_id)
  WHERE sub_plan IS NULL or sub_plan = 'Individual'
)

, final AS (
    SELECT 
        DISTINCT ORG_ID
        , count(*) AS usage
    FROM org_events
    WHERE
        -- select orgs created within the last 60 days, with usage within the 30 days
        event_timestamp::date > ('2022-11-01'::date - 30)
        AND created_at::date > ('2022-11-01'::date - 60)
    GROUP BY 1
)

SELECT * FROM final