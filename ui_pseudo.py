class BoneImg(object, url):
    """docstring for BoneImg."""
    def __init__(self, arg):
        super(BoneImg, self).__init__()
        self.arg = arg

        img = cv2.imread(url)
        label_img = null
        isShow = False


def ribCounting(img, isShow):
    if(onClick(showLabel)):
        if(img.label_img == null and !isShow):
            single_img = cropSingleBody(img)
            rib_img = cropRib(single_img)
            img.label_img = countRib(rib_img)
            isShow = True
