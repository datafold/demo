WITH final AS (
    SELECT 
        extract( 'year' from sub_created_at) as date_year
        , extract( 'month' from sub_created_at) as date_month
        , count(distinct org_id) as cnt_subscribers
        , sum(sub_price) as sum_revenue
        , hash(date_month) as id
    FROM {{ ref('dim_orgs') }}
    WHERE sub_created_at is not NULL 
    GROUP BY 1 , 2
    ORDER BY 1
)

SELECT * FROM final