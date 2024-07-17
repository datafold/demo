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
        -- select orgs created within the last 60 days, with usage within the 30 days
        -- event_timestamp::date > ('2022-11-01'::date - 30)
        -- AND created_at::date > ('2022-11-01'::date - 60)

        {% if target.name == 'sf' %}
            event_timestamp::date > ('2022-11-01'::date - 30)
            AND created_at::date > ('2022-11-01'::date - 60)
        {% elif target.name == 'db' %}
            event_timestamp::date > ('2022-11-01'::date - 30)
            AND created_at::date > ('2022-11-01'::date - 60)
        {% elif target.name == 'bq' %}
            CAST(event_timestamp /* select orgs created within the last 60 days, with usage within the 30 days */ AS DATE) > (
              CAST('2022-11-01' AS DATE) - 30
            )
            AND CAST(created_at AS DATE) > (
              CAST('2022-11-01' AS DATE) - 60
            )
        {% else %}
            event_timestamp::date > ('2022-11-01'::date - 30)
            AND created_at::date > ('2022-11-01'::date - 60)
        {% endif %}
 
    GROUP BY 1
)

SELECT * FROM final
