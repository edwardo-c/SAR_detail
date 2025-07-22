-- Return pay_structure total by month in tabular form
-- pivoted in power query in final report

SELECT
    rep,
    pay_structure,
    credit_month,
    SUM(amount) AS total
FROM sales
WHERE credit_year = 2025
GROUP BY rep, pay_structure, credit_month
