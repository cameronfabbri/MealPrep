"""

"""
# Copyright (c) 2019.
# Cameron Fabbri

from BingImages import BingImages

def get_image_url(keywords):
    keywords = ','.join(keywords)
    return list(BingImages(keywords, count=1).get())[0]
