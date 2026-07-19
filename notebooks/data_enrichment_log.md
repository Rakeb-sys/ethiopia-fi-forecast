# Data Enrichment Log

**Author / Collected By:** Data_Enrichment_Script  
**Date:** 2026-07-19  

## Overview of Changes
This log details structural additions made to track financial inclusion variables targeting forecasting models for Access and Usage in Ethiopia.

---

## 1. New Observations Added
* **Indicator Code:** `MOBILE_MONEY_ACC`
* **Pillar:** ACCESS
* **Value:** 43,000,000
* **Date:** 2024-02-01
* **Source:** Ethio Telecom Performance Report
* **Source URL:** https://www.ethiotelecom.et
* **Original Quote:** "Telebirr subscribers reached 43 million by early 2024."
* **Confidence Level:** High
* **Strategic Value:** Provides modern high-velocity infrastructure data points necessary for non-linear forecasting models.

---

## 2. New Events Tracked
* **Category:** Policy
* **Event Detail:** National Bank of Ethiopia Directive No. ONPSD/01/2020
* **Date:** 2020-04-01
* **Source:** National Bank of Ethiopia Directives
* **Source URL:** https://nbe.gov.et
* **Original Quote:** "NBE issued Directive No. ONPSD/01/2020 allowing non-banking institutions to offer mobile money services."
* **Confidence Level:** High
* **Strategic Value:** Flags the historical starting point of structural regulatory changes causing a break from linear baseline growth projections.

---

## 3. New Impact Links Modeled
* **Parent ID Reference:** REC_0035 (NBE Directive Event)
* **Target Indicator Linkage:** `MOBILE_MONEY_ACC`
* **Pillar Alignment:** USAGE
* **Direction / Magnitude:** Positive / High
* **Modeled Lag Horizon:** 12 Months
* **Evidence Justification:** Directly correlates systemic expansion to structural regulatory policy relaxation based on broader regional deployment precedents.
