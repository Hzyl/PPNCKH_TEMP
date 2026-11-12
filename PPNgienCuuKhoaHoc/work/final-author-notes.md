# Final proposal author notes

Content: `final_sections.json`; all sections 1–16 follow the official template order. Five names and IDs are included. Proposed responsibilities, coordinator, 12-week schedule, products and budget are explicitly prospective. The administrative supervisor/contact/approval fields are not fabricated.

## Substantive integration notes

- Main comparison deliberately uses a conservative eight-variable T0 whitelist. T1 adds six first-semester variables. No second-semester, financial-status, sensitive demographic, family or macroeconomic predictors enter the principal comparison. This narrower configuration is disclosed; do not label it all available enrollment information.
- This is a retrospective information-set comparison. The public table does not establish the landmark risk set at the end of semester one or exact dropout dates. Do not claim prospective early-warning validity.
- Enrolled remains a separate primary class. The secondary binary model uses Dropout versus not labeled Dropout, never Dropout versus confirmed graduates.
- Primary model selection uses five-fold CV only within training; validation chooses binary operational thresholds. Final models remain trained on training only, so the validation threshold corresponds to the same model. Test data are not used for selection.
- Paired stratified test bootstrap estimates conditional test-sample uncertainty, not training or external-generalization uncertainty.
- Only sources [1] and [2] are relied on. A verified domestic literature review is not supplied; text explicitly acknowledges this gap and schedules further searching instead of inventing Vietnamese studies. Root may add a verified domestic primary source if available.
- Two current-UCI features absent from the paper's column count are disclosed. Data counts are descriptive facts, not invented predictive performance.
- The JSON includes prospective prose for all formal sections, but do not reproduce administrative integration explanations verbatim inside signature fields. Keep official signature areas unsigned.
- Root must visually inspect the final integrated template and ensure academic references appear under section 8 or an explicit references section as appropriate. No Word operations or other files were touched by this author.

## Validation

Validated JSON parsing, presence of all 16 sections, supported block types and table widths; JavaScript wrapper passed `node --check --input-type=module`.
