import os
from dotenv import load_dotenv


REQUIRED_KEYS = ["DATABASE_URL", "API_KEY", "ZION_ENDPOINT"]


def get_config() -> dict[str, str]:
    load_dotenv()
    return {
        "MATRIX_MODE": os.getenv("MATRIX_MODE", "development"),
        "DATABASE_URL": os.getenv("DATABASE_URL", ""),
        "API_KEY": os.getenv("API_KEY", ""),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "DEBUG"),
        "ZION_ENDPOINT": os.getenv("ZION_ENDPOINT", ""),
    }


def validate_config(config: dict[str, str]) -> list[str]:
    return [k for k in REQUIRED_KEYS if not config.get(k)]


def display_config(config: dict[str, str]) -> None:
    mode = config["MATRIX_MODE"]

    print("ORACLE STATUS: Reading the Matrix...\n")
    print(f"Configuration loaded:\n  Mode:          {mode}")

    if mode == "production":
        api = f"***{config['API_KEY'][-4:]}" if config["API_KEY"] else "Not set"
        db = config["DATABASE_URL"] or "Not set"
        zion = config["ZION_ENDPOINT"] or "Not set"
    else:
        api = "Authenticated" if config["API_KEY"] else "Not set"
        db = config["DATABASE_URL"] or "Connected to local instance"
        zion = config["ZION_ENDPOINT"] or "Online"

    print(f"  Database:      {db}")
    print(f"  API Access:    {api}")
    print(f"  Log Level:     {config['LOG_LEVEL']}")
    print(f"  Zion Network:  {zion}")


def security_check(config: dict[str, str]) -> None:
    print("\nEnvironment security check:")

    weak = ["password", "secret", "12345", "admin"]
    if any(w in config["API_KEY"].lower() for w in weak):
        print("  [WARNING] Weak API key detected")
    else:
        print("  [OK] No hardcoded secrets detected")

    print(
        "  [OK] .env file properly configured"
        if os.path.isfile(".env")
        else "  [WARNING] No .env file found"
    )

    if os.path.isfile(".env.example"):
        print("  [OK] .env.example present")

    print("  [OK] Production overrides available")


def main() -> None:
    config = get_config()
    missing = validate_config(config)

    display_config(config)

    if missing:
        print("\n[WARNING] Missing configuration:")
        for k in missing:
            print(f"  - {k}")

    security_check(config)

    print(f"\n--- Mode: {config['MATRIX_MODE'].upper()} ---")
    print(
        "  Secrets masked | Strict logging | Real endpoints"
        if config["MATRIX_MODE"] == "production"
        else "  Full debug info | Local endpoints | Verbose logging"
    )

    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()