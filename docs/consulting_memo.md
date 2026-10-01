# Management consulting memo | Synthetic healthcare commercial prioritization

**Client situation:** A hypothetical commercial team must allocate limited analytical and field capacity across four regions, six products, and three therapy areas. The challenge is to identify where further investigation could improve commercial performance while respecting medical/compliance constraints.

## Structured issue tree
1. **Commercial scale:** Where is current revenue concentrated and how does it change by month?
2. **Unit economics:** Which product/region combinations deliver gross profit and contribution after promotion spend?
3. **Channel opportunity:** In which region/therapy segments is simulated physician potential high but visits low?
4. **Continuity signal:** Which independent synthetic episode cohorts show higher day-120 discontinuation and warrant medical review?
5. **Execution:** Which limited experiments can validate the economic assumptions without overgeneralizing observational data?

## Evidence and model
Use `outputs/executive_kpis.csv`, `outputs/regional_performance.csv`, `outputs/segment_prioritization.csv` and the automatically generated `outputs/executive_strategy_brief.md`. Keep revenue/margin, channel potential and clinical-continuity **separate** when interpreting the priority score.

## Proposed 90-day action plan
- **Days 1–15:** Align on objectives and metric definitions; reconcile the source data; obtain finance, commercial, medical and compliance review.
- **Days 16–45:** Test a compliant physician-segment outreach plan in selected regions; define a comparable control group before making changes.
- **Days 46–70:** Work with medical/compliance teams on permitted aggregate patient-support information if a discontinuation issue warrants investigation.
- **Days 71–90:** Evaluate changes in contribution after promotion, margin, descriptive call efficiency and any appropriately governed continuity metric. Adjust or stop before wider scaling.

## Risks / decision safeguards
1. High revenue does not imply a large untapped market.
2. High margin and high volume can point to different commercial choices.
3. Higher discontinuation may reflect many unrelated factors; do not turn this into treatment recommendations.
4. Higher sales per call does not prove that more calls will cause more prescriptions.
5. Weighted scores are transparent *assumptions*, not facts. Validate sensitivity to alternative weights and stakeholder priorities.

**Decision:** Review the top-ranked combinations as *hypotheses*. Do not recommend real commercial expansion or any patient-level intervention based on this fictional dataset alone.
