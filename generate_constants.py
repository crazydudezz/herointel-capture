"""Generate _constants.py and icon.png from the parent web app's .env.local + public/.

Run from the herointel-capture directory:
    python generate_constants.py
"""

import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
ENV_FILE = PROJECT_ROOT / ".env.local"
LOGO_SOURCE = PROJECT_ROOT / "public" / "logo4-square.png"
WORDMARK_SOURCE = PROJECT_ROOT / "public" / "logo3.png"
ICON_DEST = HERE / "icon.png"
ICO_DEST = HERE / "icon.ico"
WORDMARK_DEST = HERE / "wordmark.png"
CONSTANTS_DEST = HERE / "_constants.py"

REQUIRED = {
    "FIREBASE_API_KEY":        "NEXT_PUBLIC_FIREBASE_API_KEY",
    "FIREBASE_PROJECT_ID":     "NEXT_PUBLIC_FIREBASE_PROJECT_ID",
    "FIREBASE_STORAGE_BUCKET": "NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET",
    "WEB_APP_URL":             "NEXT_PUBLIC_APP_URL",
}


def parse_env(path: Path) -> dict:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        v = v.strip()
        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
            v = v[1:-1]
        out[k.strip()] = v
    return out


def main() -> int:
    if not ENV_FILE.exists():
        print(f"[generate_constants] {ENV_FILE} not found")
        return 1
    env = parse_env(ENV_FILE)

    values = {}
    missing = []
    for const, env_key in REQUIRED.items():
        v = env.get(env_key, "").strip()
        if not v:
            missing.append(env_key)
        values[const] = v
    if missing:
        print("[generate_constants] missing env vars: " + ", ".join(missing))
        return 1

    body = (
        '"""Auto-generated from ../.env.local. Do not edit by hand."""\n\n'
        + "\n".join(f'{k} = "{v}"' for k, v in values.items())
        + "\n"
    )
    CONSTANTS_DEST.write_text(body, encoding="utf-8")
    print(f"[generate_constants] wrote {CONSTANTS_DEST}")

    if LOGO_SOURCE.exists():
        shutil.copyfile(LOGO_SOURCE, ICON_DEST)
        print(f"[generate_constants] copied {LOGO_SOURCE.name} ->{ICON_DEST.name}")
        try:
            from PIL import Image
            img = Image.open(LOGO_SOURCE).convert("RGBA")
            img.save(ICO_DEST, format="ICO",
                     sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
            print(f"[generate_constants] wrote {ICO_DEST.name} (multi-size)")
        except Exception as e:
            print(f"[generate_constants] WARNING: could not generate icon.ico: {e}")
    else:
        print(f"[generate_constants] WARNING: {LOGO_SOURCE} not found; tray will use fallback icon")

    if WORDMARK_SOURCE.exists():
        shutil.copyfile(WORDMARK_SOURCE, WORDMARK_DEST)
        print(f"[generate_constants] copied {WORDMARK_SOURCE.name} ->{WORDMARK_DEST.name}")
    else:
        print(f"[generate_constants] WARNING: {WORDMARK_SOURCE} not found; in-app logo will be hidden")
    return 0


if __name__ == "__main__":
    sys.exit(main())
