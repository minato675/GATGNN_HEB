from pathlib import Path
import warnings

from chgnet.model import CHGNet, StructOptimizer
from pymatgen.core import Structure


warnings.filterwarnings(
    "ignore",
    message=r"logm result may be inaccurate.*",
    category=RuntimeWarning,
)

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "Element"
OUTPUT_DIR = BASE_DIR / "opt_cif"


def optimize_structure(file_path: Path, output_dir: Path) -> None:
    structure = Structure.from_file(file_path)

    unrelaxed_structure = structure.copy()
    unrelaxed_structure.apply_strain([0.1, 0.1, 0.1])
    unrelaxed_structure.perturb(0.005)

    result = relaxer.relax(unrelaxed_structure, verbose=True)
    optimized_structure = result["final_structure"]

    output_file = output_dir / file_path.name
    optimized_structure.to(fmt="cif", filename=str(output_file))
    print(f"Saved optimized CIF: {output_file}")


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    chgnet = CHGNet.load()
    relaxer = StructOptimizer(model=chgnet, optimizer_class="BFGS")

    cif_files = sorted(INPUT_DIR.glob("*.cif"))
    if not cif_files:
        raise FileNotFoundError(f"No CIF files found in {INPUT_DIR}")

    for file_path in cif_files:
        print(f"Processing: {file_path.name}")
        optimize_structure(file_path, OUTPUT_DIR)
        print(f"Done: {file_path.name}\n")
