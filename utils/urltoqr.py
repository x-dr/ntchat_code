import qrcode
from nanoid import generate
import os.path
import os
import sys

def get_exec_dir():
    return os.path.dirname(sys.argv[0])


def get_download_dir():
    user_dir = os.path.join(get_exec_dir(), 'qrcode')
    user_dir = os.path.abspath(user_dir)
    if not os.path.isdir(user_dir):
        os.makedirs(user_dir)
    return user_dir


def get_img_file():
    while True:
        path = os.path.join(get_download_dir(), generate(size=10))
        # print(path)
        if not os.path.isfile(path):
            return path


 # => "IRFa-VaY2b"
def create_qr_code(url):
# 实例化QRCode生成qr对象
    img_file=get_img_file()+'.png'
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(img_file)
    return img_file


# print(create_qr_code('http://www.baidu.com'))