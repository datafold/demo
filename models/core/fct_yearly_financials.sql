-- select
--     date_trunc('year', date_month) as date_year
--     , sum(cnt_subscribers)         as yearly_subscribers
--     , sum(sum_revenue)             as yearly_revenue
-- from {{ref('fct_monthly_financials')}}
-- group by 1





{% if target.name == 'sf' %}
    select
        date_trunc('year', date_month) as date_year
        , sum(cnt_subscribers)         as yearly_subscribers
        , sum(sum_revenue)             as yearly_revenue
    from {{ref('fct_monthly_financials')}}
    group by 1
{% elif target.name == 'db' %}
    select
        date_trunc('year', date_month) as date_year
        , sum(cnt_subscribers)         as yearly_subscribers
        , sum(sum_revenue)             as yearly_revenue
    from {{ref('fct_monthly_financials')}}
    group by 1
{% elif target.name == 'bq' %}
    SELECT
        DATE_TRUNC(date_month, YEAR) AS date_year,
        SUM(cnt_subscribers) AS yearly_subscribers,
        SUM(sum_revenue) AS yearly_revenue
    FROM {{ ref('fct_monthly_financials') }}
    GROUP BY 1
{% else %}
    select
        date_trunc('year', date_month) as date_year
        , sum(cnt_subscribers)         as yearly_subscribers
        , sum(sum_revenue)             as yearly_revenue
    from {{ref('fct_monthly_financials')}}
    group by 1
{% endif %}






