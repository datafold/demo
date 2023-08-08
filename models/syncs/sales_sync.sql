WITH org_events AS (
  SELECT
     do.*,
     fu.event_timestamp,
     fu.activity
  FROM {{ ref('dim_orgs') }} do
  LEFT JOIN {{ ref('feature_used') }} fu on do.orgid = fu.org_id
  WHERE plan IS NULL and 4=4
)

, final AS (
    SELECT 
        DISTINCT ORGID
        , count(*) AS usage
    FROM org_events
    WHERE
        -- select orgs created within the last 60 days, with usage within the 30 days
        event_timestamp::date > ('2022-11-01'::date - 30)
        AND created_at::date > ('2022-11-01'::date - 61)
    GROUP BY 1
)

SELECT * FROM final