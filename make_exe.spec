from kivymd import hooks_path as kivymd_hooks_path
from kivy_deps import sdl2, glew
from PyInstaller.building.build_main import *
from PyInstaller.utils.hooks import collect_submodules, collect_data_files
import sys
import os

path = os.path.abspath(".")


hiddenimports = collect_submodules('mediapipe')
datas = collect_data_files('mediapipe', subdir=None, include_py_files=True)

a = Analysis(
    ["main.py"],
    pathex=[path],
    binaries=[],
    datas=datas+[("main.py", "."), ("*.kv", "."), ("assets\\", "assets\\"), ("widgets\\*.py", "widgets\\"), ("screens\\*.py",
                                                                                                             "screens\\"), ("utils\\", "utils\\"), ("handtracking\\*.py", "handtracking\\")],
    hiddenimports=hiddenimports+['pygrabber.dshow_graph','plyer'
    ],
    hookspath=[kivymd_hooks_path],
    runtime_hooks=[],
    excludes=['mediapipe.examples',
              "pandas",
              "jedi",
              "scipy",
              "PIL",
              ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)
a.binaries = a.binaries - \
    TOC([('opencv_world3410.dll', None, None),
         ('cv2\\opencv_videoio_ffmpeg430_64.dll', None, None),
         ('mfc140u.dll',None,None),
         ])
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    debug=False,
    strip=False,
    upx=True,
    name="Virtual Music",
    icon='assets/icons/app_icon.ico',
    console=False,
)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Virtual Music')
