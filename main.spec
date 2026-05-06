# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/main.py'],
    pathex=['src'],
    binaries=[],
    datas=[('web', 'web')],
    hiddenimports=['webview', 'webview.platforms.winforms', 'clr', 'pythonnet'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PIL', 'Pillow',
        'numpy', 'scipy', 'pandas', 'matplotlib',
        'unittest', 'doctest', 'pdb', 'difflib',
        'tkinter', '_tkinter',
        'gevent', 'greenlet', 'zope', 'zope.interface', 'zope.event',
        'psutil',
    ],
    noarchive=False,
    optimize=2,
)

# Keep only Windows x64 pywebview runtime assets in onefile bundle.
def _keep_data(entry):
    name = entry[0].replace('\\', '/').lower()
    drop_markers = [
        'webview/lib/pywebview-android.jar',
        'webview/lib/runtimes/win-arm64/',
        'webview/lib/runtimes/win-x86/',
    ]
    return not any(marker in name for marker in drop_markers)
a.datas = [entry for entry in a.datas if _keep_data(entry)]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ValoGuard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[
        'vcruntime140.dll',
        'python3*.dll',
        'Microsoft.Web.WebView2.WinForms.dll',
        'Microsoft.Web.WebView2.Core.dll',
        'WebBrowserInterop.x86.dll',
        'WebBrowserInterop.x64.dll',
        'Python.Runtime.dll',
    ],
    runtime_tmpdir=None,
    console=False,
    icon='assets/icon.ico',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
