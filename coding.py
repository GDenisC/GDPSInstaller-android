
from dataclasses import dataclass
import os
from typing import Optional
from zipfile import ZipFile
from const import (
    APK_DOWNLOAD_LINK,
    APK_GD_PATH,
    ROBTOP,
    ROBTOP_ANDROID,
    ROBTOP_ANDROID_REPLACE,
    ROBTOP_BASE64,
    URL_LENGHT,
    URL_LENGHT_ANDROID,
    URL_LENGHT_HTTP,
    URL_LENGHT_BASE64,
    base64_encode
)
from threading import Thread
import requests

def checkurl(url: str, /) -> bool:
    if url.startswith('http://'):
        return URL_LENGHT_HTTP == len(url)
    return URL_LENGHT == len(url)

def checkandroid(android: str, /) -> bool:
    if android.startswith('L'):
        return len(android) == URL_LENGHT_ANDROID[0]
    return len(android) == URL_LENGHT_ANDROID[1]

def base64url(url: str, /) -> Optional[str]:
    if not url.startswith('http://'):
        url = 'http://' + url
    url = base64_encode(url)
    if len(url) == URL_LENGHT_BASE64:
        return url
    return None

def replace_links(file: str, /, url: str, robtopx: str = 'robtopx', geometryjump: str = 'geometryjump', *, android: bool = True) -> None:
    with open(file, 'rb') as f:
        dat = f.read()
    
    if not android:
        dat = dat.replace(ROBTOP.encode(), url.encode())
        dat = dat.replace(ROBTOP_BASE64.encode(), base64url(url).encode())
    else:
        _android = ROBTOP_ANDROID_REPLACE(robtopx, geometryjump)
        dat = dat.replace(ROBTOP_ANDROID[0].encode(), _android[0].encode())
        dat = dat.replace(ROBTOP_ANDROID[1].encode(), _android[1].encode())

    with open(file, 'wb') as f:
        f.write(dat)

_APK_IS_DOWNLOADED = False

def _downloadapk() -> None:
    with open(APK_GD_PATH.replace('android.apk', 'gdclients.zip'), 'wb') as f:
        f.write(requests.get(APK_DOWNLOAD_LINK).content)
    global _APK_IS_DOWNLOADED
    _APK_IS_DOWNLOADED = True

def downloadapk() -> None:
    global _APK_IS_DOWNLOADED
    _APK_IS_DOWNLOADED = False
    Thread(target=_downloadapk).start()

def is_apk_downloaded() -> bool:
    return _APK_IS_DOWNLOADED

def unzip(filename: str, path: str) -> None:
    ZipFile(path + filename).extractall(path)
    os.remove(path + filename)

@dataclass
class GDPS:
    name: str
    database: str
