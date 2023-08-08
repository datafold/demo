WITH org_events AS (
  SELECT
     *
  FROM {{ ref('dim_orgs') }}
  LEFT JOIN {{ ref('feature_used') }} USING (orgid)
  WHERE plan IS NULL and 1=1
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