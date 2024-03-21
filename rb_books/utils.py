import os

from datetime import datetime


def dynamic_upload_img_path(instance, filename):
    path = datetime.now().strftime('covers/%Y/%m/%d')
    base_filename, file_extension = os.path.splitext(filename)
    return f'{path}/{instance.slug}{file_extension}'
