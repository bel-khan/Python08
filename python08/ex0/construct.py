import os
import sys
import site


def is_virtual_env() -> bool:
    return (
        hasattr(sys, "real_prefix")
        or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)
     )


def get_venv_name() -> str | None:
    venv_path = os.environ.get("VIRTUAL_ENV")
    if venv_path:
        return os.path.basename(venv_path)
    return None


def get_package_location() -> str:
    packages = site.getsitepackages()
    return packages[0] if packages else "Unknown"


def show_outside_venv() -> None:
    print("MATRIX STATUS: You're still plugged in\n")
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected\n")
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.\n")
    print("To enter the construct, run:")
    print("  python -m venv matrix_env")
    print("  source matrix_env/bin/activate   # On Unix")
    print("  matrix_env\\Scripts\\activate      # On Windows")
    print("\nThen run this program again.")


def show_inside_venv() -> None:
    venv_name = get_venv_name() or "unknown"
    venv_path = os.environ.get("VIRTUAL_ENV", "Unknown")
    package_path = get_package_location()

    print("MATRIX STATUS: Welcome to the construct\n")
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {venv_name}")
    print(f"Environment Path: {venv_path}\n")
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting the global system.\n")
    print(f"Package installation path:\n{package_path}")


def main() -> None:
    if is_virtual_env():
        show_inside_venv()
    else:
        show_outside_venv()


if __name__ == "__main__":
    main()
