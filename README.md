# SAR_Detail

A Python-based pipeline for extracting and normalizing line-level sales data related to the Sales Attainment Report (SAR).  
This project replaces a Power Query-based solution due to performance and modeling limitations.

## Purpose

- Provide detailed sales data at the **rep-role-product** level
- Normalize roles and quota logic to match **business attainment**
- Support quota alignment by building a **scalable, reusable backend system**

## ⚙️ What This Does

- Loads raw sales and quota files
- Cleans and reshapes data using Python (pandas)
- Applies conditional logic for:
  - Role standardization (e.g., treating non-Pro AV as `"sales_person"`)
  - Category granularity (only Pro AV reps use `product_category` for quotas)
  - Composite keys for joining quotas to sales
- Outputs a clean, structured CSV ready for use in Power BI or Excel

## 🚫 Why Not Power Query?

Power Query proved insufficient due to:
- Sluggish performance with conditional category granularity
- Difficulty managing composite relationships
- Repeated rebuilds from minor logic changes

Python offers better control, speed, and future extensibility.

