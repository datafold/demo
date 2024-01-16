with final as (
    select
        date_trunc('month', sub_created_at) as date_month
        , count(distinct org_id) as cnt_subscribers
        , sum(sub_price) as sum_revenue
    from {{ ref('dim_orgs') }}
    where sub_created_at is not null
    group by 1
    order by 1
)

select * from final