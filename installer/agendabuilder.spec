# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

datas = [
    ('../icons', 'icons'),
    # might need to add fonts?
]

hiddenimports = [
    #'logging',
    #'logging.config',
    'reportlab',
    #'reportlab.graphics',
    #'reportlab.graphics.barcode.common',
    #'reportlab.graphics.barcode.code128',
    #'reportlab.graphics.barcode.code93',
    #'reportlab.graphics.barcode.code39',
    #'reportlab.graphics.barcode.lto',
    #'reportlab.graphics.barcode.qr',
    #'reportlab.graphics.barcode.usps',
    #'reportlab.graphics.barcode.usps4s',
    #'reportlab.graphics.barcode.eanbc',
    #'reportlab.graphics.barcode.ecc200datamatrix',
    #'reportlab.graphics.barcode.fourstate',
]


a = Analysis(
    ['agenda-builder.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='agendabuilder',
    debug=False,
    bootloader_ignore_signals=False,
    icon=os.path.join("../icons/agendabuilder.ico"),
    strip=False,
    upx=True,
    console=True
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='agendabuilder'
)
