import sys
import importlib


def check_dependencies() -> dict[str, str | None]:
    status: dict[str, str | None] = {}
    for pkg in ["pandas", "numpy", "matplotlib"]:
        try:
            mod = importlib.import_module(pkg)
            status[pkg] = getattr(mod, "__version__", "unknown")
        except ImportError:
            status[pkg] = None
    return status


def show_dependency_status(status: dict[str, str | None]) -> bool:
    print("LOADING STATUS: Loading programs...\n")
    print("Checking dependencies:")

    descriptions: dict[str, str] = {
        "pandas": "Data manipulation ready",
        "numpy": "Numerical computation ready",
        "matplotlib": "Visualization ready",
    }

    all_ok = True
    for pkg, version in status.items():
        if version:
            desc = descriptions.get(pkg, "Ready")
            print(f"  [OK] {pkg} ({version}) - {desc}")
        else:
            print(f"  [MISSING] {pkg}")
            print(f"    pip:    pip install {pkg}")
            print(f"    poetry: poetry add {pkg}")
            all_ok = False

    print()
    return all_ok


def show_install_instructions() -> None:
    print("Install all dependencies with:")
    print("  pip:    pip install -r requirements.txt")
    print("  poetry: poetry install")
    sys.exit(1)


def compare_managers(status: dict[str, str | None]) -> None:
    print("\n--- pip vs Poetry ---")
    print(f"{'Package':<15} {'Version':<15} {'Manager'}")
    print("-" * 50)
    for pkg, version in status.items():
        v = version if version else "not installed"
        print(f"{pkg:<15} {v:<15} pip / poetry")
    print("\npip uses requirements.txt")
    print("poetry uses pyproject.toml")


def run_analysis() -> None:
    import numpy as np  # type: ignore
    import pandas as pd  # type: ignore
    import matplotlib.pyplot as plt  # type: ignore

    print("Analyzing Matrix data...")

    rng = np.random.default_rng(seed=42)
    n_points = 1000
    signal = rng.normal(loc=0.0, scale=1.0, size=n_points).cumsum()
    noise = rng.normal(loc=0.0, scale=0.5, size=n_points)

    print(f"Processing {n_points} data points...")

    df = pd.DataFrame({
        "time": np.arange(n_points),
        "signal": signal,
        "noise": noise,
    })

    print("Generating visualization...")

    plt.figure(figsize=(10, 5))
    plt.plot(df["time"], df["signal"], color="blue", linewidth=1)
    plt.fill_between(
        df["time"],
        df["signal"] - df["noise"],
        df["signal"] + df["noise"],
        alpha=0.2,
        color="cyan",
    )
    plt.title("Matrix Signal Analysis")
    plt.xlabel("Time")
    plt.ylabel("Signal")
    plt.tight_layout()
    plt.savefig("matrix_analysis.png", dpi=150)
    plt.close()

    print("\nAnalysis complete!")
    print("Results saved to: matrix_analysis.png")


def main() -> None:
    status = check_dependencies()
    all_ok = show_dependency_status(status)

    if not all_ok:
        show_install_instructions()

    run_analysis()
    compare_managers(status)


if __name__ == "__main__":
    main()
