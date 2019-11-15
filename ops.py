from google_images_download import google_images_download

def get_image_url(keywords):

    keywords = ','.join(keywords)

    response  = google_images_download.googleimagesdownload()
    arguments = {'keywords':keywords,'limit':1,'print_urls':True,'no_download':True, 'silent_mode':True}
    image_url_ = response.download(arguments)[0][keywords]

    img_count = 0
    while image_url_ == []:
        img_count += 1
        image_url_ = response.download(arguments)[0][keywords]
        #if img_count > 20: 
        #    image_url_ = [None]
        #else:
        #    image_url_ = response.download(arguments)[0][title]

    image_url = image_url_[0]
    return image_url
