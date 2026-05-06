import re
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


RESULT_FILES = {
    "new_bulk-modulus": Path("RESULTS/new_bulk-modulus_results.csv"),
    "new_Youngs-modulus": Path("RESULTS/new_Youngs-modulus_results.csv"),
}
OUT_DIR = Path("RESULTS/boride_analysis")
ELEMENT_PATTERN = re.compile(r"([A-Z][a-z]?)(?:[0-9.]+)?")


def contains_boron(formula: str) -> bool:
    elements = ELEMENT_PATTERN.findall(str(formula))
    return "B" in elements


def metrics_frame(property_name: str, df: pd.DataFrame, subset_name: str) -> dict:
    measured_col = f"Measured {property_name}"
    predicted_col = f"Predicted {property_name}"
    y_true = df[measured_col].astype(float)
    y_pred = df[predicted_col].astype(float)

    return {
        "property": property_name,
        "subset": subset_name,
        "n": len(df),
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": mean_squared_error(y_true, y_pred) ** 0.5,
        "R2": r2_score(y_true, y_pred),
    }


def save_parity_plot(property_name: str, df: pd.DataFrame, out_path: Path) -> None:
    measured_col = f"Measured {property_name}"
    predicted_col = f"Predicted {property_name}"
    y_true = df[measured_col].astype(float)
    y_pred = df[predicted_col].astype(float)

    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    padding = (max_val - min_val) * 0.06 if max_val > min_val else 1.0
    lo = min_val - padding
    hi = max_val + padding

    plt.figure(figsize=(5.2, 5.0), dpi=180)
    plt.scatter(y_true, y_pred, s=34, alpha=0.78, edgecolors="black", linewidths=0.35)
    plt.plot([lo, hi], [lo, hi], color="black", linestyle="--", linewidth=1.2)
    plt.xlim(lo, hi)
    plt.ylim(lo, hi)
    plt.xlabel(f"DFT {property_name}")
    plt.ylabel(f"Predicted {property_name}")
    plt.title(f"Boride held-out subset ({property_name})")
    plt.grid(True, alpha=0.25)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summaries = []

    for property_name, result_path in RESULT_FILES.items():
        df = pd.read_csv(result_path)
        boride_df = df[df["chemical_formula_structural"].map(contains_boron)].copy()

        boride_csv = OUT_DIR / f"{property_name}_boride_subset.csv"
        boride_df.to_csv(boride_csv, index=False)

        summaries.append(metrics_frame(property_name, df, "all_held_out"))
        summaries.append(metrics_frame(property_name, boride_df, "boride_held_out"))

        plot_path = OUT_DIR / f"{property_name}_boride_parity.png"
        save_parity_plot(property_name, boride_df, plot_path)

    summary_df = pd.DataFrame(summaries)
    summary_df.to_csv(OUT_DIR / "boride_metrics_summary.csv", index=False)
    print(summary_df.to_string(index=False))
    print(f"\nSaved analysis files to: {OUT_DIR}")


if __name__ == "__main__":
    main()
