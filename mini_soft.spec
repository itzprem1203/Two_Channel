# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/Users/itzpr.DESKTOP-EUQC32B/Desktop/mini_soft/mini_soft/manage.py'],
    pathex=[],
    binaries=[],
    datas=[('mini_soft/app/templates/app', 'mini_soft/app/templates/app'), ('mini_soft/app/static', 'mini_soft/app/static'), ('mini_soft/app/views', 'mini_soft/app/views'), ('mini_soft/staticfiles', 'mini_soft/staticfiles'), ('mini_soft/app/migrations', 'mini_soft/app/migrations'), ('mini_soft/asgi.py', 'mini_soft/asgi.py'), ('mini_soft/settings.py', 'mini_soft/settings.py')],
    hiddenimports=['whitenoise.middleware', 'serial.tools.list_ports', 'pyserial', 'serial', 'kaleido', 'whitenoise', 'channels_redis.core', 'channels_redis', 'redis', 'django.core.asgi', 'django.core.wsgi', 'mini_soft.asgi'],
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
    name='mini_soft',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\itzpr.DESKTOP-EUQC32B\\Desktop\\mini_soft\\mini_soft\\app\\static\\images\\Gauge.ico'],
)
