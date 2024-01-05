import customtkinter as ctk
import tkinter as tk
from PIL import Image
import math
from tkinter import filedialog
from settings import * 

class Panel(ctk.CTkFrame):
    def __init__ (self, parent):
        super().__init__(master=parent)
        self.pack(fill = 'x',pady = 4,ipady = 8,padx = 5)

class SliderPanel(Panel):
    def __init__(self, parent_app,data_var ,text,min_value,max_value):
        super().__init__(parent = parent_app)
        self.rowconfigure((0,1), weight=1)
        self.columnconfigure((0,1),weight=1)
        self.data_var = data_var
        self.num_text = ctk.StringVar()
        self.num_text.set(str(self.data_var.get()))
        self.num_text.trace_add('write',self.update_slide)
        self.data_var.trace_add('write',self.update_text)
        ctk.CTkLabel(self, text=text).grid(column = 0, row = 0, sticky ='w',padx= 5)
        self.num_label = ctk.CTkEntry(self, textvariable = self.num_text,
                                      corner_radius=0,width=50)
        self.num_label.grid(column = 1, row = 0,sticky ='e',padx= 5)
        
        self.slider = ctk.CTkSlider(self,
                      variable=self.data_var,
                      from_ = min_value,
                      to =max_value, command= self.update_text).grid(row = 1 , column = 0,columnspan  = 2,sticky = "we", padx = 10)
    def update_text(self,*value):
        self.num_text.set(f'{round(self.data_var.get(),2)}')
    def update_slide(self,*args):
        try:
            self.data_var.set(float(self.num_label.get()))
        except:
            pass


class SegmentPanel(Panel):
    def __init__(self, parent_app,var ,text,options):
        super().__init__(parent = parent_app)

        ctk.CTkLabel(self, text= text).pack()
        ctk.CTkSegmentedButton(self,values= options,variable=var).pack( expand = True,fill = 'both', padx = 4, pady = 4)
        
class SwitchPanel(Panel):
    def __init__(self, parent, *args):
        super().__init__(parent=parent)
        for var, text in args:
            switch = ctk.CTkSwitch(self, text= text,variable= var,button_color= BLUE,fg_color=SLIDER_BG)
            switch.pack(side = 'left', expand = True, fill = 'both', padx = 5, pady = 5)

class DropDownPanel(ctk.CTkOptionMenu):
    def __init__(self, parent, data_var, options):
        super().__init__(master=parent,
                         values= options,
                         fg_color=DARK_FREY,
                         button_color=DROPDOWN_MAIN_COLOR,
                         button_hover_color=DROPDOWN_HOVER_COLOR,
                         dropdown_fg_color=DROPDOWN_MENU_COLOR,
                         variable= data_var)
        self.pack(fill = 'x', pady= 4)

class RevertButton(ctk.CTkButton):

    def __init__(self, parent,*args):
        super().__init__(master=parent, text= 'revert',command=self.revert)
        self.pack(side = "bottom", pady = 10)
        self.parent = parent
        self.args = args

    def revert(self):
        for var,value in self.args:
            var.set(value)
        self.parent.root_app.original = self.parent.root_app.source_image
        self.parent.root_app.image = self.parent.root_app.original
        self.parent.root_app.resize_image()
class ToolButton(ctk.CTkLabel):
    def __init__(self, parent,root_app,image_path,funtion):
        super().__init__(master=parent,width=40,height=40,
                         image=ctk.CTkImage(Image.open(image_path), size=(26, 26)),
                         text=None,
                         fg_color=WHITE,
                         corner_radius=7)
        self.pack(padx = 5, pady =5)
        self.root_app = root_app
        self.funtion = funtion
        self.bind("<Button-1>",self.On_left_click)
    
    def On_left_click(self,event):
        self.root_app.configure(cursor="plus")
        self.Select = True
        self.configure(fg_color = BACKGROUND_COLOR)
        self.root_app.bind("<Button-3>",self.On_right_click)
        self.funtion(self)
        
    def On_right_click(self,event):
        self.root_app.configure(cursor="")
        self.configure(fg_color = WHITE)
        self.root_app.unbind("<Button-3>")
        self.root_app.canvas.unbind("<ButtonPress-1>")
        self.root_app.canvas.unbind("<B1-Motion>")
        self.root_app.canvas.unbind("<ButtonRelease-1>")

class Curso_coord(ctk.CTkLabel):
    def __init__(self, parent,text):
        super().__init__(master=parent, textvariable = text)
        self.pack(side = 'bottom')

class PostionPanel(Panel):
    def __init__(self, parent_app,root_app):
        super().__init__(parent = parent_app)
        self.root_app = root_app
        label = ctk.CTkLabel(self,text="position")
        label.pack()

        self.x_var = ctk.IntVar(value=0)
        self.y_var = ctk.IntVar(value=0)
        self.size_var = ctk.DoubleVar(value=1)

        x_entry = ctk.CTkEntry(self,textvariable = self.x_var,width=50)
        x_entry.pack(side = 'left',padx = 5)
        y_entry = ctk.CTkEntry(self,textvariable= self.y_var,width=50)
        y_entry.pack(side = 'left',padx = 5)
        size_entry = ctk.CTkEntry(self,textvariable= self.size_var,width=50)
        size_entry.pack(side = 'left',padx = 5)

        apply_button = ctk.CTkButton(self,text="apply",width=60,
                                     command = lambda *args: root_app.change_layer_position(self.x_var.get(),
                                                                                            self.y_var.get(),
                                                                                            self.size_var.get()))
        

        reset_button = ctk.CTkButton(self,text="X",width=25,command = self.reset)
        reset_button.pack(side = 'right',padx = 5)
        apply_button.pack(side = 'right',padx = 5)

    def reset(self):
        self.x_var.set(0)
        self.y_var.set(0)
        self.size_var.set(1)
        self.root_app.reset_layer_position()
        
class CurveToolPanel(Panel):
    def __init__(self, parent_app,root_app):
        super().__init__(parent = parent_app)

        self.root_app = root_app
        self.root_layer = self.root_app.current_layer
        self.canvas_width = 200
        self.canvas_height = 200
        self.canvas = tk.Canvas(self,width=self.canvas_width,height=self.canvas_height,background=BACKGROUND_COLOR,)
        self.canvas.pack(fill='both',padx=15,pady=15)

        self.root_app.curvetool = self
        for point in self.root_app.control_points:
            radius = 5
            self.canvas.create_oval(point[0] - radius, point[1] - radius, point[0] + radius, point[1] + radius, fill=WHITE)
        self.canvas.bind('<Configure>',self.update_canvas_info)
        self.canvas.bind("<Button-1>", self.left_click)

    def update_canvas_info(self,event=None):
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        
        self.draw_screen()
        


    def draw_screen(self):
        self.canvas.delete('all')
        self.root_app.control_points = sorted(self.root_app.control_points)
        self.points_coord = []
        for point in self.root_app.control_points:
            self.points_coord.append((int(point[0]*self.canvas_width),
                                      int(self.canvas_height - point[1]*self.canvas_height))) 
        for point in self.points_coord:
            radius = 5
            self.canvas.create_oval(point[0] - radius, point[1] - radius, point[0] + radius, point[1] + radius, fill=WHITE)
        self.canvas.create_line(*self.points_coord,smooth=True,width=2,fill=WHITE)

    def left_click(self,event):
        for point in range (len(self.points_coord)-1):
            if self.calculate_distance( (event.x,event.y),self.points_coord[point]) <5:
                self.select_point = point
                self.canvas.bind("<B1-Motion>", self.move)
                self.canvas.bind('<ButtonRelease-1>', self.end_move)



    def move(self,event):
        self.root_app.control_points[self.select_point] = (min(max(event.x/self.canvas_width,0),1),
                                                  min(max((self.canvas_height-event.y)/self.canvas_height,0),1))
        self.root_app.manipulate_image(self.root_layer)
        self.draw_screen()
    def end_move(self,event):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind('<ButtonRelease-1>')

    def calculate_distance(self,point_1, point_2):
        distance = math.sqrt((point_2[0] - point_1[0])**2 + (point_2[1] - point_1[1])**2)
        return distance
    
class SaveButton(ctk.CTkButton):
    def __init__(self,parent,export_image,name_string,file_string,path_string):
        super().__init__(master=parent,text='save',command= self.save)
        self.pack(side = 'bottom',pady = 10)
        self.export_image = export_image
        self.name_string = name_string
        self.file_string = file_string
        self.path_string = path_string

    def save(self):
        self.export_image(
            self.name_string.get(),
            self.file_string.get(),
            self.path_string.get()
        )
                
class FileNamePanel(Panel):
    def __init__(self, parent,name_string,file_string):
        super().__init__(parent = parent)
        self.name_string = name_string
        self.name_string.trace('w',self.update_text)
        self.file_string = file_string
        ctk.CTkEntry(self,textvariable=self.name_string).pack(fill = 'x',padx = '20',pady= 5)

        frame = ctk.CTkFrame(self,fg_color='transparent')
        jpg_check = ctk.CTkCheckBox(frame,text = 'jpg',command= lambda: self.click('jpg'),  variable= self.file_string, onvalue= 'jpg',offvalue = 'png')
        jpg_check.pack(side = 'left',fill = 'x',expand =True)
        png_check = ctk.CTkCheckBox(frame,text = 'png',command= lambda: self.click('png'),  variable= self.file_string, onvalue= 'png', offvalue= 'jpg')
        png_check.pack(side = 'left',fill = 'x',expand =True)
        frame.pack(expand = True,fill = 'x',padx= 20)

        self.output = ctk.CTkLabel(self, text = '')
        self.output.pack()

    def click(self,value):
        self.file_string.set(value)
        self.update_text()

    def update_text(self,*args):
        if self.name_string.get():
            text = self.name_string.get().replace(' ','_') +'.'+ self.file_string.get()
            self.output.configure(text = text)

class FilePathPanel(Panel):
    def __init__(self,parent,path_string):
        super().__init__(parent = parent)
        self.path_string = path_string

        ctk.CTkButton(self,text= ' Open ',command=self.open_file_dialog).pack(pady =5)
        ctk.CTkEntry(self,textvariable=self.path_string).pack(expand= True,fill = 'both',padx = 5,pady = 5)

    def open_file_dialog(self):
        self.path_string.set(filedialog.askdirectory())

class LayerPanel(ctk.CTkFrame):
    def __init__(self, parent_app,layer):
        super().__init__(master = parent_app)

        root_app = parent_app.root_app
        name = ctk.StringVar(value=layer.name)
        self.pack(fill = 'x',side = 'bottom',pady = 4,ipady = 8,padx = 5)
        self.Label = ctk.CTkEntry(self,textvariable=name,width=100)
        self.Label.pack(side = "left")
        

        self.delete_button = ctk.CTkButton(self,text= "X", width=20,height=20,
                                           command = lambda *args: root_app.delete_layer(layer))
        self.delete_button.pack(side = "right") 
        
        self.select_button = ctk.CTkButton(self,text= "O", width=20,height=20,
                                           command = lambda *args: root_app.change_current_layer(root_app.current_layer,layer))
        self.select_button.pack(side = "right")

        self.copy_button = ctk.CTkButton(self,text= "+", width=20,height=20,
                                           command = lambda *args: root_app.duplicate_layer(layer))
        self.copy_button.pack(side = "right")

        self.down_button = ctk.CTkButton(self,text= "↓", width=20,height=20,
                                           command = lambda *args: root_app.move_layer_down(layer))
        self.down_button.pack(side = "right")

        self.up_button = ctk.CTkButton(self,text= "↑", width=20,height=20,
                                           command = lambda *args: root_app.move_layer_up(layer))
        self.up_button.pack(side = "right")

class TextLayerPanel(ctk.CTkFrame):
    def __init__(self, parent_app,layer):
        super().__init__(master = parent_app,fg_color="#1d3054")

        root_app = parent_app.root_app
        name = ctk.StringVar(value=layer.name)
        self.pack(fill = 'x',side ='bottom',pady = 4,ipady = 8,padx = 5)
        self.Label = ctk.CTkEntry(self,textvariable=name,width=100)
        self.Label.pack(side = "left")
        

        self.delete_button = ctk.CTkButton(self,text= "X", width=20,height=20,
                                           command = lambda *args: root_app.delete_layer(layer))
        self.delete_button.pack(side = "right") 
        
        self.select_button = ctk.CTkButton(self,text= "O", width=20,height=20,
                                           command = lambda *args: root_app.change_current_text_layer(root_app.current_text_layer,layer))
        self.select_button.pack(side = "right")

        self.copy_button = ctk.CTkButton(self,text= "+", width=20,height=20,
                                           command = lambda *args: root_app.duplicate_text_layer(layer))
        self.copy_button.pack(side = "right")

        self.down_button = ctk.CTkButton(self,text= "↓", width=20,height=20,
                                           command = lambda *args: root_app.move_layer_down(layer))
        self.down_button.pack(side = "right")

        self.up_button = ctk.CTkButton(self,text= "↑", width=20,height=20,
                                           command = lambda *args: root_app.move_layer_up(layer))
        self.up_button.pack(side = "right")
        

class FilterPanel(ctk.CTkFrame):
    def __init__(self, parent_app,name,funtion,from_value,to_value):
        super().__init__(master = parent_app)
        self.pack()
        var = ctk.IntVar(value=0)
        ctk.CTkLabel(self,text=name).pack()
        slider = ctk.CTkSlider(self,variable=var,from_=from_value,to=to_value)
        slider.pack(side= 'left',pady = 8,padx = 5)
        button = ctk.CTkButton(self,textvariable=var,
                                          command = lambda *args: funtion(var.get()))
        button.pack(side = 'left',pady = 8,padx = 5)





        