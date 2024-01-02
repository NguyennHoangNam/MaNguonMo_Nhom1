import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk,Image,ImageOps,ImageEnhance,ImageFilter
from Frame import *
from settings import *
import numpy as np
import cv2

#ctk.set_default_color_theme("theme\cutomtheme.json")

class App(ctk.CTk):
    def __init__ (self):
        super().__init__()
        SCREEN_W, SCREEN_H = self.winfo_screenwidth(), self.winfo_screenheight()
        WINDOW_W, WINDOW_H = int(SCREEN_W*0.9),int(SCREEN_H*0.9)
        self.geometry(f"{WINDOW_W}x{WINDOW_H}+{(SCREEN_W-WINDOW_W)//2}+{(SCREEN_H-WINDOW_H-80)//2}")
        
        self.init_parameter()

        self.rowconfigure(0,weight=1,uniform='a')
        self.rowconfigure(1,weight=19,uniform='a')
        self.columnconfigure(0,weight=1)
        
        self.layers = []

        self.base_image = Image.new("RGB",(500,500))
        self.current_layer = None
        self.image = self.base_image
        self.imagetk = ImageTk.PhotoImage(self.image)


        self.work_place = Works_place_area(self)
        self.canvas = self.work_place.canvas
        self.menu_bar = Menu_Bar(self)
        
        self.mainloop()
        

    def init_parameter(self):
        self.opacity = ctk.IntVar(value=255)

        self.zoom_level = ctk.DoubleVar(value=ZOOM_DEFAULT)
        self.rotate_var = ctk.DoubleVar(value=ROTATE_DEFAULT)
        self.flip_var = ctk.StringVar(value=FLIP_OPTIONS[0])
    
        self.brightness = ctk.DoubleVar(value=BRIGHTNESS_DEFAULT)
        self.grayscale = ctk.BooleanVar(value=GRAYSCALE_DEFAULT)
        self.invert = ctk.BooleanVar(value=INVERT_DEFAULT)
        self.vibrance = ctk.DoubleVar(value=VIBRANCE_DEFAULT)

        self.blur = ctk.DoubleVar(value=BLUR_DEFAULT)
        self.sharpness = ctk.DoubleVar(value=SHARPNESS_DEFAULT)
        self.effect = ctk.StringVar(value=EFFECT_OPTION[0])

        self.control_points = CONTROL_POINTS_DEFAULT
        #self.red = ctk.I

        self.curso_crood = ctk.StringVar(value='')

        #self.red_value = ctk.IntVar

        self.vars = [self.opacity,self.rotate_var,self.flip_var,self.brightness,self.grayscale,
                     self.invert,self.vibrance,self.blur,self.sharpness,self.effect]
        
        for var in self.vars:
            var.trace_add('write',lambda *args: self.manipulate_image(self.current_layer))


    def reset_parameter(self):
        
        self.opacity.set(OPACITY_DEFAULT)
        self.zoom_level.set(ZOOM_DEFAULT)
        self.rotate_var.set(ROTATE_DEFAULT)
        self.flip_var.set(FLIP_OPTIONS[0])

        self.brightness.set(BRIGHTNESS_DEFAULT)
        self.grayscale.set(GRAYSCALE_DEFAULT)
        self.invert.set(INVERT_DEFAULT)
        self.vibrance.set(VIBRANCE_DEFAULT)

        self.blur.set(BLUR_DEFAULT)
        self.sharpness.set(SHARPNESS_DEFAULT)
        self.effect.set(EFFECT_OPTION[0])

        self.control_points = CONTROL_POINTS_DEFAULT
        self.curvetool.update_canvas_info()
        #self.red = ctk.I

        self.curso_crood.set('')

    def manipulate_image(self,layer):
        self.image = self.base_image
        layer.image_data = layer.og_image_data

        #if self.opacity.get() != OPACITY_DEFAULT:
        layer.opacity = int(self.opacity.get())
        if layer.opacity <0: layer.opacity = 0
        elif layer.opacity >255: layer.opacity =255
        if self.rotate_var.get() != ROTATE_DEFAULT:
            value = self.rotate_var.get()
            layer.image_data = layer.image_data.rotate(value,Image.NEAREST)
            #layer.rotate_var = value
        if self.flip_var.get() == 'X':
            value = self.flip_var.get()
            layer.image_data = ImageOps.mirror(layer.image_data)
            #layer.flip_var = value
        elif self.flip_var.get() == 'Y':
            #layer.flip_var = self.flip_var.get()
            layer.image_data = ImageOps.flip(layer.image_data)
        elif self.flip_var.get() == 'Both':
            #layer.flip_var = self.flip_var.get()
            layer.image_data = ImageOps.mirror(layer.image_data)
            layer.image_data = ImageOps.flip(layer.image_data)
        if self.brightness.get() != BRIGHTNESS_DEFAULT:
            value = self.brightness.get()
            layer.brightness = value
            brightness_enhancer = ImageEnhance.Brightness(layer.image_data)
            layer.image_data = brightness_enhancer.enhance(value)
            
        if self.vibrance.get() != VIBRANCE_DEFAULT:
            value = self.vibrance.get()
            vibrance_enhancer = ImageEnhance.Color(layer.image_data)
            layer.image_data = vibrance_enhancer.enhance(value)
            #layer.vibrance = value
        if self.grayscale.get():
            layer.image_data = ImageOps.grayscale(layer.image_data)
            #layer.grayscale = self.grayscale.get()
        if self.invert.get():
            layer.image_data = ImageOps.invert(layer.image_data)
            #layer.invert = self.invert.get()
        if self.blur.get() != BLUR_DEFAULT:
            value = self.blur.get()
            layer.image_data = layer.image_data.filter(ImageFilter.GaussianBlur(value))
            #layer.blur = value
        if self.sharpness.get() !=SHARPNESS_DEFAULT:
            value = self.sharpness.get()
            layer.image_data = layer.image_data.filter(ImageFilter.UnsharpMask(self.sharpness.get()))
            #layer.sharpness = value
        if self.control_points != CONTROL_POINTS_DEFAULT:
            #layer.control_points = self.control_points
            array = (np.array(self.control_points) * 255).astype(int)
            layer.image_data = self.apply_curve_adjustment(layer.image_data,array)

        match self.effect.get():
            case 'Emboss': 
                layer.image_data = layer.image_data.filter(ImageFilter.EMBOSS)
                #layer.effect = 'Emboss'
            case 'Find edges': 
                layer.image_data = layer.image_data.filter(ImageFilter.FIND_EDGES)
                #layer.effect = 'Find edges'
            case 'Contour': 
                layer.image_data = layer.image_data.filter(ImageFilter.CONTOUR)
                #layer.effect = 'Contour'
            case 'Edge enchance': 
                layer.image_data = layer.image_data.filter(ImageFilter.EDGE_ENHANCE)
                #layer.effect = 'Edge enchance'
        self.show_image()



    def resize_image(self,event =None):
        self.image = self.base_image
        # self.image2 = self.image2.resize(self.base_image.size,Image.NEAREST)
        # self.image3 = self.image3.resize(self.base_image.size,Image.NEAREST)
        # self.image = Image.composite(self.image2,self.image,Image.new('L',self.image.size,255))
        # self.image = Image.composite(self.image3,self.image,Image.new('L',self.image.size,0))
        self.image_ratio = self.image.size[0] / self.image.size[1]
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.Canvas_ratio = self.canvas_width /self.canvas_height
        if self.Canvas_ratio > self.image_ratio:
            self.image_height = int(self.canvas_height)
            self.image_width = int(self.image_height * self.image_ratio)
        else:
            self.image_width = int(self.canvas_width)
            self.image_height = int(self.image_width / self.image_ratio)
        #self.image_width =int(self.image_width*self.zoom_level.get())
        #self.image_height =int(self.image_height*self.zoom_level.get())
        
        self.show_image()

    def show_image(self):
        
        self.canvas.delete('all')
        self.resized_image = self.image.resize((self.image_width,self.image_height),Image.NEAREST)
        for layer in self.layers:
            layer_resize_image = layer.image_data.resize(self.resized_image.size,Image.NEAREST)
            self.resized_image = Image.composite(layer_resize_image,
                                            self.resized_image,
                                            Image.new('L',self.resized_image.size,
                                                    layer.opacity))
        self.imagetk = ImageTk.PhotoImage(self.resized_image)
        self.canvas.create_image(self.canvas_width // 2,self.canvas_height//2,anchor=tk.CENTER,image = self.imagetk)

    def change_current_layer(self,current_layer,layer):
        
        self.current_layer = layer
        self.opacity.set(layer.opacity)
        for i in range(1,len(self.vars)):
            current_layer.vars[i] = self.vars[i].get()

        for i in range(1, len(self.vars)):
            self.vars[i].set(layer.vars[i])
        
        #self.manipulate_image(layer)
        

        
        # self.zoom_level.set(layer.zoom_level)
        # self.rotate_var.set(layer.rotate_var)
        # self.flip_var.set(layer.flip_var)

        # self.brightness.set(layer.brightness)
        # self.grayscale.set(layer.grayscale)
        # self.invert.set(layer.invert)
        # self.vibrance.set(layer.vibrance)

        # self.blur.set(layer.blur)
        # self.sharpness.set(layer.sharpness)
        # self.effect.set(layer.effect)

        # self.control_points = layer.control_points
        #self.curvetool.update_canvas_info()

    def delete_layer(self,layer):
        layer.panel.destroy()
        self.layers.remove(layer)
        self.show_image()
        del layer

    def duplicate_layer(self,layer):
        self.layers.append(Layer(self,"Layer " + str(len(self.layers)),layer.image_data))

    def add_layer(self):
        path = filedialog.askopenfile(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")]).name
        new_image = Image.open(path)
        self.layers.append(Layer(self,"Layer " + str(len(self.layers)),new_image))
        self.show_image()

    def on_mouse_wheel(self, event):
        # Determine the direction and magnitude of the scroll
        delta = event.delta
        if delta > 0:
            self.zoom_level.set(self.zoom_level.get()* 1.1)
        else:
            self.zoom_level.set(self.zoom_level.get()/ 1.1)

        # Limit the zoom level between 0.1 and 10.0
        self.zoom_level.set(max(0.1, min(2, self.zoom_level.get()))) 

        # Update the displayed image
        self.image = ImageOps.crop(image=self.image,border=self.zoom_level.get())
        self.resize_image()
        


    def track_cursor_placement(self,event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        #self.curso_crood.set(f"{x} , {y}")     
    def crop_image(self,parent):
        self.crop_start_x = None
        self.crop_start_y = None
        self.crop_end_x = None
        self.crop_end_y = None
        self.crop_button = parent
        self.canvas.bind("<Button-1>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.update_crop)
        self.canvas.bind("<ButtonRelease-1>", self.end_crop)

    def start_crop(self, event):
        
        self.x_offset = int((self.canvas_width - self.resized_image.size[0])/2)
        self.y_offset = int((self.canvas_height -self.resized_image.size[1])/2)
        self.crop_start_x = event.x
        self.crop_start_y = event.y

    def update_crop(self, event):
        self.crop_end_x = event.x
        self.crop_end_y = event.y
        self.canvas.delete("crop_rectangle")
        self.canvas.create_rectangle(
            self.crop_start_x,
            self.crop_start_y,
            self.crop_end_x,
            self.crop_end_y,
            outline="gray20",
            tags="crop_rectangle",
            fill= "gray60",
            width=4,
            dash =(20,5),
            stipple="gray12"
        )
    def end_crop(self, event):
        self.canvas.delete("crop_rectangle")
        if self.crop_start_x < self.x_offset: self.crop_start_x = self.x_offset
        if self.crop_start_y < self.y_offset: self.crop_start_y = self.y_offset
        x1, y1, x2, y2 = self.crop_start_x- self.x_offset, self.crop_start_y-self.y_offset, event.x- self.x_offset, event.y- self.y_offset
        self.current_layer.image_data = self.current_layer.image_data.resize(self.resized_image.size,Image.NEAREST)
        for layer in self.layers:
            self.current_layer.image_data = self.current_layer.image_data.crop((min(x1,x2), min(y1,y2), max(x1,x2), max(y1,y2)))
        self.resize_image()
        self.crop_button.configure(fg_color = WHITE)
        self.configure(cursor="")
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
    
    def apply_curve_adjustment(self ,pil_image, control_points):
        image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2HSV)
        # Create a lookup table for the curve adjustment
        lut = np.zeros((256, 1), dtype=np.uint8)

        # Split the control points into x and y coordinates
        x = [point[0] for point in control_points]
        y = [point[1] for point in control_points]

        # Interpolate the curve between control points
        interp = np.interp(np.arange(256), x, y)

        # Populate the lookup table
        lut[:, 0] = np.clip(interp, 0, 255).astype(np.uint8)

        # Apply the curve adjustment using the lookup table
        image[:, :, 2] = cv2.LUT(image[:, :, 2], lut)
        final_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_HSV2RGB))


        return final_image

    def import_image(self):
        path = filedialog.askopenfile(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")]).name
        new_image = Image.open(path)
        if self.layers:
            for layer in self.layers:
                self.delete_layer(layer)
        self.layers = []
        self.layers.append(Layer(self,"Layer " + str(len(self.layers)),new_image))
        self.base_image = Image.new("RGB",new_image.size)
        self.current_layer = self.layers[0]
        
        #self.reset_parameter()
        self.resize_image()
        
    def export_image(self,name,file,path):
            export_string = f'{path}/{name}.{file}'
            self.resized_image.save(export_string)
            
class Layer:
    def __init__(self,root_app,name,image_data):
        self.name = name
        self.og_image_data = image_data
        self.image_data = image_data   
        self.panel = LayerPanel(root_app.layer_box,self)

        self.opacity = OPACITY_DEFAULT

        self.zoom_level = ZOOM_DEFAULT
        self.rotate_var = ROTATE_DEFAULT
        self.flip_var = FLIP_OPTIONS[0]
    
        self.brightness = BRIGHTNESS_DEFAULT
        self.grayscale = GRAYSCALE_DEFAULT
        self.invert = INVERT_DEFAULT
        self.vibrance = VIBRANCE_DEFAULT

        self.blur = BLUR_DEFAULT
        self.sharpness = SHARPNESS_DEFAULT
        self.effect = EFFECT_OPTION[0]

        self.control_points = CONTROL_POINTS_DEFAULT


        self.vars = [self.opacity,self.rotate_var,self.flip_var,self.brightness,self.grayscale,
                     self.invert,self.vibrance,self.blur,self.sharpness,self.effect]
        # for var in self.vars:
        #     var.trace_add('write',lambda *args: root_app.manipulate_image(self))         
    

App()