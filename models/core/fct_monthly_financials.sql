WITH final AS (
    SELECT 
        date_trunc('month', sub_created_at) as date_month
        , count(distinct org_id) as cnt_subscribers
        , sum(sub_price) as sum_revenue
    FROM "COALESCE_DEMO"."CORE"."DIM_ORGS" 
    WHERE sub_created_at is not NULL 
    GROUP BY 1 
    ORDER BY 1
)

SELECT * FROM final