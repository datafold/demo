select
    date_trunc('year', date_month) as date_year
    , sum(cnt_subscribers)         as yearly_subscribers
    , sum(sum_revenue)             as yearly_revenue
from {{ref('fct_monthly_financials')}}
group by 1
