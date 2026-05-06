# Reviewer #1 - Comment 1: Boride Subset Validation

To address the reviewer concern regarding the applicability of the generalized GATGNN model to boride systems, we performed an additional validation using only held-out boride compositions from the evaluation results. Boride entries were identified from the `chemical_formula_structural` field by selecting compositions containing elemental B.

The purpose of this analysis is not to develop a boride-specific model, but to verify whether the generalized ceramic model trained on a broad ceramic dataset remains transferable to boride chemistry without system-specific retraining.

| Property | Subset | N | MAE | RMSE | R2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Bulk modulus | All held-out | 510 | 6.99 | 12.97 | 0.966 |
| Bulk modulus | Boride held-out | 43 | 4.53 | 6.49 | 0.971 |
| Young's modulus | All held-out | 510 | 16.66 | 30.82 | 0.949 |
| Young's modulus | Boride held-out | 43 | 18.53 | 28.51 | 0.918 |

These results indicate that the generalized model maintains robust predictive performance for the held-out boride subset. In particular, the boride subset shows comparable or better error metrics for bulk modulus, and still retains strong correlation for Young's modulus. This supports the transferability of the generalized ceramic ML framework to boride systems, including high-entropy borides, without requiring boride-specific model retraining.
