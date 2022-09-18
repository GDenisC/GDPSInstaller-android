
import os
from shutil import copyfile, rmtree
import sys
from coding import (
    GDPS,
    checkurl,
    downloadapk,
    is_apk_downloaded,
    unzip,
    APK_GD_PATH,
    replace_links
)
from time import sleep
from const import (
    ANDROID_APKTOOL,
    ANDROID_DIR,
    ANDROID_SIGNAPK,
    APK_COLLISION,
    APKTOOL_DIR,
    DEBUG,
    JAVA9,
    JAVA_INSTALLED,
    JAVA_VERSION,
    SIGNAPK_DIR,
    URL_LENGHT
)
from logs import log, loginput

def check_java() -> None:
    log('Checking java...')

    if not JAVA_INSTALLED:
        log('Java not installed.', error='ERROR')
        os.system('pause')
        sys.exit(-1)
    log('Java installed.')

    if not JAVA_VERSION:
        log('Java version not detected.', error='ERROR')
        os.system('pause')
        sys.exit(-1)
    log('Java version getted')

    if JAVA9:
        log('Java9 Enabled', error='WARN')

    JAVA_VER = int(float('.'.join(JAVA_VERSION.decode().split('"')[1].split('.')[:2])))
    if (JAVA_VER >= 9) or (JAVA_VER >= 10 and JAVA9):
        log('Java Version >9 (>10) not supports signapk.', error='ERROR')
        os.system('pause')
        sys.exit(-1)

GDPSC: GDPS = None

def get_params() -> None:
    global GDPSC
    while True:
        name = loginput('GDPS Name: ')
        db = loginput('GDPS Database: ')
        GDPSC = GDPS(name, db)

        if not (len(GDPSC.database) == URL_LENGHT and checkurl(GDPSC.database)):
            log(f'GDPS Database not success. You need {URL_LENGHT} simvols! (without http:// ).')
            continue
        if len(name) != len('geometryjump'):
            log(f'GDPS Name not success. You need {len("geometryjump")} simvols!')
            continue
        break
    log('Data success getted.')

def install_clients() -> None:
    if os.path.exists(APK_GD_PATH):
        log('android.apk already created, skipping task', error='WARN')
        return
    log('Starting downloading apk...')
    try:
        downloadapk()
    except Exception as e:
        log(e, error='ERROR')

    while 1:
        if is_apk_downloaded():
            break
        sleep(1)

    log('Success APK download!')

def unzip_clients() -> None:
    if os.path.exists(APK_GD_PATH):
        log('android.apk already created, skipping task', error='WARN')
        return
    log('Unzipping gdclients.zip...')
    unzip('gdclients.zip', APK_GD_PATH.replace('android.apk', ''))
    log('Unzipped!')

def create_android_apk() -> None:
    if os.path.exists(APK_GD_PATH):
        log('android.apk already created, skipping task', error='WARN')
    else:
        log('Creating android.apk...')
        os.replace(APK_GD_PATH.replace('android.apk', 'Android/Geometry Dash.apk'), APK_GD_PATH)
        log('Created!')
        log('Directory Android and PC not removed.', error='WARN')
    if not os.path.exists(APK_GD_PATH.replace('android.apk', 'PC')):
        return

    i = loginput('Want you remove Android and PC dirs? (YES or NO) (ENTER to YES): ')
    if i == '':
        i = 'YES'
    if i == 'YES':
        log('Starting new task...')
        rmtree(APK_GD_PATH.replace('android.apk', 'Android'), ignore_errors=True)
        rmtree(APK_GD_PATH.replace('android.apk', 'PC'), ignore_errors=True)
        log('Success removed!')

def use_apktool() -> None:
    if not os.path.exists(APKTOOL_DIR + 'android.apk'):
        log('Coping android.apk...')
        copyfile(APK_GD_PATH, APKTOOL_DIR + 'android.apk')

    log('Starting apktool...')
    ANDROID_APKTOOL[0]('android.apk')

    log('Starting replacing links...')
    for link in APK_COLLISION:
        log(f'Replacing {APKTOOL_DIR + "android/" + link}')
        replace_links(APKTOOL_DIR + 'android/' + link, '', 'deniscx', GDPSC.name)

    log(f'Replacing android/apktool/android/lib/armeabi-v7a/libcocos2dcpp.so')
    replace_links(APKTOOL_DIR + 'android/lib/armeabi-v7a/libcocos2dcpp.so', GDPSC.database, android=False)
    
    log('Renaming Geometry Dash')
    with open(APKTOOL_DIR + 'android/res/values/strings.xml', 'r') as f:
        dat = f.read().replace('Geometry Dash', GDPSC.name)
    with open(APKTOOL_DIR + 'android/res/values/strings.xml', 'w') as f:
        f.write(dat)
    
    log('Ending apktool...')
    ANDROID_APKTOOL[1]('android')
    os.rename(APKTOOL_DIR + 'android/dist/android.apk', SIGNAPK_DIR + 'gd.apk')
    rmtree(APKTOOL_DIR + 'android')
    os.remove(APKTOOL_DIR + 'android.apk')

def use_signapk() -> None:
    log('Finalizing...')
    ANDROID_SIGNAPK('gd', 'gd-signed')
    os.rename(ANDROID_DIR + 'signapk/gd-signed.apk', './dist/' + GDPSC.name + '.apk')

try:
    check_java()
    get_params()
    install_clients()
    unzip_clients()
    create_android_apk()
    log('Downloading tasks finished, starting GDPS creation')
    use_apktool()
    use_signapk()
except Exception as e:
    log(f"ERROR | {e}", error='ERROR')
    log('! YOU NEED REINSTALL GDPS INSTALLER OR CLEAR ./ANDROID/ FILES TO FIX OTHER ERRORS !', error='ERROR')

log('Android builded.')
os.system('pause') # P.S .exe not have that line
