from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from PIL import Image, ImageTk, ImageFilter, ImageOps
import numpy as np

image = Image.new('RGB', (800,1280), (255, 255, 255)) #global image
backup = Image.new('RGB', (800,1280), (255, 255, 255)) #backup

class MyFrame(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("ImageShop")
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.master.minsize(width = 600, height = 500)
        self.grid()

        self.buttonLoad = Button(self, text="Open", # load img button
        command = self.load_img, width=10)
        self.buttonLoad.grid()

    def load_img(self):
        global image
        global backup
        imgname = askopenfilename(filetypes=(("JPG files", "*.jpg"),
        ("PNG files", "*.png"),
        ("BMP files", "*.bmp")))
        if imgname:
            try:
                print(imgname)
                image = Image.open(imgname)

                backup = image # to have the original image button

                tkimage = ImageTk.PhotoImage(image)
                Label(image = tkimage).grid(row = 0, column = 8,padx = 10, pady= 10)

                self.buttonHF = Button(self,text="flipH",
                command = self.H_flip,width=10)
                self.buttonHF.grid(row = 1, column = 0, padx = 10, pady = 1) # horizontal flip button

                self.buttonVF = Button(self,text="flipV",
                command = self.V_flip,width=10)
                self.buttonVF.grid(row = 2, column = 0, padx = 10, pady = 1) # vertical flip button

                self.buttonGS = Button(self,text="GrayScale",
                command = self.GSFilter,width=10)
                self.buttonGS.grid(row = 3, column = 0, padx = 10, pady = 1) # GS filter

                self.LblQT = Label(self, text = "QT number:") # label qt
                self.LblQT.grid(row = 4, column = 0, padx = 1, pady =1)

                self.EQT = Entry(self, bd =3, width = 10) # Image quantization
                self.EQT.bind("<Return>",lambda numqt: self.QTFilter(numqt = self.EQT.get()))
                self.EQT.grid(row = 4, column = 1)

                self.buttonQT = Button(self, text="Ok",
                command = lambda: self.QTFilter(numqt = self.EQT.get()), width=10)
                self.buttonQT.grid(row = 4, column = 2, ) # Image qt button


                self.LblSV = Label(self, text = "Save as:") # label qt
                self.LblSV.grid(row = 5, column = 0)

                self.ESV = Entry(self, bd =3, width = 10) # Image quantization
                self.ESV.bind("<Return>",lambda name: self.save_img(name = self.ESV.get()))
                self.ESV.grid(row = 5, column = 1)

                self.buttonSV = Button(self, text="Save", # Image save button
                command = lambda: self.save_img(name = self.ESV.get()),width=10)
                self.buttonSV.grid(row = 5, column = 2)

                self.buttonOI = Button(self, text="Original", # Retrive original image button
                command = self.originalIMG, width = 10)
                self.buttonOI.grid(row = 6, column = 0,  padx = 10, pady = 1)

                self.buttonNEG = Button(self, text = "Negative", # Negative calc button
                command = self.negative, width = 10)
                self.buttonNEG.grid(row = 7, column = 0, padx = 10, pady = 1)

                self.buttonHIST = Button(self, text = "Histogram", # Histogram calc button
                command = self.histogram, width =10)
                self.buttonHIST.grid(row = 8, column =0, padx = 10, pady =1)

                self.lblBV = Label(self, text="Bright value:")  # label brightness
                self.lblBV.grid(row=9, column=0, padx=1, pady=1)

                self.EBV = Entry(self, bd=3, width=10)
                self.EBV.bind("<Return>", lambda: self.brightness_adjust(bright=self.EBV.get()))
                self.EBV.grid(row=9, column=1)

                self.buttonBV = Button(self, text="Ok",
                                       command=lambda: self.brightness_adjust(bright=self.EBV.get()), width=10)
                self.buttonBV.grid(row=9, column=2, )  # Image brightness button

                self.lblCA = Label(self, text="Contrast:")  # label contrast
                self.lblCA.grid(row=10, column=0, padx=1, pady=1)

                self.ECA = Entry(self, bd=3, width=10)
                self.ECA.bind("<Return>", lambda: self.contrast_adjust(contrast_value=self.ECA.get()))
                self.ECA.grid(row=10, column=1)

                self.buttonCA = Button(self, text="Ok",
                                       command=lambda: self.contrast_adjust(contrast_value=self.ECA.get()), width=10)
                self.buttonCA.grid(row=10,  column=2, )  # contrast button

                mainloop()
            except:
                showerror("Open Source File", "Failed to read image\n '%s'" %imgname)
            return

    def originalIMG(self):
        global image
        global backup
        image = backup

        backupimg = ImageTk.PhotoImage(image)

        Label(image=backupimg).grid(row=0, column=20)
        mainloop()
        return image

    def H_flip(self):  # horizontal flip with pixel by pixel operations
        global image
        width = image.size[0]
        height = image.size[1]
        for y in range(height):
            for x in range(width // 2):
                left = image.getpixel((x, y))
                right = image.getpixel((width - 1 - x, y))
                image.putpixel((width - 1 - x, y), left)
                image.putpixel((x, y), right)

        HFimg = ImageTk.PhotoImage(image)
        Label(image=HFimg).grid(row=0, column=20)
        mainloop()
        return HFimg

    def V_flip(self):
        global image
        width = image.size[0]
        height = image.size[1]

        for y in range(height // 2):
            for x in range(width):
                left = image.getpixel((x, y))
                right = image.getpixel((x, height - y - 1))
                image.putpixel((x, height - y - 1), left)
                image.putpixel((x, y), right)

        VFimg = ImageTk.PhotoImage(image)
        Label(image=VFimg).grid(row=0, column=20)
        mainloop()
        return VFimg

    def save_img(self, name):
        global image
        image.save(name)

    # Create a new image with the given size
    def create_image(self, i, j):
        image = Image.new("RGB", (i, j), "white")
        return image

    def set_pixel(self, image, i, j):
        # image bounds
        width, height = image.size
        if i > width or j > height:
            return None

        pixel = image.setpixel((i, j))
        return pixel

    def get_pixel(self, image, i, j):
        # image bounds
        width, height = image.size
        if i > width or j > height:
            return None

        # get pixel
        pixel = image.getpixel((i, j))
        return pixel

    # Create a Grayscale version of the image
    def GSFilter(self):
        global image
        # Get size
        width, height = image.size
        # Create new Image and a Pixel Map
        new = self.create_image(width, height)
        pixels = new.load()

        # Transform to grayscale
        for i in range(width):
            for j in range(height):
                # Get Pixel
                pixel = self.get_pixel(image, i, j)

                # Get R, G, B values (This are int from 0 to 255)
                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]

                # Transform to grayscale
                gray = (red * 0.299) + (green * 0.587) + (blue * 0.114)

                # Set Pixel in new image
                pixels[i, j] = (int(gray), int(gray), int(gray))

        # Show image
        GSimg = ImageTk.PhotoImage(new)
        Label(image=GSimg).grid(row=0, column=20)

        image = new

        mainloop()

        return new

    def QTFilter(self, numqt):
        global image
        width, height = image.size

        newimg = self.create_image(width, height)
        newpixels = newimg.load()

        num = int(numqt)

        if num > 256:
            num = 256
        elif num <= 0:
            num = 1

        prop = 255 / num

        for i in range(0, width):
            for j in range(0, height):
                pixel = self.get_pixel(image, i, j)

                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]

                Rchan = int(red / prop)
                Gchan = int(green / prop)
                Bchan = int(blue / prop)

                newR = int(Rchan * prop)
                newG = int(Gchan * prop)
                newB = int(Bchan * prop)

                if newR > 255:
                    newR = 255
                if newG > 255:
                    newG = 255
                if newB > 255:
                    newB = 255

                newpixels[i, j] = (int(newR), int(newG), int(newB))

        QTimg = ImageTk.PhotoImage(newimg)
        Label(image=QTimg).grid(row=0, column=20)

        image = newimg

        mainloop()

        return newimg

    def negative(self):
        global image
        width, height = image.size

        new = self.create_image(width, height)
        pixels = new.load()

        for i in range(width):
            for j in range(height):
                pixel = self.get_pixel(image, i, j)

                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]

                negred = 255 - red
                neggre = 255 - green
                negblu = 255 - blue

                pixels[i, j] = (negred, neggre, negblu)

        NEGIMG = ImageTk.PhotoImage(new)
        Label(image=NEGIMG).grid(row=0, column=20)

        image = new

        mainloop()

        return new

    def hhistogram(self):
        global image
        width, height = image.size

        pixels = image.load() # load original img pixels

        histogram = []
        colored = 0

        for i in range(256):
            histogram.append(0)

        for x in range(width):
            for y in range(height):
                if(pixels[x,y][0] != pixels[x,y][1]) or (pixels[x,y][0] != pixels[x,y][2]) or (pixels[x,y][1] != pixels[x,y][2]):
                    colored = 1

        if colored == 1:
            for x in range(width):
                for y in range(height):
                    Linear_T = pixels[x, y][0] * 0.299 + pixels[x, y][1] * 0.587 + pixels[x, y][2] * 0.114
                    pixels[x, y] = int(Linear_T), int(Linear_T), int(Linear_T)

        for x in range(width):
            for y in range(height):
                histogram[pixels[x,y][0]] = histogram[pixels[x,y][0]] + 1

        return histogram


    def brightness_adjust(self, bright):
        global image
        width, height = image.size

        brightness = int(bright)

        new = self.create_image(width, height)
        pixels = new.load()

        for x in range(width):
            for y in range(height):
                pixel = self.get_pixel(image, x, y)

                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]

                Linear_TR = red + brightness
                Linear_TG = green + brightness
                Linear_TB = blue + brightness

                if Linear_TR > 255:
                    Linear_TR = 255
                elif Linear_TR < 0:
                    Linear_TR = 0

                if Linear_TG > 255:
                    Linear_TG = 255
                elif Linear_TG < 0:
                    Linear_TG = 0

                if Linear_TB > 255:
                    Linear_TB = 255
                elif Linear_TB < 0:
                    Linear_TB = 0

                pixels[x, y] = int(Linear_TR), int(Linear_TG), int(Linear_TB)


        newimg = ImageTk.PhotoImage(new)
        Label(image=newimg).grid(row=0, column=20)

        image = new

        mainloop()




    def contrast_adjust(self, contrast_value):
        global image
        width, height = image.size

        contrast = float(contrast_value)

        new = self.create_image(width, height)
        pixels = new.load()

        for x in range(width):
            for y in range(height):
                pixel = self.get_pixel(image, x, y)

                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]

                Linear_TR = red * contrast
                Linear_TG = green * contrast
                Linear_TB = blue * contrast

                if Linear_TR > 255:
                    Linear_TR = 255

                if Linear_TG > 255:
                    Linear_TG = 255

                if Linear_TB > 255:
                    Linear_TB = 255

                pixels[x, y] = int(Linear_TR), int(Linear_TG), int(Linear_TB)

        newimg = ImageTk.PhotoImage(new)
        Label(image=newimg).grid(row=0, column=20)

        image = new

        mainloop()

    def histogram(self):
        h = self.createHistogram
        h = self.normalizeHistogram

        img = np.zeros([256,256,3],dtype=np.uint8)
        img.fill(255)

        for column in range(0,256):
            key = (column, column, column)
            pixelsCount = 0
            if key in h:
                pixelsCount = h[key]
            for row in range(256 - pixelsCount,256):
                img[row, column] = [55, 55, 55]


        return img

    def createHistogram(self):
        global image
        height, width, channels = image.shape

        histogram = {}

        for row in range(0, height):
            for columns in range(0, width):
                key = tuple(image[row,column])
                if key in histogram:
                    histogram[key] += 1
                else:
                    histogram[key] = 1

        return histogram


    def normalizeHistogram(self):
        sortedValues = sorted(h.values())
        biggest = sortedValues[len(h.values()) - 1]
        new = {}

        for value in range(0, 256):
            key = (value, value, value)
            new[key] = 0
            if key in h:
                new[key] = 256 * h[key] / biggest

        return new




if __name__=="__main__":
    MyFrame().mainloop()
