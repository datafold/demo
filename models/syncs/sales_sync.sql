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
    WHERE event_timestamp < dateadd('day', 30, created_at)
        AND event_timestamp > dateadd('day', -21, '2022-11-09'::date)
        AND created_at > dateadd('day', -32, '2022-11-09'::date)
    GROUP BY 1
)

SELECT * FROM final