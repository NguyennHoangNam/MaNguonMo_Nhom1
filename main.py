import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk,Image,ImageOps,ImageEnhance,ImageFilter,ImageFont,ImageDraw
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
        self.change_layer = False

        self.base_image = Image.new("RGB",(500,500))
        self.current_layer = None
        self.current_text_layer = None
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

        self.color_red = ctk.DoubleVar(value=RED_DEFAULT)
        self.color_green = ctk.DoubleVar(value=GREEN_DEFAULT)
        self.color_blue = ctk.DoubleVar(value=BLUE_DEFAULT)
        self.color_hue = ctk.DoubleVar(value=HUE_DEFAULT)


        self.font_path = ctk.StringVar(value=FONT_PATH_DEFAULT)
        self.font_size = ctk.IntVar(value=FONT_SIZE_DEFAULT)
        self.text_x = ctk.IntVar(value=TEXT_X)
        self.text_y = ctk.IntVar(value=TEXT_Y)
        self.text_content = ctk.StringVar(value=TEXT_CONTENT_DEFAULT)
        self.text_color = ctk.StringVar(value=TEXT_COLOR_DEFAULT)

        #self.control_points = CONTROL_POINTS_DEFAULT
        self.curso_crood = ctk.StringVar(value='')

        self.vars = [self.opacity,self.rotate_var,self.flip_var,
                     self.brightness,self.grayscale,self.invert,self.vibrance,
                     self.blur,self.sharpness,self.effect,
                     self.color_red,self.color_green,self.color_blue,self.color_hue]
        self.text_vars = [self.font_path,self.font_size,self.text_x,self.text_y,self.text_content,self.text_color]
        
        for var in self.vars:
            var.trace_add('write',lambda *args: self.manipulate_image(self.current_layer,self.current_text_layer))

        for var in self.text_vars:
            var.trace_add('write',lambda *args: self.manipulate_image(self.current_layer,self.current_text_layer))

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

        # self.control_points = CONTROL_POINTS_DEFAULT
        # self.curvetool.update_canvas_info()
        # #self.red = ctk.I

        # self.curso_crood.set('')

    def manipulate_image(self,layer,text_layer):
        if not layer:
            return
        self.image = self.base_image
        layer.image_data = layer.og_image_data
        red, green, blue, alpha = layer.image_data.split()
        layer.image_data = Image.merge('RGB', (red, green, blue))

        #if self.opacity.get() != OPACITY_DEFAULT:
        layer.opacity = int(self.opacity.get())
        if layer.opacity <0: layer.opacity = 0
        elif layer.opacity >255: layer.opacity =255
        if self.rotate_var.get() != ROTATE_DEFAULT:
            value = self.rotate_var.get()
            layer.image_data = layer.image_data.rotate(value,expand=True,resample = Image.NEAREST)
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
            #layer.brightness = value
            brightness_enhancer = ImageEnhance.Brightness(layer.image_data)
            layer.image_data = brightness_enhancer.enhance(value)
            
        if self.vibrance.get() != VIBRANCE_DEFAULT:
            value = self.vibrance.get()
            vibrance_enhancer = ImageEnhance.Color(layer.image_data)
            layer.image_data = vibrance_enhancer.enhance(value)
            #layer.vibrance = value
        if self.grayscale.get():
            #layer.image_data = ImageOps.grayscale(layer.image_data)
            image_array = np.array(layer.image_data)
            average_values = np.mean(image_array, axis=2, keepdims=True)

            # Set the average value for all color channels
            image_array[:, :, :] = average_values
            layer.image_data = Image.fromarray(np.clip(image_array,0,255).astype(np.uint8))
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
        # if self.control_points != CONTROL_POINTS_DEFAULT:
        #     #layer.control_points = self.control_points
        #     array = (np.array(self.control_points) * 255).astype(int)
        #     layer.image_data = self.apply_curve_adjustment(layer.image_data,array)
        try:
            for i,color in enumerate([self.color_red,self.color_green,self.color_blue]):
                if color.get()>0:
                    image_array = np.array(layer.image_data)
                    image_array[:, :, i] = (image_array[:, :, i] +
                                                    (255-image_array[:, :, i])*((color.get())/100))
                    layer.image_data = Image.fromarray(np.clip(image_array,0,255).astype(np.uint8))
                elif color.get()<0:
                    image_array = np.array(layer.image_data)
                    image_array[:, :, i] = (image_array[:, :, i] -
                                                    (image_array[:, :, i])*((color.get())/-100))
                    layer.image_data = Image.fromarray(np.clip(image_array,0,255).astype(np.uint8))
        except :
            pass

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
        if text_layer and not self.change_layer :
            for i in range(len(self.text_vars)):
                try:
                    text_layer.text_vars[i] = self.text_vars[i].get()
                except:
                    pass
        red, green, blue = layer.image_data.split()

        layer.image_data = Image.merge('RGBA', (red, green, blue,alpha))
        self.show_image()


    def resize_image(self,event =None):

        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()

        self.image_ratio = self.image.size[0] / self.image.size[1]   
        self.Canvas_ratio = self.canvas_width /self.canvas_height
        if self.Canvas_ratio > self.image_ratio:
            self.image_height = int(self.canvas_height)
            self.image_width = int(self.image_height * self.image_ratio)
        else:
            self.image_width = int(self.canvas_width)
            self.image_height = int(self.image_width / self.image_ratio)
        self.scale = self.image_width/self.base_image.size[0]
        #self.image_width =int(self.image_width*self.zoom_level.get())
        #self.image_height =int(self.image_height*self.zoom_level.get())
        
        self.show_image()

    def show_image(self):
        
        self.canvas.delete('all')
        self.resized_image = self.image.resize((self.image_width,self.image_height),Image.NEAREST)
        for layer in self.layers:
            if not layer.is_text:
                layer_resize_image = layer.image_data.resize((int(max(10,layer.image_data.size[0]*self.scale * layer.size)),
                                                              int(max(10,layer.image_data.size[1]*self.scale * layer.size))),
                                                              Image.NEAREST)
                #layer_resize_image = layer_resize_image.crop((0,0,self.resized_image.size[0],self.resized_image.size[1]))
                # self.resized_image = Image.composite(layer_resize_image,
                #                                 self.resized_image,
                #                                 Image.new('L',layer_resize_image.size,
                #                                         layer.opacity))
                #layer_resize_image.convert('RGBA')
                mask1 = layer_resize_image.convert('RGBA')
                red, green, blue, alpha = mask1.split()
                new_alpha = alpha.point(lambda i: i*(layer.opacity/255))
                mask = Image.merge('RGBA', (red, green, blue, new_alpha))
                self.resized_image.paste(layer_resize_image,(layer.position[0],layer.position[1]),mask=mask)
            elif layer.is_text:
                try:
                    draw = ImageDraw.Draw(self.resized_image)
                    font = ImageFont.truetype(layer.text_vars[0], layer.text_vars[1])
                    draw.text((layer.text_vars[2],layer.text_vars[3]), layer.text_vars[4], fill=layer.text_vars[5], font=font)
                except:
                    pass

        self.imagetk = ImageTk.PhotoImage(self.resized_image)
        self.canvas.create_image(self.canvas_width // 2,self.canvas_height//2,anchor=tk.CENTER,image = self.imagetk)

    def change_current_layer(self,current_layer,layer):
        
        self.current_layer = layer
        self.opacity.set(layer.opacity)
        if current_layer:
            for i in range(1,len(self.vars)):
                current_layer.vars[i] = self.vars[i].get()

        for i in range(1, len(self.vars)):
            self.vars[i].set(layer.vars[i])

    def change_current_text_layer(self,current_text_layer,layer):
        self.change_layer = True
        self.current_text_layer = layer
        if current_text_layer:
            for i in range(len(self.text_vars)):
                self.text_vars[i].set(layer.text_vars[i])
        
        self.change_layer = False
    def delete_layer(self,layer):
        self.layers.remove(layer)
        layer.panel.destroy()
        self.show_image()
        del layer

    def duplicate_layer(self,layer):
        new_layer = Layer(self,"Layer " + str(len(self.layers)),layer.image_data)
        self.layers.append(new_layer)
        self.change_current_layer(self.current_layer,new_layer)
        self.show_image()

    def duplicate_text_layer(self,layer):
        new_text = Text_layer(self,"Text " + str(len(self.layers)))
        for i in range(len(new_text.text_vars)):
            new_text.text_vars[i] = layer.text_vars[i]
        self.layers.append(new_text)
        self.change_current_text_layer(self.current_text_layer,new_text)
        self.show_image()

    def add_layer(self):
        path = filedialog.askopenfile(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")]).name
        new_image = Image.open(path)
        image_layer = Layer(self,"Layer " + str(len(self.layers)),new_image)
        self.layers.append(image_layer)
        self.change_current_layer(self.current_layer,image_layer)
        self.show_image()

    def add_text_layer(self):
        text_layer = Text_layer(self,"Text " + str(len(self.layers)))
        self.layers.append(text_layer)
        self.change_current_text_layer(self.current_text_layer,text_layer)
        self.manipulate_image(self.current_layer,self.current_text_layer)
        self.show_image()

    def move_layer_up(self,layer):
        index = self.layers.index(layer)
        if index <len(self.layers)-1:
            self.layers[index], self.layers[index + 1] = self.layers[index + 1], self.layers[index]

        for widget in self.layer_box.winfo_children():
            widget.pack_forget()
        for layer in self.layers:
            layer.panel.pack(fill = 'x',side = 'bottom',pady = 4,ipady = 8,padx = 5)
        if not layer.is_text:
            self.change_current_layer(self.current_layer,layer)
        elif layer.is_text:
            self.change_current_text_layer(self.current_text_layer,layer)
        self.show_image()

    def move_layer_down(self,layer):
        index = self.layers.index(layer)
        if index > 0:
            self.layers[index], self.layers[index - 1] = self.layers[index - 1], self.layers[index]
        for widget in self.layer_box.winfo_children():
            widget.pack_forget()
        for layer in self.layers:
            layer.panel.pack(fill = 'x',side = 'bottom',pady = 4,ipady = 8,padx = 5)
        if not layer.is_text:
            self.change_current_layer(self.current_layer,layer)
        elif layer.is_text:
            self.change_current_text_layer(self.current_text_layer,layer)
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
    def crop_image(self,button):
        self.crop_start_x = None
        self.crop_start_y = None
        self.crop_end_x = None
        self.crop_end_y = None
        self.crop_button = button
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
        self.current_layer.image_data = self.base_image.resize(self.resized_image.size,Image.NEAREST)
        crop_image = self.resized_image.crop((min(x1,x2), min(y1,y2), max(x1,x2), max(y1,y2)))
        self.base_image = Image.new("RGB",crop_image.size)
        self.resize_image()
        self.change_current_layer(self.current_layer,self.current_layer)
        self.crop_button.configure(fg_color = WHITE)
        self.configure(cursor="")
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
    
    def draw_rectangle(self,button):
        self.crop_start_x = None
        self.crop_start_y = None
        self.crop_end_x = None
        self.crop_end_y = None
        self.crop_button = button
        self.canvas.bind("<Button-1>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.update_crop)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw_rectangle)

    def end_draw_rectangle(self,event):
        self.canvas.delete("crop_rectangle")
        if self.crop_start_x < self.x_offset: self.crop_start_x = self.x_offset
        if self.crop_start_y < self.y_offset: self.crop_start_y = self.y_offset
        x1, y1, x2, y2 = self.crop_start_x- self.x_offset, self.crop_start_y-self.y_offset, event.x- self.x_offset, event.y- self.y_offset

        new_image = Image.new("RGBA",(max(x1,x2)-min(x1,x2),max(y1,y2)-min(y1,y2)))
        rectangle = [(min(x1,x2), min(y1,y2)), (max(x1,x2), max(y1,y2))]
        shape_layer = Shape_layer(self,"Rectangle " + str(len(self.layers)),new_image,rectangle,'rectangle')

        self.layers.append(shape_layer)
        self.change_current_layer(self.current_layer,shape_layer)
        self.show_image()

        self.resize_image()
        self.change_current_layer(self.current_layer,self.current_layer)
        self.crop_button.configure(fg_color = WHITE)
        self.configure(cursor="")
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def update_shape(self,color,outline,width,data):
        if self.current_layer.is_shape:
            match self.current_layer.shape_type:
                case 'rectangle':
                    try:
                        data = data.split(",")
                        data_points = [int(num) for num in data]
                        self.current_layer.og_image_data =  Image.new("RGBA",(data_points[0],data_points[1]))
                        rectangle = [(0, 0), (data_points[0],data_points[1])]
                        draw = ImageDraw.Draw(self.current_layer.og_image_data)
                        draw.rectangle(rectangle, fill=color,outline=outline,width=width)
                        
                        self.change_current_layer(self.current_layer,self.current_layer)
                        self.show_image()
                    except:
                        pass

                case 'ellipse':
                    try:
                        data = data.split(",")
                        data_points = [int(num) for num in data]
                        self.current_layer.og_image_data =  Image.new("RGBA",(data_points[0],data_points[1]))
                        rectangle = [(0, 0), (data_points[0],data_points[1])]
                        draw = ImageDraw.Draw(self.current_layer.og_image_data)
                        draw.ellipse(rectangle, fill=color,outline=outline,width=width)
                        
                        self.change_current_layer(self.current_layer,self.current_layer)
                        self.show_image()
                    except:
                        pass
                case 'polygon':
                    try:
                        data = data.split(",")
                        data_points = [int(num) for num in data]
                        self.current_layer.og_image_data =  Image.new("RGBA",self.base_image.size)
                        draw = ImageDraw.Draw(self.current_layer.og_image_data)
                        arr_2d = [[x, y] for x, y in zip(data_points[::2], data_points[1::2])]

                        subtracted_list = [(max(0,sublist[0] - arr_2d[0][0]), max(0,sublist[1] - arr_2d[0][1])) for sublist in arr_2d]
                        draw.polygon(subtracted_list, fill=color,outline=outline,width=width)
                        
                        self.change_current_layer(self.current_layer,self.current_layer)
                        self.show_image()
                    except:
                        pass

    def draw_ellipse(self,button):
        self.crop_start_x = None
        self.crop_start_y = None
        self.crop_end_x = None
        self.crop_end_y = None
        self.crop_button = button
        self.canvas.bind("<Button-1>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.update_crop)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw_ellipse)

    def end_draw_ellipse(self,event):
        self.canvas.delete("crop_rectangle")
        if self.crop_start_x < self.x_offset: self.crop_start_x = self.x_offset
        if self.crop_start_y < self.y_offset: self.crop_start_y = self.y_offset
        x1, y1, x2, y2 = self.crop_start_x- self.x_offset, self.crop_start_y-self.y_offset, event.x- self.x_offset, event.y- self.y_offset

        new_image = Image.new("RGBA",(max(x1,x2)-min(x1,x2),max(y1,y2)-min(y1,y2)))
        ellipse = [(min(x1,x2), min(y1,y2)), (max(x1,x2), max(y1,y2))]
        shape_layer = Shape_layer(self,"Ellipse " + str(len(self.layers)),new_image,ellipse,'ellipse')

        self.layers.append(shape_layer)
        self.change_current_layer(self.current_layer,shape_layer)
        self.show_image()

        self.resize_image()
        self.change_current_layer(self.current_layer,self.current_layer)
        self.crop_button.configure(fg_color = WHITE)
        self.configure(cursor="")
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def draw_polygon(self,button):
        self.crop_button = button
        self.polygon_points = []

        self.x_offset = int((self.canvas_width - self.resized_image.size[0])/2)
        self.y_offset = int((self.canvas_height -self.resized_image.size[1])/2)

        self.canvas.bind("<Button-1>", self.add_polygon_point)
        #self.canvas.bind("<Double-Button-1>", self.end_draw_polygon)
        self.canvas.bind("<Double-Button-1>", self.end_draw_polygon)


    def add_polygon_point(self,event):
        x = event.x
        y = event.y
        if x < self.x_offset: x = self.x_offset
        if y < self.y_offset: y = self.y_offset

        x = x - self.x_offset
        y = y - self.y_offset
        self.polygon_points.append((x,y))
    def end_draw_polygon(self,event):
        new_image = Image.new("RGBA",self.base_image.size)
        shape_layer = Shape_layer(self,"Polygon " + str(len(self.layers)),new_image,self.polygon_points,'polygon')
        self.layers.append(shape_layer)
        self.change_current_layer(self.current_layer,shape_layer)
        self.show_image()
        self.resize_image()
        self.change_current_layer(self.current_layer,self.current_layer)
        self.crop_button.configure(fg_color = WHITE)
        self.configure(cursor="")
        self.canvas.unbind("<Double-Button-1>")
        self.canvas.unbind("<Button-1>")
        

    def draw_selection(self,button):
        self.crop_button = button
        self.polygon_points = []

        self.x_offset = int((self.canvas_width - self.resized_image.size[0])/2)
        self.y_offset = int((self.canvas_height -self.resized_image.size[1])/2)

        self.canvas.bind("<Button-1>", self.add_polygon_point)
        #self.canvas.bind("<Double-Button-1>", self.end_draw_polygon)
        self.canvas.bind("<Double-Button-1>", self.end_selection)

    def end_selection(self,event):
        mask = Image.new("L",self.current_layer.og_image_data.size)
        draw = ImageDraw.Draw(mask)
        draw.polygon(self.polygon_points,fill=255)

        result = Image.new("RGBA", self.current_layer.og_image_data.size)
        result.paste(self.current_layer.image_data, (0, 0), mask=mask)
        self.current_layer.og_image_data = result
        self.show_image()
        self.resize_image()
        self.change_current_layer(self.current_layer,self.current_layer)
        self.crop_button.configure(fg_color = WHITE)
        self.configure(cursor="")
        self.canvas.unbind("<Double-Button-1>")
        self.canvas.unbind("<Button-1>")
    
    def equalize_image(self):
        red, green, blue, alpha = self.current_layer.og_image_data.split()

        red = np.array(red)
        r_eq = cv2.equalizeHist(red)
        red_img = Image.fromarray(np.clip(r_eq,0,255).astype(np.uint8))

        green = np.array(green)
        g_eq  = cv2.equalizeHist(green)
        green_img = Image.fromarray(np.clip(g_eq,0,255).astype(np.uint8))

        blue = np.array(blue)
        b_eq   = cv2.equalizeHist(blue)
        blue_img = Image.fromarray(np.clip(b_eq,0,255).astype(np.uint8))

        self.current_layer.og_image_data = Image.merge('RGBA', (red_img, green_img, blue_img,alpha))
        self.change_current_layer(self.current_layer,self.current_layer)
        self.show_image()
    
    
    
    # def apply_curve_adjustment(self ,pil_image, control_points):
    #     image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2HSV)
    #     # Create a lookup table for the curve adjustment
    #     lut = np.zeros((256, 1), dtype=np.uint8)

    #     # Split the control points into x and y coordinates
    #     x = [point[0] for point in control_points]
    #     y = [point[1] for point in control_points]

    #     # Interpolate the curve between control points
    #     interp = np.interp(np.arange(256), x, y)

    #     # Populate the lookup table
    #     lut[:, 0] = np.clip(interp, 0, 255).astype(np.uint8)

    #     # Apply the curve adjustment using the lookup table
    #     image[:, :, 2] = cv2.LUT(image[:, :, 2], lut)
    #     final_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_HSV2RGB))


    #     return final_image

    def import_image(self):
        path = filedialog.askopenfile(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")]).name
        new_image = Image.open(path)
        for widget in self.layer_box.winfo_children():
            widget.destroy()
        if self.layers:
            for layer in self.layers:
                self.delete_layer(layer)
        self.layers = []
        self.layers.append(Layer(self,"Layer " + str(len(self.layers)),new_image))
        self.base_image = Image.new("RGB",new_image.size)
        self.image = self.base_image
        self.current_layer = self.layers[0]
        
        self.change_current_layer(None,self.layers[0])
        self.resize_image()
        
    def export_image(self,name,file,path):
            export_string = f'{path}/{name}.{file}'
            self.resized_image.save(export_string)

    def import_font(self):
        path = filedialog.askopenfile(filetypes=[("Font Files", "*.ttf;*.otf")]).name
        self.font_path.set(path)

    def change_layer_position(self,x,y,z):
        self.current_layer.position = [x,y]
        self.current_layer.size = z
        self.show_image()

    def reset_layer_position(self):
        self.current_layer.position = [0,0]
        self.current_layer.size = 1
        self.show_image()

    def min_filter(self,value):
        try:
            self.current_layer.og_image_data = self.current_layer.og_image_data.filter(ImageFilter.MinFilter(size=value))
            self.change_current_layer(self.current_layer,self.current_layer)
            self.show_image()
        except:
            pass

    def max_filter(self,value):
        try:
            self.current_layer.og_image_data = self.current_layer.og_image_data.filter(ImageFilter.MaxFilter(size=value))
            self.change_current_layer(self.current_layer,self.current_layer)
            self.show_image()
        except:
            pass
    def median_filter(self,value):
        try:
            self.current_layer.og_image_data = self.current_layer.og_image_data.filter(ImageFilter.MedianFilter(size=value))
            self.change_current_layer(self.current_layer,self.current_layer)
            self.show_image()
        except:
            pass
            
            
    def reset_image_layer(self):
        self.current_layer.og_image_data = self.current_layer.root_image
        self.change_current_layer(self.current_layer,self.current_layer)
        self.show_image()

class Layer:
    def __init__(self,root_app,name,image_data):
        self.name = name
        self.is_text = False
        self.is_shape = False
        self.root_image = image_data.convert('RGBA')
        self.og_image_data = image_data.convert('RGBA')
        self.image_data = self.og_image_data
        self.panel = LayerPanel(root_app.layer_box,self)
        self.position = [0,0]
        self.size = 1

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

        self.color_red = RED_DEFAULT
        self.color_green = GREEN_DEFAULT
        self.color_blue = BLUE_DEFAULT
        self.color_hue = HUE_DEFAULT

        self.control_points = CONTROL_POINTS_DEFAULT


        self.vars = [self.opacity,self.rotate_var,self.flip_var,
                     self.brightness,self.grayscale,self.invert,self.vibrance,
                     self.blur,self.sharpness,self.effect,
                     self.color_red,self.color_green,self.color_blue,self.color_hue]
    
    
class Text_layer:
    def __init__(self,root_app,name):
        self.name = name
        self.is_text = True

        self.font_path =FONT_PATH_DEFAULT
        self.font_size = FONT_SIZE_DEFAULT
        self.text_x = TEXT_X
        self.text_y = TEXT_Y
        self.text_content =TEXT_CONTENT_DEFAULT
        self.text_color =TEXT_COLOR_DEFAULT

        self.panel = TextLayerPanel(root_app.layer_box,self)

        self.text_vars = [self.font_path,self.font_size,self.text_x,self.text_y,self.text_content,self.text_color]

class Shape_layer(Layer):
    def __init__(self, root_app,name,image_data,data_points,shapetype):
        super().__init__(root_app = root_app,name = name,image_data = image_data)
        self.data_points = data_points
        self.is_shape = True
        self.position = [data_points[0][0],data_points[0][1]]
        self.shape_type = shapetype

        rectangle = [(0, 0), (data_points[1][0]-data_points[0][0], data_points[1][1]-data_points[0][1])]
        draw = ImageDraw.Draw(self.image_data)
        match shapetype:
            case 'rectangle':
                draw.rectangle(rectangle, fill='red')
            case 'ellipse':
                draw.ellipse(rectangle, fill='red')
            case 'polygon':
                subtracted_list = [(max(0,sublist[0] - data_points[0][0]), max(0,sublist[1] - data_points[0][1])) for sublist in data_points]
                draw.polygon(subtracted_list, fill='red')


App()