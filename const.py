
import os, base64
import subprocess

DEBUG = True

ANDROID_DIR = 'android/'
APKTOOL_DIR = ANDROID_DIR + 'apktool/'
SIGNAPK_DIR = ANDROID_DIR + 'signapk/'
ANDROID_FULL_DIR = os.path.abspath(ANDROID_DIR).replace('\\', '/') + '/'
try:
    JAVA_PATH = os.environ['JAVA_HOME']
    JAVA_INSTALLED = True
except KeyError:
    JAVA_PATH = ''
    JAVA_INSTALLED = False

JAVA_VERSION = None
if JAVA_INSTALLED and not JAVA_VERSION:
    JAVA_VERSION = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT)

try:
    with open(SIGNAPK_DIR + 'java.txt', 'r') as f:
        JAVA9 = bool(int(f.read(1))) # 0 or 1, default: 0
except ValueError:
    JAVA9 = False

def _android_signapk(_in, _out):
    os.chdir(ANDROID_DIR + 'signapk')
    os.system(f'signapk "{_in}" "{_out}"')
    os.chdir('../../')

ANDROID_SIGNAPK = _android_signapk

def _android_apktool1(apkname):
    os.chdir(ANDROID_DIR + 'apktool')
    os.system(f'apktool d {apkname}')
    os.chdir('../../')

def _android_apktool2(dirname):
    os.chdir(ANDROID_DIR + 'apktool')
    os.system(f'apktool b {dirname}')
    os.chdir('../../')

ANDROID_APKTOOL = (
    lambda apkname: _android_apktool1(apkname),
    lambda dirname: _android_apktool2(dirname)
)

base64_encode = lambda string: base64.urlsafe_b64encode(string.encode()).decode()

ROBTOP = 'www.boomlings.com/database'
ROBTOP_BASE64 = base64_encode('http://'+ROBTOP)

ROBTOP_ANDROID = (
    'Lcom/robtopx/geometryjump',
    'com.robtopx.geometryjump'
)

ROBTOP_ANDROID_REPLACE = lambda robtopx, geometryjump: (
    ROBTOP_ANDROID[0].replace('robtopx', robtopx).replace('geometryjump', geometryjump),
    ROBTOP_ANDROID[1].replace('robtopx', robtopx).replace('geometryjump', geometryjump)
)

URL_LENGHT = len(ROBTOP)
URL_LENGHT_HTTP = len('http://') + URL_LENGHT
URL_LENGHT_BASE64 = len(ROBTOP_BASE64)
URL_LENGHT_ANDROID = (
    len(ROBTOP_ANDROID[0]),
    len(ROBTOP_ANDROID[1])
)

APK_DOWNLOAD_LINK = 'https://download1076.mediafire.com/g0b0zlk80ptg/zg82woctdma245b/CLEAR+GDPS.zip'
APK_GD_PATH = os.path.abspath(f'{ANDROID_FULL_DIR}/gd/android.apk')

APK_COLLISION = (
    'smali/com/robtopx/geometryjump/BuildConfig.smali',
    'smali/com/robtopx/geometryjump/GeometryJump.smali',
    'smali/com/robtopx/geometryjump/R$attr.smali',
    'smali/com/robtopx/geometryjump/R$color.smali',
    'smali/com/robtopx/geometryjump/R$drawable.smali',
    'smali/com/robtopx/geometryjump/R$id.smali',
    'smali/com/robtopx/geometryjump/R$layout.smali',
    'smali/com/robtopx/geometryjump/R$string.smali',
    'smali/com/robtopx/geometryjump/R$style.smali',
    'smali/com/robtopx/geometryjump/R$styleable.smali',
    'smali/com/robtopx/geometryjump/R.smali',
    'AndroidManifest.xml',
    'lib/armeabi-v7a/libcocos2dcpp.so'
)
