import customtkinter as ctk
import tkinter as tk
from PIL import Image,ImageTk
from panels import * 

bg_color = '#212121'
bdr_color ='#cecac9'
class Works_place_area(ctk.CTkFrame):
    def __init__ (self,root_app):
        super().__init__(master =root_app,corner_radius=0)
        self.grid(row=1,column=0,sticky='news')

        self.columnconfigure(0,weight=5,uniform='b')
        self.columnconfigure(1,weight=15,uniform='b')
        self.columnconfigure(2,weight=8,uniform='b')
        self.rowconfigure(0,weight=1)

        self.left_side = ctk.CTkFrame(self)
        self.left_side.grid(row=0,column=0,sticky='news',pady = 20, padx = 10)
        self.Tool_box = Tool_box(self.left_side,root_app)
        self.Layer_box = Layer_box(self.left_side,root_app)
        self.canvas = Canvas_area(self,root_app)
        self.Menu_box = Menu_box(self,root_app)

class Canvas_area(ctk.CTkCanvas):
    def __init__ (self,canvas_frame,root_app):
        super().__init__(master =canvas_frame,highlightthickness=0,relief='ridge',background = bg_color)
        self.grid(row=0,column=1,sticky='news',padx = 5,pady=15)
        image_item = self.create_image(int(self.cget("width"))//2,int(self.cget("height"))//2, anchor=tk.CENTER,image = root_app.imagetk)

        self.bind('<Configure>',root_app.resize_image)
        #self.bind("<MouseWheel>",root_app.on_mouse_wheel)
        self.bind("<Motion>", root_app.track_cursor_placement)
        

class Menu_box(ctk.CTkTabview):
    def __init__ (self,parent_app,root_app):
        super().__init__(master =parent_app,corner_radius=25,border_width = 5,)
        self.grid(row=0,column=2,sticky='news',pady = 10, padx = 10)

        self.add('Pos')
        self.add('Color')
        self.add('Effect')
        self.add('Text')
        self.add('Shape')
        self.add('Export')
        

        Position_box(self.tab('Pos'),root_app)
        Color_box(self.tab('Color'),root_app)
        Effect_box(self.tab('Effect'),root_app)
        Export_box(self.tab('Export'),root_app.export_image)
        Text_box(self.tab('Text'),root_app)
        Shape_box(self.tab('Shape'),root_app)

class Tool_box(ctk.CTkFrame):
    def __init__ (self, parent_app,root_app):
        super().__init__(master=parent_app)
        self.pack(expand = True,fill = 'both',pady = 10,padx =10)
        ToolButton(self,root_app,'icon\Image_Crop_Icon.png',root_app.crop_image)
        ToolButton(self,root_app,"icon\Rectangle_Icon.png",root_app.draw_rectangle)
        ToolButton(self,root_app,"icon\Ellipse_Icon.png",root_app.draw_ellipse)
        ToolButton(self,root_app,"icon\Polygon_Icon.png",root_app.draw_polygon)
        ToolButton(self,root_app,"icon\Selection_Icon.png",root_app.draw_selection)
        # ToolButton(self,root_app,"B")
    
class Layer_box(ctk.CTkFrame):
    def __init__ (self, parent_app,root_app):
        super().__init__(master=parent_app,height=400)
        self.pack(expand = True,fill = 'both',pady = 10,padx =10)
        self.root_app = root_app
        self.root_app.layer_box = self
  

class Position_box(ctk.CTkFrame):
    def __init__ (self, parent_app,root_app):
        super().__init__(master=parent_app,fg_color='transparent')
        self.pack(expand = True, fill = 'both')

        self.root_app = root_app
        PostionPanel(self,root_app)
        SliderPanel(self,root_app.opacity,"opacity",0,255)
        SliderPanel(self,root_app.rotate_var,"rotation",-180,180)
        SegmentPanel(self,root_app.flip_var,"Invert",FLIP_OPTIONS)
        

        # RevertButton(self,(root_app.rotate_var,ROTATE_DEFAULT),
        #              (root_app.flip_var,FLIP_OPTIONS[0]))

class Color_box(ctk.CTkFrame):
    def __init__ (self, parent_app,root_app):
        super().__init__(master=parent_app,fg_color='transparent')
        self.pack(expand = True, fill = 'both')

        self.root_app = root_app

        SliderPanel(self,root_app.brightness,"Brightness",0,5 )
        SliderPanel(self,root_app.vibrance,"Vibrance",0,5 )
        SwitchPanel(self,(root_app.grayscale,"B/W"),(root_app.invert,"Invert"))

        SliderPanel(self,root_app.color_red,"Red",-100,100)
        SliderPanel(self,root_app.color_green,"Green",-100,100)
        SliderPanel(self,root_app.color_blue,"Blue",-100,100)
        SliderPanel(self,root_app.color_hue,"Hue",-100,100)
        #CurveToolPanel(self,root_app)

        # RevertButton(self,(root_app.brightness,BRIGHTNESS_DEFAULT),
        #              (root_app.vibrance,VIBRANCE_DEFAULT),
        #              (root_app.grayscale,GRAYSCALE_DEFAULT))
        

class Effect_box(ctk.CTkFrame):
    def __init__ (self, parent_app,root_app):
        super().__init__(master=parent_app,fg_color='transparent')
        self.pack(expand = True, fill = 'both')

        self.root_app = root_app
        layer_var = root_app.current_layer

        DropDownPanel(self, root_app.effect, EFFECT_OPTION)
        SliderPanel(self,root_app.blur,"Blur",0,30 )
        SliderPanel(self,root_app.sharpness,"Sharpness",0,5 )

        equalize_button = ctk.CTkButton(self,text="Equalize",command=self.root_app.equalize_image)
        equalize_button.pack(pady = 8,padx = 5)

        FilterPanel(self,"min filter",root_app.min_filter,0,9)
        FilterPanel(self,"max filter",root_app.max_filter,0,9)
        FilterPanel(self,"median filter",root_app.median_filter,0,9)

        

        reset_button = ctk.CTkButton(self,text="Reset", command=root_app.reset_image_layer)
        reset_button.pack(side = 'bottom')

class Text_box(ctk.CTkFrame):
    def __init__ (self, parent_app,root_app):
        super().__init__(master=parent_app,fg_color='transparent')
        self.pack(expand = True, fill = 'both')
        self.root_app = root_app

        self.add_text_button = ctk.CTkButton(self,text="Add text",command=root_app.add_text_layer)
        self.add_text_button.pack(pady = 5)
        self.choose_font_button = ctk.CTkButton(self,textvariable=root_app.font_path,command=root_app.import_font)
        self.choose_font_button.pack(pady = 5)
        self.entry_x = ctk.CTkEntry(self,textvariable=root_app.text_x)
        self.entry_x.pack(pady = 10)
        self.entry_y = ctk.CTkEntry(self,textvariable=root_app.text_y)
        self.entry_y.pack(pady = 5)
        self.entry_size = ctk.CTkEntry(self,textvariable=root_app.font_size)
        self.entry_size.pack(pady = 5)
        self.entry_color = ctk.CTkEntry(self,textvariable=root_app.text_color)
        self.entry_color.pack(pady = 5)
        self.entry_content = ctk.CTkEntry(self,textvariable=root_app.text_content)
        self.entry_content.pack(pady = 5)

class Shape_box(ctk.CTkFrame):
    def __init__ (self, parent_app,root_app):
        super().__init__(master=parent_app,fg_color='transparent')
        self.pack()
        shape_color = ctk.StringVar(value="black")
        outline_color = ctk.StringVar(value="black")
        outline_width = ctk.IntVar(value=0)
        data_points  =ctk.StringVar(value="0,0")

        shape_color_entry = ctk.CTkEntry(self,textvariable=shape_color)
        shape_color_entry.pack()

        outline_color_entry = ctk.CTkEntry(self,textvariable=outline_color)
        outline_color_entry.pack()

        outline_width_entry = ctk.CTkEntry(self,textvariable=outline_width)
        outline_width_entry.pack()

        data_points_entry = ctk.CTkEntry(self,textvariable=data_points)
        data_points_entry.pack()

        apply_button = ctk.CTkButton(self,text = "update",command = lambda *args: root_app.update_shape(shape_color.get(),
                                                                                                       outline_color.get(),
                                                                                                       outline_width.get(),
                                                                                                       data_points.get()))
        apply_button.pack()

class Menu_Bar(ctk.CTkFrame):
    def __init__ (self,root_app):
        super().__init__(master =root_app)
        self.grid(row=0,column=0,sticky='news',pady = 3, padx = 10)
        padx = 1
        pady = 5
        ipadx = 2
        ipady = 3
        b1 = ctk.CTkButton(self,text="Import",width=80,corner_radius=5,command=root_app.import_image)
        b1.pack(side = 'left',padx = padx,pady = pady,ipadx = ipadx,ipady = ipady)
        b2 = ctk.CTkButton(self,text="Add Layer",width=80,corner_radius=5,command=root_app.add_layer)
        b2.pack(side = 'left',padx = padx,pady = pady,ipadx = ipadx,ipady = ipady)
        b3 = ctk.CTkButton(self,text="Exit",width=80,corner_radius=5)
        b3.pack(side = 'left',padx = padx,pady = pady,ipadx = ipadx,ipady = ipady)

class Export_box(ctk.CTkFrame):
    def __init__(self,parent,export_image):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand = True,fill = 'both')

        self.name_string = ctk.StringVar()
        self.file_string = ctk.StringVar()
        self.path_string = ctk.StringVar()

        FilePathPanel(self,self.path_string)
        FileNamePanel(self,self.name_string,self.file_string)
        
        SaveButton(self,export_image ,self.name_string,self.file_string,self.path_string)