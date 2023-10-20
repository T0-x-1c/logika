from PIL import Image, ImageFilter

class ImageEditor():
    def __init__(self, fielname):
        self.fielname = fielname

        self.original = None
        self.edited = []

    def open(self):
        try:
            self.original = Image.open(self.fielname)
            self.original.show()
        except:
            print('файл не знайдено')

    def do_left(self):
        left = self.original.transpose(Image.ROTATE_90)
        self.edited.append(left)

        left.save('left_' + self.fielname)

    def bw(self):
        bw = self.original.convert('L')
        self.edited.append(bw)

        bw.save('bw' + self.fielname)

img = ImageEditor('gomer.jpeg')
