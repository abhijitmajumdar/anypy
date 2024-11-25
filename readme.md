# anypy

## Run (no installation)
- Zero dependency app
  ```bash
  curl -s https://github.com/abhijitmajumdar/anypy/releases/download/20241125.1531/anypy | bash -s -- 3.11.10
  # Or run this to see supported versions
  curl -s https://github.com/abhijitmajumdar/anypy/releases/download/20241125.1531/anypy | bash -s -- -h
  ```
- If you have Python3.7+
  ```bash
  curl -s https://raw.githubusercontent.com/abhijitmajumdar/anypy/refs/heads/main/anypy.py | python3 - 3.11.10
  # Or run this to see supported versions
  curl -s https://raw.githubusercontent.com/abhijitmajumdar/anypy/refs/heads/main/anypy.py | python3 - -h
  ```

## Install standalone app
```bash
mkdir -p ~/.local/bin/
curl https://github.com/abhijitmajumdar/anypy/releases/download/20241125.1531/anypy -o ~/.local/bin/anypy
chmod +x ~/.local/bin/anypy
```
