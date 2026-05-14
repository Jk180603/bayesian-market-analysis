-- 1. Channel-level performance
SELECT
    channel,
    ROUND(SUM(spend), 2) AS total_spend,
    SUM(clicks) AS total_clicks,
    SUM(conversions) AS total_conversions,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(revenue) / NULLIF(SUM(spend), 0), 2) AS roas
FROM marketing_campaigns
GROUP BY channel
ORDER BY total_revenue DESC;


-- 2. Daily revenue trend
SELECT
    date,
    ROUND(SUM(spend), 2) AS daily_spend,
    SUM(conversions) AS daily_conversions,
    ROUND(SUM(revenue), 2) AS daily_revenue
FROM marketing_campaigns
GROUP BY date
ORDER BY date;


-- 3. Cost per conversion by channel
SELECT
    channel,
    ROUND(SUM(spend) / NULLIF(SUM(conversions), 0), 2) AS cost_per_conversion
FROM marketing_campaigns
GROUP BY channel
ORDER BY cost_per_conversion ASC;


-- 4. Best performing channels by conversion rate
SELECT
    channel,
    ROUND(SUM(conversions)::numeric / NULLIF(SUM(clicks), 0), 4) AS conversion_rate
FROM marketing_campaigns
GROUP BY channel
ORDER BY conversion_rate DESC;