import tkinter.filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
from io import BytesIO
import os
import pathlib
import json
import os
import math
from functools import partial
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import tkinter.filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
import os
from tkinter import ttk
import random
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

MAX_COLOR_VALUE = 255
MAX_BIT_VALUE = 8

class IMG_Stegno:
    def main(self, root):
        root.title('Steganography by AFTAB')
        root.geometry('630x650')
        root.resizable(width=False, height=False)
        root.config(bg='#e3f4f1')

        frame = tk.Frame(root, bg='#e3f4f1')
        frame.grid(sticky="nsew")

        title = tk.Label(frame, text='Image Steganography')
        title.config(font=('Times New Roman', 25, 'bold'), bg='#e3f4f1')
        title.grid(row=0, column=0, columnspan=4, pady=10)

        image = Image.open('demo.png')
        image = image.resize((630, 500), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(frame, image=photo)
        image_label.photo = photo
        image_label.grid(row=1, column=0, columnspan=4, pady=10)

        button_style = {
            'font': ('Helvetica', 12),  
            'bg': '#ff5733',  
            'fg': 'white',  
            'width': 10,  
            'height': 1,  
            'relief': 'raised',  
            'cursor': 'hand2'  
        }

        button_frame = tk.Frame(frame, bg='#e3f4f1')
        button_frame.grid(row=2, column=0, columnspan=4, pady=10, padx=10)

        buttons = [
            ("Mosaic Image", partial(self.mosaic_frame1, frame)),
            ("Encode Text", partial(self.encode_frame1, frame)),
            ("Decode Text", partial(self.decode_frame1, frame)),
            ("Encode Image", self.encode_image),
            ("Decode Image", self.decode_image)
        ]

        for i, (text, command) in enumerate(buttons):
            button = tk.Button(button_frame, text=text, command=command, **button_style)
            button.grid(row=0, column=i, padx=10)

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)



    def make_image(self, data, resolution):
        image = Image.new("RGB", resolution)
        image.putdata(data)
        return image

    def remove_n_least_significant_bits(self, value, n):
        value = value >> n
        return value << n

    def get_n_least_significant_bits(self, value, n):
        value = value << MAX_BIT_VALUE - n
        value = value % MAX_COLOR_VALUE
        return value >> MAX_BIT_VALUE - n

    def get_n_most_significant_bits(self, value, n):
        return value >> MAX_BIT_VALUE - n

    def shift_n_bits_to_8(self, value, n):
        return value << MAX_BIT_VALUE - n

    def encode_image(self):
        try:
            image_to_hide_path = filedialog.askopenfilename(title="Select Image to Hide")
            image_to_hide_in_path = filedialog.askopenfilename(title="Select Image to Hide In")
            image_to_hide = Image.open(image_to_hide_path)
            image_to_hide_in = Image.open(image_to_hide_in_path)
            
            if image_to_hide.size != image_to_hide_in.size:
                raise ValueError("Images must have the same dimensions")

            image_to_hide = image_to_hide.resize(image_to_hide_in.size)
            encoded_image = self.encodea(image_to_hide, image_to_hide_in, 2)
            encoded_image.save("encoded_image.png")
            self.show_image("encoded_image.png")
        except Exception as e:
            print("Error:", str(e))

    def decode_image(self):
        try:
            image_to_decode_path = filedialog.askopenfilename(title="Select Image to Decode")
            image_to_decode = Image.open(image_to_decode_path)
            decoded_image = self.decodea(image_to_decode, 2)
            decoded_image.save("decoded_image.png")
            self.show_image("decoded_image.png")
        except Exception as e:
            print("Error:", str(e))

    def encodea(self, image_to_hide, image_to_hide_in, n_bits):
        width, height = image_to_hide_in.size
        hide_image = image_to_hide.load()
        hide_in_image = image_to_hide_in.load()
        data = []

        for y in range(height):
            for x in range(width):
                try:
                    r_hide, g_hide, b_hide = hide_image[x, y]
                    r_hide = self.get_n_most_significant_bits(r_hide, n_bits)
                    g_hide = self.get_n_most_significant_bits(g_hide, n_bits)
                    b_hide = self.get_n_most_significant_bits(b_hide, n_bits)

                    r_hide_in, g_hide_in, b_hide_in = hide_in_image[x, y]
                    r_hide_in = self.remove_n_least_significant_bits(r_hide_in, n_bits)
                    g_hide_in = self.remove_n_least_significant_bits(g_hide_in, n_bits)
                    b_hide_in = self.remove_n_least_significant_bits(b_hide_in, n_bits)

                    data.append((r_hide + r_hide_in,
                                g_hide + g_hide_in,
                                b_hide + b_hide_in))
                except Exception as e:
                    print(e)

        return self.make_image(data, image_to_hide.size)

    def decodea(self, image_to_decode, n_bits):
        width, height = image_to_decode.size
        encoded_image = image_to_decode.load()
        data = []

        for y in range(height):
            for x in range(width):
                r_encoded, g_encoded, b_encoded = encoded_image[x, y]
                r_encoded = self.get_n_least_significant_bits(r_encoded, n_bits)
                g_encoded = self.get_n_least_significant_bits(g_encoded, n_bits)
                b_encoded = self.get_n_least_significant_bits(b_encoded, n_bits)
                r_encoded = self.shift_n_bits_to_8(r_encoded, n_bits)
                g_encoded = self.shift_n_bits_to_8(g_encoded, n_bits)
                b_encoded = self.shift_n_bits_to_8(b_encoded, n_bits)
                data.append((r_encoded, g_encoded, b_encoded))

        return self.make_image(data, image_to_decode.size)
            
    

    def show_image(self, path):
        image = Image.open(path)
        image.thumbnail((400, 400))
        img = ImageTk.PhotoImage(image)
        label = tk.Label(image=img)
        label.image = img
        label.pack()
    

    def back(self, frame):
        frame.destroy()
        self.main(root)

    def encode_frame1(self, F):
        F.destroy()
        F2 = Frame(root)
        label1 = Label(F2, text='Select the Image in which you want to hide text:')
        label1.config(font=('Times New Roman', 25, 'bold'), bg='#e3f4f1')
        label1.grid()

        button_bws = Button(F2, text='Select', command=lambda: self.encode_frame2(F2))
        button_bws.config(font=('Helvetica', 18), bg='#e8c1c7')
        button_bws.grid()
        button_back = Button(F2, text='Cancel', command=lambda: self.back(F2))
        button_back.config(font=('Helvetica', 18), bg='#e8c1c7')
        button_back.grid(pady=15)
        button_back.grid()
        F2.grid()

    def mosaic_frame1(self, F):
        F.destroy()
        F2 = Frame(root)
        label1 = Label(F2, text='Select the Image in which you want to mosaic:')
        label1.config(font=('Times New Roman', 25, 'bold'), bg='#e3f4f1')
        label1.grid()

        button_bws = Button(F2, text='Select', command=lambda: self.encode_frame3(F2))
        button_bws.config(font=('Helvetica', 18), bg='#e8c1c7')
        button_bws.grid()
        button_back = Button(F2, text='Cancel', command=lambda: self.back(F2))
        button_back.config(font=('Helvetica', 18), bg='#e8c1c7')
        button_back.grid(pady=15)
        button_back.grid()
        F2.grid()

    def decode_frame1(self, F):
        F.destroy()
        d_F2 = Frame(root)
        label1 = Label(d_F2, text='Select Image with Hidden text:')
        label1.config(font=('Times New Roman', 25, 'bold'), bg='#e3f4f1')
        label1.grid()
        label1.config(bg='#e3f4f1')
        button_bws = Button(d_F2, text='Select', command=lambda: self.decode_frame2(d_F2))
        button_bws.config(font=('Helvetica', 18), bg='#e8c1c7')
        button_bws.grid()
        button_back = Button(d_F2, text='Cancel', command=lambda: self.back(d_F2))
        button_back.config(font=('Helvetica', 18), bg='#e8c1c7')
        button_back.grid(pady=15)
        button_back.grid()
        d_F2.grid()

    def encode_frame2(self, e_F2):
        e_pg = Frame(root)
        myfile = tkinter.filedialog.askopenfilename(
            filetypes=([('png', '*.png'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'), ('All Files', '*.*')]))
        if not myfile:
            messagebox.showerror("Error", "You have selected nothing!")
        else:
            my_img = Image.open(myfile)
            new_image = my_img.resize((300, 200))
            img = ImageTk.PhotoImage(new_image)
            label3 = Label(e_pg, text='Selected Image')
            label3.config(font=('Helvetica', 14, 'bold'))
            label3.grid()
            board = Label(e_pg, image=img)
            board.image = img
            self.output_image_size = os.stat(myfile)
            self.o_image_w, self.o_image_h = my_img.size
            board.grid()
            label2 = Label(e_pg, text='Enter the message')
            label2.config(font=('Helvetica', 14, 'bold'))
            label2.grid(pady=15)
            text_a = Text(e_pg, width=50, height=10)
            text_a.grid()
            encode_button = Button(e_pg, text='Cancel', command=lambda: self.back(e_pg))
            encode_button.config(font=('Helvetica', 14), bg='#e8c1c7')
            button_back = Button(e_pg, text='Encode',
                                command=lambda: [self.enc_fun(text_a, my_img), self.back(e_pg)])
            button_back.config(font=('Helvetica', 14), bg='#e8c1c7')
            button_back.grid(pady=15)
            encode_button.grid()
            e_pg.grid(row=1)
            e_F2.destroy()

    def encode_frame3(self, e_F2):
        e_pg = Frame(root)
        myfile = tkinter.filedialog.askopenfilename(
            filetypes=([('png', '*.png'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'), ('All Files', '*.*')]))
        if not myfile:
            messagebox.showerror("Error", "You have selected nothing!")
        else:
            my_img = Image.open(myfile)
            new_image = my_img.resize((300, 200))
            img = ImageTk.PhotoImage(new_image)
            label3 = Label(e_pg, text='Selected Image')
            label3.config(font=('Helvetica', 14, 'bold'))
            label3.grid()
            board = Label(e_pg, image=img)
            board.image = img
            self.output_image_size = os.stat(myfile)
            self.o_image_w, self.o_image_h = my_img.size
            board.grid()
            encode_button = Button(e_pg, text='Cancel', command=lambda: self.back(e_pg))
            encode_button.config(font=('Helvetica', 14), bg='#e8c1c7')
            button_back = Button(e_pg, text='Mosaic', command=lambda: self.process_image(e_F2, myfile))
            button_back.config(font=('Helvetica', 14), bg='#e8c1c7')
            button_back.grid(pady=15)
            encode_button.grid()
            e_pg.grid(row=1)
            e_F2.destroy()

    def get_average_color(self, img):
        average_color = np.average(np.average(img, axis=0), axis=0)
        average_color = np.around(average_color, decimals=-1)
        average_color = tuple(int(i) for i in average_color)
        return average_color

    def get_closest_color(self, color, colors):
        cr, cg, cb = color

        min_difference = float("inf")
        closest_color = None
        for c in colors:
            r, g, b = eval(c)
            difference = math.sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
            if difference < min_difference:
                min_difference = difference
                closest_color = eval(c)

        return closest_color

    def process_image(self, e_F2, myfile):
        if "cache.json" not in os.listdir():
            imgs_dir = pathlib.Path("stego")
            images = list(imgs_dir.glob("*.png"))

            data = {}
            for img_path in images:
                img = cv2.imread(str(img_path))
                average_color = self.get_average_color(img)
                if str(tuple(average_color)) in data:
                    data[str(tuple(average_color))].append(str(img_path))
                else:
                    data[str(tuple(average_color))] = [str(img_path)]
            with open("cache.json", "w") as file:
                json.dump(data, file, indent=2, sort_keys=True)
            print("Caching done")

        with open("cache.json", "r") as file:
            data = json.load(file)

        img = cv2.imread(myfile)
        img_height, img_width, _ = img.shape
        tile_height, tile_width = 5, 5
        num_tiles_h, num_tiles_w = img_height // tile_height, img_width // tile_width
        img = img[:tile_height * num_tiles_h, :tile_width * num_tiles_w]

        tiles = []
        for y in range(0, img_height, tile_height):
            for x in range(0, img_width, tile_width):
                tiles.append((y, y + tile_height, x, x + tile_width))

        for tile in tiles:
            y0, y1, x0, x1 = tile
            try:
                average_color = self.get_average_color(img[y0:y1, x0:x1])
            except Exception:
                continue
            closest_color = self.get_closest_color(average_color, data.keys())

            i_path = random.choice(data[str(closest_color)])
            i = cv2.imread(i_path)
            i = cv2.resize(i, (tile_width, tile_height))
            img[y0:y1, x0:x1] = i

            cv2.imshow("Image", img)
            cv2.waitKey(1)

        new_filename = tkinter.filedialog.asksaveasfilename(defaultextension=".jpg")
        if new_filename:
            cv2.imwrite(new_filename, img)

    def decode_frame2(self, d_F2):
        d_F3 = Frame(root)
        myfiles = tkinter.filedialog.askopenfilename(
            filetypes=([('png', '*.png'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'), ('All Files', '*.*')]))
        if not myfiles:
            messagebox.showerror("Error", "You have selected nothing!")
        else:
            my_img = Image.open(myfiles, 'r')
            my_image = my_img.resize((300, 200))
            img = ImageTk.PhotoImage(my_image)
            label4 = Label(d_F3, text='Selected Image :')
            label4.config(font=('Helvetica', 14, 'bold'))
            label4.grid()
            board = Label(d_F3, image=img)
            board.image = img
            board.grid()
            hidden_data = self.decode(my_img)
            label2 = Label(d_F3, text='Hidden data is :')
            label2.config(font=('Helvetica', 14, 'bold'))
            label2.grid(pady=10)
            text_a = Text(d_F3, width=50, height=10)
            text_a.insert(INSERT, hidden_data)
            text_a.configure(state='disabled')
            text_a.grid()
            button_back = Button(d_F3, text='Cancel', command=lambda: self.frame_3(d_F3))
            button_back.config(font=('Helvetica', 14), bg='#e8c1c7')
            button_back.grid(pady=15)
            button_back.grid()
            d_F3.grid(row=1)
            d_F2.destroy()

    def decode(self, image):
        image_data = iter(image.getdata())
        data = ''

        while (True):
            pixels = [value for value in image_data.__next__()[:3] +
                      image_data.__next__()[:3] +
                      image_data.__next__()[:3]]
            binary_str = ''
            for i in pixels[:8]:
                if i % 2 == 0:
                    binary_str += '0'
                else:
                    binary_str += '1'

            data += chr(int(binary_str, 2))
            if pixels[-1] % 2 != 0:
                return data

    def generate_Data(self, data):
        new_data = []

        for i in data:
            new_data.append(format(ord(i), '08b'))
        return new_data

    def modify_Pix(self, pix, data):
        dataList = self.generate_Data(data)
        dataLen = len(dataList)
        imgData = iter(pix)
        for i in range(dataLen):
            pix = [value for value in imgData.__next__()[:3] +
                   imgData.__next__()[:3] +
                   imgData.__next__()[:3]]
            for j in range(0, 8):
                if (dataList[i][j] == '0') and (pix[j] % 2 != 0):
                    if (pix[j] % 2 != 0):
                        pix[j] -= 1
                elif (dataList[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1
            if (i == dataLen - 1):
                if (pix[-1] % 2 == 0):
                    pix[-1] -= 1
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1
            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode_enc(self, newImg, data):
        w = newImg.size[0]
        (x, y) = (0, 0)

        for pixel in self.modify_Pix(newImg.getdata(), data):
            newImg.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1

    def enc_fun(self, text_a, myImg):
        data = text_a.get("1.0", "end-1c")
        if (len(data) == 0):
            messagebox.showinfo("Alert", "Kindly enter text in TextBox")
        else:
            newImg = myImg.copy()
            self.encode_enc(newImg, data)
            new_filename = tkinter.filedialog.asksaveasfilename(defaultextension=".png")
            if new_filename:
                newImg.save(new_filename)
                messagebox.showinfo("Success", "Encoding Successful\nFile is saved as Image_with_hiddentext.png in the same directory")

    def frame_3(self, frame):
        frame.destroy()
        self.main(root)

root = Tk()
o = IMG_Stegno()
o.main(root)
root.mainloop()