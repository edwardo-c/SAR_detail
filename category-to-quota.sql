-- Return total sales by product category
-- joined with rep's quota
WITH category_sales AS (
    SELECT
        s.rep,
        s.rep_role_key,
        s.product_category, 
        SUM(amount) as net_sales
    FROM sales AS s
    WHERE credit_year = 2025 AND product_category IS NOT NULL
    GROUP BY s.rep, s.rep_role_key, s.product_category
) 
SELECT
    cs.rep,
    cs.product_category,
    cs.net_sales,
    q.sales_objective,
    CAST(cs.net_sales AS FLOAT) / NULLIF(q.sales_objective, 0) AS percent_to_quota
FROM category_sales as cs
LEFT JOIN pro_av_quotas_2025 AS q ON (cs.rep_role_key = q.rep_category_key)
ORDER BY percent_to_quota DESC