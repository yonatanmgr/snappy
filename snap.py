import time
import yaml
import argparse
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

# === Configuration ===
YAML_CONFIG_FILE = "config.yaml"
DEFAULT_SCREENSHOT_PATH = Path("screenshot.png")
DEFAULT_DELAY_MS = 1000

def timestamp():
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")


def load_config(yaml_file):
    try:
        with open(yaml_file, 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        raise ValueError(f"Config file '{yaml_file}' not found.")

    if not isinstance(config, dict):
        raise ValueError("Config file must contain a valid YAML object.")

    if "url" not in config or not isinstance(config["url"], str):
        raise ValueError("Missing or invalid 'url' in config.yaml.")

    screen = config.get("screen")
    if not isinstance(screen, dict):
        raise ValueError("Missing 'screen' section in config.yaml.")

    width = screen.get("width_px")
    height = screen.get("height_px")

    if not isinstance(width, int) or not isinstance(height, int):
        raise ValueError("Screen width and height must be integers (width_px, height_px).")

    # Validate delay_ms if present
    delay_ms = config.get("delay_ms", DEFAULT_DELAY_MS)
    if not isinstance(delay_ms, int) or delay_ms < 0:
        raise ValueError("delay_ms must be a non-negative integer.")

    return config


def build_url(config):
    base_url = config["url"]
    params = config.get("params", {})
    if params:
        query = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{base_url}?{query}"
    return base_url


def main(screenshot_path=DEFAULT_SCREENSHOT_PATH):
    config = load_config(YAML_CONFIG_FILE)
    url = build_url(config)
    width = config["screen"]["width_px"]
    height = config["screen"]["height_px"]
    delay_ms = config.get("delay_ms", DEFAULT_DELAY_MS)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": width, "height": height})
        page = context.new_page()

        page.goto(url, wait_until="networkidle")

        # Convert milliseconds to seconds and wait
        delay_seconds = delay_ms / 1000.0
        time.sleep(delay_seconds)

        page.screenshot(path=str(screenshot_path))
        print(f"{timestamp()} Screenshot saved to {screenshot_path} after {delay_ms}ms delay")

        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Take a screenshot of a webpage.")
    parser.add_argument(
        "--screenshot-path",
        type=Path,
        default=DEFAULT_SCREENSHOT_PATH,
        help="Path to save the screenshot (default: screenshot.png)",
    )
    args = parser.parse_args()

    try:
        main(args.screenshot_path)
    except Exception as e:
        print(f"{timestamp()} Error: {e}")
        exit(1)