# -*- mode: python ; coding: utf-8 -*-
"""
接亲小游戏 - PyInstaller macOS 打包配置
在 Mac 上运行: pyinstaller jieqin_game_macos.spec

依赖安装:
    pip install pyinstaller PyQt6 tinycc

构建:
    pyinstaller jieqin_game_macos.spec
    # 产物: dist/jieqin_game.app
"""
from pathlib import Path
from PyInstaller.utils.hooks import collect_all

# ── 路径配置 ─────────────────────────────────────────────
# 获取 spec 文件所在目录（即项目根目录）
SPEC_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SPEC_DIR

# ── Web 静态资源 ──────────────────────────────────────────
web_assets = [
    'index.html',
    'game.js',
    'style.css',
    'qwebchannel.js',
]

web_datas = []
for f in web_assets:
    p = PROJECT_ROOT / f
    if p.exists():
        web_datas.append((str(p), '.'))
    else:
        print(f"[WARN] 缺少资源文件: {p}")

# ── 图片资源 ──────────────────────────────────────────────
for ext in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
    # 根目录的图片
    for img_path in PROJECT_ROOT.glob(f'*.{ext}'):
        web_datas.append((str(img_path), '.'))
    # imgs 子目录的图片
    for img_path in PROJECT_ROOT.glob(f'imgs/*.{ext}'):
        web_datas.append((str(img_path), 'imgs'))

# ── PyQt6 ────────────────────────────────────────────────
pyqt6_all = collect_all('PyQt6')
pyqt6_datas = list(pyqt6_all[0])
pyqt6_binaries = list(pyqt6_all[1])
pyqt6_hiddenimports = list(pyqt6_all[2])

# ── TinyCC ───────────────────────────────────────────────
tinycc_all = collect_all('tinycc')
tinycc_datas = list(tinycc_all[0])
tinycc_binaries = list(tinycc_all[1])
tinycc_hiddenimports = list(tinycc_all[2])

# 额外添加 tinycc/lib 目录
try:
    import tinycc as _tc
    tinycc_base = Path(_tc.__file__).parent
    lib_dir = tinycc_base / 'lib'
    if lib_dir.exists():
        tinycc_datas.append((str(lib_dir), 'tinycc/lib'))
except ImportError:
    pass

# ── 隐藏导入 ──────────────────────────────────────────────
hiddenimports = [
    # PyQt6 核心模块
    'PyQt6',
    'PyQt6.QtWidgets',
    'PyQt6.QtWebEngineWidgets',
    'PyQt6.QtWebChannel',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.sip',
    # tinycc
    'tinycc',
    'tinycc.compile',
    # PyQt6 子模块
    'PyQt6.QtWebEngineCore',
    'PyQt6.QtWebEngine',
    'PyQt6.QtWebEngineWidgets',
    'PyQt6.QtNetwork',
    'PyQt6.QtOpenGLWidgets',
    'PyQt6.QtOpenGL',
    'PyQt6.QtPrintSupport',
]
hiddenimports += pyqt6_hiddenimports
hiddenimports += tinycc_hiddenimports

# ── 数据文件汇总 ──────────────────────────────────────────
datas = web_datas + pyqt6_datas + tinycc_datas

# ── 二进制文件汇总 ────────────────────────────────────────
binaries = pyqt6_binaries + tinycc_binaries

# ── 入口脚本 ─────────────────────────────────────────────
entry_script = str(PROJECT_ROOT / 'py' / 'main.py')

# ── Analysis ─────────────────────────────────────────────
a = Analysis(
    [entry_script],
    pathex=[str(PROJECT_ROOT)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib', 'numpy', 'pandas', 'scipy',
        'PIL', 'Pillow', 'tkinter', 'PySimpleGUI',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# ── PYZ ───────────────────────────────────────────────────
pyz = PYZ(a.pure, cipher=None)

# ── EXE ───────────────────────────────────────────────────
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='jieqin_game',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,          # macOS 下通常不用 UPX
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,      # 无控制台窗口（GUI 应用）
    disable_windowed_traceback=False,
    argv_emulation=True,  # macOS 专用：支持拖拽文件等
    target_arch=None,   # None = 当前架构，也可设为 'universal2'
    codesign_identity=None,
    entitlements_file=None,
    # icon='app.icns',  # 如果有 icns 图标，取消注释并指定路径
)

# ── macOS App Bundle ─────────────────────────────────────
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='jieqin_game',
)
