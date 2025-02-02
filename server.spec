# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['server.py'],  # Replace with your main script name
    pathex=[],
    binaries=[],
    datas=[
        ('static', 'static'),  # Include static directory
        ('version.txt', '.'),
    ],
    hiddenimports=[
        'uvicorn.logging', 
        'uvicorn.protocols', 
        'uvicorn.lifespan.on', 
        'uvicorn.lifespan.off',
        'cycler',
        'matplotlib',
        'matplotlib.backends.backend_tkagg',
        'numpy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pytest', '_pytest', 'pip', 'setuptools'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)