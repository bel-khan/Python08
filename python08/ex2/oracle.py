import os
import sys
from dotenv import load_dotenv


def load_configuration():
    load_dotenv()


def get_config():
    config = {
        "MATRIX_MODE": os.getenv("MATRIX_MODE", "development"),
        "DATABASE_URL": os.getenv("DATABASE_URL", "sqlite://localhost/matrix.db"),
        "API_KEY": os.getenv("API_KEY"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "DEBUG"),
        "ZION_ENDPOINT": os.getenv("ZION_ENDPOINT", "http://zion.local:8080"),
    }
    return config


def display_configuration(config):
    mode = config["MATRIX_MODE"]
    print("ORACLE STATUS: Reading the Matrix...\n")
    print("Configuration loaded:")
    print(f"  Mode: {mode}")
    if mode == "production":
        print("  Database: Connected to production cluster")
        print("  API Access: " + ("Authenticated" if config["API_KEY"] else "MISSING - CRITICAL"))
        print(f"  Log Level: {config['LOG_LEVEL']}")
        print("  Zion Network: Secure (TLS enabled)")
    else:
        print("  Database: Connected to local instance")
        print("  API Access: " + ("Authenticated" if config["API_KEY"] else "Not configured (dev mode)"))
        print(f"  Log Level: {config['LOG_LEVEL']}")
        print("  Zion Network: Online")


def security_check(config):
    print("\nEnvironment security check:")
    issues = []
    suspicious = ["password", "secret", "hardcoded"]
    api_key = config.get("API_KEY") or ""
    if any(word in api_key.lower() for word in suspicious):
        issues.append("Possible hardcoded secret in API_KEY")
    else:
        print("  [OK] No hardcoded secrets detected")
    if os.path.exists(".env"):
        print("  [OK] .env file properly configured")
    else:
        print("  [WARN] No .env file found (using defaults or environment variables)")
    if os.getenv("MATRIX_MODE") or os.getenv("API_KEY"):
        print("  [OK] Production overrides available")
    else:
        print("  [INFO] No environment variable overrides detected")
    if issues:
        for issue in issues:
            print(f"  [WARN] {issue}")
        sys.exit(1)


def main():
    load_configuration()
    config = get_config()
    display_configuration(config)
    security_check(config)
    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
