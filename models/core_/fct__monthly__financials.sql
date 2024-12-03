-- WITH final AS (
--     SELECT 
--         date_trunc('month', sub_created_at) as date_month
--         , count(distinct org_id) as cnt_subscribers
--         , sum(sub_price) as sum_revenue
--     FROM {{ ref('dim__orgs') }}
--     WHERE sub_created_at is not NULL 
--     GROUP BY 1 
--     ORDER BY 1
-- )

-- SELECT * FROM final



WITH final AS (
    -- SELECT 
    --     date_trunc('month', sub_created_at) as date_month
    --     , count(distinct org_id) as cnt_subscribers
    --     , sum(sub_price) as sum_revenue
    -- FROM {{ ref('dim__orgs') }}
    -- WHERE sub_created_at is not NULL 
    -- GROUP BY 1 
    -- ORDER BY 1

    {% if target.name == 'sf' %}
        SELECT 
            date_trunc('month', sub_created_at) as date_month
            , count(distinct org_id) as cnt_subscribers
            , case
            when date_trunc('month', sub_created_at) >= '2024-09-30' and date_trunc('month', sub_created_at) <= '2024-10-02'
            then sum(sub_price) * 2
            else sum(sub_price) end as sum_revenue
        FROM {{ ref('dim__orgs') }}
        WHERE sub_created_at is not NULL 
        GROUP BY 1 
        ORDER BY 1
    {% elif target.name == 'db' %}
        SELECT 
            date_trunc('month', sub_created_at) as date_month
            , count(distinct org_id) as cnt_subscribers
            , sum(sub_price) as sum_revenue
        FROM {{ ref('dim__orgs') }}
        WHERE sub_created_at is not NULL 
        GROUP BY 1 
        ORDER BY 1
    {% elif target.name == 'bq' %}
        SELECT
          TIMESTAMP_TRUNC(sub_created_at, month) AS date_month,
          COUNT(DISTINCT org_id) AS cnt_subscribers,
          SUM(sub_price) AS sum_revenue
        FROM {{ ref('dim__orgs') }}
        WHERE NOT sub_created_at IS NULL
        GROUP BY 1
        ORDER BY 1 NULLS LAST
    {% else %}
        SELECT 
            date_trunc('month', sub_created_at) as date_month
            , count(distinct org_id) as cnt_subscribers
            , sum(sub_price) as sum_revenue
        FROM {{ ref('dim__orgs') }}
        WHERE sub_created_at is not NULL 
        GROUP BY 1 
        ORDER BY 1
    {% endif %}

)

SELECT * FROM final





