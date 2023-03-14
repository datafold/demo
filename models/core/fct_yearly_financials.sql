select
    date_year
    , date_month
    , sum(cnt_subscribers)         as yearly_subscribers
    , sum(sum_revenue)             as yearly_revenue
    , hash(date_year) as id
from {{ref('fct_monthly_financials')}}
group by 1 , 2
