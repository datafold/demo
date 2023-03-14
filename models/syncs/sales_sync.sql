WITH org_events AS (
  SELECT
     *
  FROM {{ ref('dim_orgs') }}
  LEFT JOIN {{ ref('feature_used') }} USING (org_id)
  WHERE sub_plan IS NULL 
)

, final AS (
    SELECT 
        DISTINCT ORG_ID
        , count(*) AS usage
    FROM org_events
    WHERE 
        event_timestamp::date <  (created_at::date + 45)
        AND event_timestamp::date > ('2022-11-09'::date - 10)
        AND created_at::date > ('2022-11-09'::date - 60)
    GROUP BY 1
)

SELECT * FROM final