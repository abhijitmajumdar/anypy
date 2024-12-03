# anypy

## Run (requires Python3.7+ installed)
```bash
curl -s https://raw.githubusercontent.com/abhijitmajumdar/anypy/refs/heads/main/anypy.py | python3 - 3.11.10
# Or run this to see supported versions
curl -s https://raw.githubusercontent.com/abhijitmajumdar/anypy/refs/heads/main/anypy.py | python3 - -h
```

## Install standalone app
```bash
mkdir -p ~/.local/bin/
curl -L https://github.com/abhijitmajumdar/anypy/releases/download/20241203.1504/anypy -o ~/.local/bin/anypy
chmod +x ~/.local/bin/anypy
```

Make sure `~/.local/bin` is in in your `$PATH`. Now run it from any terminal as
```bash
anypy 3.11.10
# Or run this to see supported versions
anypy -h
```
