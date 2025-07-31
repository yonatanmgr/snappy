# 📸 snappy

snappy is a lightweight Python script (`snap.py`) that takes a screenshot of a webpage with custom query parameters and screen resolution using [Playwright](https://playwright.dev/python/).

It is perfect for automated snapshots of dashboards, displays, or any URL with dynamic query parameters.

---

## 🚀 Features

- Load URL and query parameters from a YAML config file
- Custom screen resolution (headless browser)
- Automatically waits for network to be idle + an extra second
- Replaces the previous screenshot only after a new one is successfully captured
- Configurable screenshot output file name via command-line argument (defaults to `screenshot.png`)
- Output file is ignored by Git

---

## 🧱 Requirements

- Python 3.8+
- Dependencies:
  ```bash
  pip install -r requirements.txt
  playwright install
  ```

---

## 🔧 Usage

1. Create a `config.yaml` file (not checked into Git). For example:

   ```yaml
   url: "https://example.com/"
   params:
     my_param_1: "a_string"
     my_param_2: "true"
     my_param_3: 123
   screen:
     width_px: 800
     height_px: 480
   delay_ms: 500
   bitmap: false
   ```

2. Run the script:

   ```bash
   python snap.py
   ```

   To specify a custom screenshot file name:

   ```bash
   python snap.py --screenshot-path custom_screenshot.png
   ```

3. Output: A fresh screenshot (e.g., `screenshot.png` or specified file name) is saved in the working directory.

---

## 📁 Project Structure

```
snappy/
├── snap.py           # Main script
├── .gitignore       # Ignores screenshots and config
├── README.md        # This file
├── config.yaml      # Your personal config (ignored by Git)
└── screenshot.png   # Auto-generated (ignored by Git)
```

---

## 📌 Notes

- `config.yaml` and screenshot files (e.g., `screenshot.png` or custom names) are excluded from version control via `.gitignore`.
- If the specified screenshot file already exists, it will only be deleted after a new screenshot is successfully captured.
- The output format (.png or .bmp), screen size and screenshot delay are customizable in `config.yaml`.
- The screenshot file name can be customized via the `--screenshot-path` command-line argument; defaults to `screenshot.png` if not specified.

---

## 📄 License

MIT © Yonatan Magier