import requests
from io import BytesIO
from hashlib import md5


def get_image_hash(image):
    h = md5(image.read())
    image.seek(0)
    return h.hexdigest()


def download_image(url):
    with requests.Session() as session:
        resp = session.head(url)
        if resp.status_code == 200:
            if resp.headers['Content-Type'].startswith('image/'):
                resp = session.get(url, stream=True)
                if resp.status_code == 200:
                    fp = BytesIO()
                    for r in resp:
                        fp.write(r)
                    fp.seek(0)
                    return fp
