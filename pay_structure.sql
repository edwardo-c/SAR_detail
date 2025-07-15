-- pay structure view --
SELECT rep, pay_structure, SUM(amount) as total 
FROM sales
WHERE credit_year = 2025
GROUP BY rep, pay_structure

UNION ALL

SELECT
    rep,
    NULL AS pay_structure,
    SUM(amount) as total
FROM sales
WHERE credit_year = 2025
GROUP BY rep

ORDER BY rep
