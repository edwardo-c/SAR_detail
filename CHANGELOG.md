## SAR DETAIL CHANGELOG

## [Unresolved]
- should bill to also be summed by acct_group?


## [Unreleased]
- process reclass in SAR_Pipeline (python)
- total attainment against total quota
- link report layer to data_model
- generate pdfs for emailing users

### Changed
- reclass logic moved to power query
- refactor: master [sales] table is now tabular by role
- refactored bill to 2025 data to separate pro_av from account_owner
- added attainment to quota by category in data model
- added 'segment' attribute for proav/keyaccounts subtotaling.
- integrated product category into rsm report layer data
- integrated key manager into sar pivot
- created sar credit pay structure view 
- organized tables inside data_model into groups (PQ)
- removed "sar_credit" logic in pos 2025 because reclass table 
  will rebalance the totals by pay_structure
- modified mtd DAX measures to account for lagging pos data
- added all DAX measures for consolidate view
- ungrouped sales in data_model; now holds line level detail 
- moved to data_model.xlsx to decouple data shaping
- adjust customer_name to account for ship to display names
- updated formulas for POS Performance
- consolidate direct and pos sales into single table
