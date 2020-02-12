"""

"""
# Copyright (c) 2019.
# Cameron Fabbri

from BingImages import BingImages

def get_image_url(keywords):
    keywords = ','.join(keywords)
    print('keywords:',keywords)
    try:
        a = list(BingImages(keywords, count=1).get())[0]
    except:
        a = 'https://lh3.googleusercontent.com/proxy/V0ZSsia8R9xFWJyKQjwsYO3Mp55UdlFyeFtS7RR4xq6gLTD_HZnGTKOG5_Efc_EFTEfGRQdH4CmnUwU7LfLfIwQQWFcF7ErVsM0vnS3N4XWNlyOQxfkXrliG1w'
    return a
