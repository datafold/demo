WITH org_events AS (
  SELECT
     a.org_id
     , a.created_at
     , a.num_users
     , a.sub_created_at
     , a.sub_plan
     , a.sub_price
     , b.event_timestamp
     , b.activity
  FROM {{ ref('dim__orgs') }} a
  LEFT JOIN {{ ref('feature__used') }} b on a.org_id = b.org_id
  WHERE sub_plan IS NULL or sub_plan = 'Individual'
)

, final AS (
    SELECT 
        DISTINCT org_id
        , count(*) AS usage
    FROM org_events
    WHERE
        -- -- select orgs created within the last 60 days, with usage within the 30 days
        -- event_timestamp::date > (current_date - 30)
        -- AND created_at::date > (current_date - 60)

        {% if target.name == 'sf' %}
            event_timestamp::date > (current_date - 30)
            AND created_at::date > (current_date - 60)
        {% elif target.name == 'db' %}
            event_timestamp::date > (current_date - 30)
            AND created_at::date > (current_date - 60)
        {% elif target.name == 'bq' %}
            CAST(event_timestamp /* select orgs created within the last 60 days, with usage within the 30 days */ AS DATE) > (
              CURRENT_DATE - 30
            )
            AND CAST(created_at AS DATE) > (
              CURRENT_DATE - 60
            )
        {% elif target.name == 'dr' %}
            CAST(event_timestamp AS DATE) > DATE_SUB(current_date, 30)
            AND CAST(created_at AS DATE) > DATE_SUB(current_date, 60)
        {% else %}
            event_timestamp::date > (current_date - 30)
            AND created_at::date > (current_date - 60)
        {% endif %}



    GROUP BY 1
)

SELECT * FROM final
