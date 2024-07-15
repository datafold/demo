WITH org_events AS (
  SELECT
     *
  FROM {{ ref('dim__orgs') }}
  LEFT JOIN {{ ref('feature__used') }} USING (org_id)
  WHERE sub_plan IS NULL 
)

, final AS (
    SELECT 
        DISTINCT org_id
        , count(*) AS usage
    FROM org_events
    WHERE
        -- select orgs created within the last 60 days, with usage within the 30 days
        event_timestamp::date > (current_date - 30)
        AND created_at::date > (current_date - 60)
    GROUP BY 1
)

SELECT * FROM final
