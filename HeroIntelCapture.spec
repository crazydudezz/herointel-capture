# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_all

# Anchor every path on the spec's directory so absolute paths are used regardless
# of where pyinstaller is invoked from.
SPEC_DIR = Path(os.path.dirname(os.path.abspath(SPEC)))
ICON_PNG = SPEC_DIR / "icon.png"
ICON_ICO = SPEC_DIR / "icon.ico"
WORDMARK = SPEC_DIR / "wordmark.png"

print(f"[spec] icon.png exists: {ICON_PNG.exists()}  ({ICON_PNG})")
print(f"[spec] icon.ico exists: {ICON_ICO.exists()}  ({ICON_ICO})")
print(f"[spec] wordmark.png exists: {WORDMARK.exists()}  ({WORDMARK})")

datas = []
binaries = []
hiddenimports = ['plyer.platforms.win.notification', 'keyring.backends.Windows', 'win32timezone', 'customtkinter']
tmp_ret = collect_all('pystray')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('keyboard')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('customtkinter')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

# Bundle the icon files so _MEIPASS resolution at runtime works.
if ICON_PNG.exists():
    datas.append((str(ICON_PNG), '.'))
if ICON_ICO.exists():
    datas.append((str(ICON_ICO), '.'))
if WORDMARK.exists():
    datas.append((str(WORDMARK), '.'))


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='HeroIntelCapture',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(ICON_ICO) if ICON_ICO.exists() else None,
)
