import time
import tkinter 
import os
from tkinter import StringVar
import shutil
import pathlib
move_dir = True
search_mod = False
#window_settings
window_color = "#191919"
window = tkinter.Tk()
window.geometry("900x900")
window.configure(background=window_color)
#end of screen settings
#fonts
FONT = ("Segoe UI Variable", 15)
font_bottom  = ("Segoe UI Variable", 10)
SMALL_FONT = ("Segoe UI Variable", 13)
#imgs
image_home = tkinter.PhotoImage(file=r"imgs\home.png")
image_sep = tkinter.PhotoImage(file=r"imgs\seperetor.png")
image_desktop = tkinter.PhotoImage(file=r"imgs\desktop.png")
image_documents = tkinter.PhotoImage(file=r"imgs\documents.png")
image_downloads = tkinter.PhotoImage(file=r"imgs\downloads.png")
image_pictures = tkinter.PhotoImage(file=r"imgs\pictures.png")
image_videos = tkinter.PhotoImage(file=r"imgs\videos.png")
image_this_pc = tkinter.PhotoImage(file=r"imgs\this_pc.png")
image_networks = tkinter.PhotoImage(file=r"imgs\networks.png")
image_tools_menu = tkinter.PhotoImage(file=r"imgs\tools_menu.png")
image_new_menu = tkinter.PhotoImage(file=r"imgs\new.png")
selected_color = "#777777"
tools_color = "#1F1F1F"
#technecal
path = os.getcwd()
selected_another = False
var = StringVar()
key_word = ""
show_files_counter = 0
#funcs
def reset_color():
    btn_documents.config(background=window_color)    
    btn_desktop.config(background=window_color)    
    btn_home.config(background=window_color)
    btn_downloads.config(background=window_color)
    btn_pictures.config(background=window_color)
    btn_videos.config(background=window_color)
    btn_this_pc.config(background=window_color)
    btn_networks.config(background=window_color)

def rename_func():
    file_extension = pathlib.Path(path).suffix
    new_word = new_e.get()
    new_word += file_extension
    os.renames(os.path.join(path, selection), os.path.join(path, new_word))    
    redraw()

def rename():
    global new_file_name
    global new_e
    global selection
    selection = folder_listbox.get(folder_listbox.curselection())
    if selection:
        new = tkinter.Tk()
        new.geometry("500x200")
        new.config(background=window_color)
        new_l = tkinter.Label(new, text="rename file", font=FONT, background=window_color, foreground="white")
        new_l.pack(pady=2)
        new_file_name = StringVar()
        new_e = tkinter.Entry(new, font=SMALL_FONT, background=window_color, foreground="white")
        new_e.pack(pady=20)   
        new_e.insert(tkinter.END, selection)        
        new_l2 = tkinter.Label(new, font=SMALL_FONT, text=path, background=window_color, foreground="white")
        new_l2.pack()
        new_b = tkinter.Button(new, text="rename", font= FONT, width=7, height=1, background="green", foreground="white", command=lambda: [rename_func(), new.destroy()])
        new_b.pack()
        new.mainloop()
    
def show_size():
    selection = folder_listbox.get(folder_listbox.curselection())
    if selection:
        text = (" " + str(len(os.listdir(path))) + " items |")
        label_bottom.config(text=text)


def change_operation_time(elapsed_time):
    directory_text_box.config(state="normal")
    directory_text_box.delete("1.0","end")
    url = "The operation took: " + str(elapsed_time) + " seconds"
    directory_text_box.insert(tkinter.END, url)        
    directory_text_box.config(state=tkinter.DISABLED) 
def search(*args):
    start = time.time()
    global key_word
    global search_mod
    global counter_S
    counter_S = 0
    folder_listbox.delete(0, tkinter.END)
    key_word = (var.get()).lower()
    with open(r"hash.txt", 'r') as fp:
        lines = fp.readlines()
        for line in lines:
            line_word = (line.strip()).split("\\")
            search_word = line_word[-1].lower()
            if search_word.find(key_word) != -1:
                counter_S+=1
                new_line = line[:-1]
                folder_listbox.insert(tkinter.END, new_line)
        search_mod = True
        end = time.time()
        elapsed_time = end - start
        change_operation_time(elapsed_time)
        change_bottom_text()
        
def url_change():    
        directory_text_box.config(state="normal")
        directory_text_box.delete("1.0","end")
        url = path.replace("\\", " > ")
        directory_text_box.insert(tkinter.END, url)        
        directory_text_box.config(state=tkinter.DISABLED)

def change_bottom_text():
    global search_mod
    if search_mod:
        text = (" " + str(counter_S) + " items |")
        label_bottom.config(text=text)
    else:
        text = (" " + str(len(os.listdir(path))) + " items |")
        label_bottom.config(text=text)

def redraw():
    url_change()
    if path:
        global search_mod
        search_mod = False
        change_bottom_text()
        folder_listbox.delete(0, tkinter.END)  # Clear previous list
        for item in os.listdir(path):
            folder_listbox.insert(tkinter.END, item)

def prev():
    global path
    path = (os.path.abspath(os.path.join(path, os.pardir)))
    redraw()
def create():
    global new_e
    global new_file_name
    new_word = new_e.get()
    os.mkdir(os.path.join(path, new_word))    
    redraw()
    with open(r"hash.txt", "a") as text_file:    
        text_file.write(os.path.join(path, new_word) + '\n')
    
def new():
    global new_file_name
    global path
    global new_e
    new = tkinter.Tk()
    new.geometry("500x200")
    new.config(background=window_color)
    new_l = tkinter.Label(new, text="new file", font=FONT, background=window_color, foreground="white")
    new_l.pack(pady=2)
    new_file_name = StringVar()
    new_e = tkinter.Entry(new, font=SMALL_FONT, background=window_color, foreground="white")
    new_e.pack(pady=20)
    new_l2 = tkinter.Label(new, font=SMALL_FONT, text=path, background=window_color, foreground="white")
    new_l2.pack()
    new_b = tkinter.Button(new, text="create", font= FONT, width=7, height=1, background="green", foreground="white", command=lambda: [create(), new.destroy()])
    new_b.pack()
    new.mainloop()

def copy():
    global path
    global selection
    global copy_src
    selection = folder_listbox.get(folder_listbox.curselection())
    if selection:
        copy_src = os.path.join(path, selection)

def paste():
    global path
    global copy_src
    copy_dst = path
    try: 
        shutil.copy2(copy_src, copy_dst)
    except:
        shutil.copy(copy_src, copy_dst)
    redraw()

def delete():
        
    selection = folder_listbox.get(folder_listbox.curselection())
    if selection:
        try:
            shutil.rmtree(os.path.join(path, selection))
            
            
            redraw()
        except:
            os.remove(os.path.join(path, selection))             
            redraw()

def what_file_extention():
    global path
    if os.path.isdir(path):
       global search_mod
       search_mod = False
       change_bottom_text()
       folder_listbox.delete(0, tkinter.END)  # Clear previous list 
       url_change()
       for item in os.listdir(path):
                    folder_listbox.insert(tkinter.END, item)
    else:
        try:
            os.startfile(path)
            path = (os.path.abspath(os.path.join(path, os.pardir)))
        except:
            directory_text_box.config(state="normal")
            directory_text_box.delete("1.0","end")
            error_message = "Error: file is not found: 404"
            directory_text_box.insert(tkinter.END, error_message)        
            directory_text_box.config(state=tkinter.DISABLED)
            path = (os.path.abspath(os.path.join(path, os.pardir)))


def select_btn_home():
    global path
    global selected_another
    if selected_another == False:
        btn_home.config(background=selected_color)
        path = r"Home"
        redraw()
        selected_another = True
    else:
        reset_color()
        btn_home.config(background=selected_color)
        path = r"Home"
        redraw()

def selected_btn_desktop():

    global path
    global selected_another
    if selected_another == False:
        btn_desktop.config(background=selected_color)
        selected_another = True
        path = "Desktop"
        redraw()
    else:
        reset_color()
        btn_desktop.config(background=selected_color)
        path = "Desktop"
        redraw()    

def selected_btn_docs():
    global path
    global selected_another
    if selected_another == False:
        btn_documents.config(background=selected_color)
        selected_another = True
        path = "Documents"
        redraw()
    else:
        reset_color()
        btn_documents.config(background=selected_color)
        path = "Documents"
        redraw()
def selected_btn_downlaods():
    global path
    global selected_another
    if selected_another == False:
        btn_downloads.config(background=selected_color)
        selected_another = True
        path = "Downloads"
        redraw()
    else:
        reset_color()
        btn_downloads.config(background=selected_color)
        path = "Downloads"
        redraw()    
def selected_btn_videos():
    global path
    global selected_another
    if selected_another == False:
        btn_videos.config(background=selected_color)
        selected_another = True
        path = "Videos"
        redraw()
    else:
        reset_color()
        btn_videos.config(background=selected_color)
        path = "Videos"
        redraw()    
def selected_btn_pictures():
    global path
    global selected_another
    if selected_another == False:
        btn_pictures.config(background=selected_color)
        selected_another = True
        path = "Pictures"
        redraw()
    else:
        reset_color()
        btn_pictures.config(background=selected_color)
        path = "Pictures"
        redraw()
def selected_btn_this_pc():
    global path
    global selected_another
    if selected_another == False:
        btn_this_pc.config(background=selected_color)
        selected_another = True
        path = r"C:/"
        redraw()
    else:
        reset_color()
        btn_this_pc.config(background=selected_color)
        path = r"C:/"
        redraw()
def selected_btn_networks():
   
    global selected_another
    if selected_another == False:
        btn_networks.config(background=selected_color)
        selected_another = True
    else:
        reset_color()
        btn_networks.config(background=selected_color)
#frames    
frame_top_first = tkinter.Frame(master=window, width=1000, height=46, background=tools_color)
frame_top_first.pack()

btn_new = tkinter.Button(master=frame_top_first, image=image_new_menu, background=tools_color, border=0)
btn_new.pack(side="left")

label_tools_menu = tkinter.Label(master=frame_top_first, image=image_tools_menu, background=tools_color)
label_tools_menu.pack(side="right")

frame_top_second = tkinter.Frame(master=window, width=1000, height=46, background=window_color)
frame_top_second.pack(side="top")

frame_bottom = tkinter.Frame(window, bg=window_color)
frame_bottom.pack(side="bottom", fill="x")

frame_left = tkinter.Frame(master=window, width=201, height=945, background=window_color)
frame_left.pack(side="left")


frame_center = tkinter.Frame(master=window, width=201, height=580, background="white")
frame_center.pack(fill="both", side="top", expand=True)


folder_listbox = tkinter.Listbox(frame_center, bg=window_color, foreground="white",font=FONT, highlightthickness=0, borderwidth=0)
folder_listbox.pack(expand = True, fill = "both", side="top")


#window_color
frame_left_top = tkinter.Frame(master=frame_left, width=201, background=window_color)
frame_left_top.pack(side="top")


btn_home = tkinter.Button(master=frame_left_top,image=image_home, background=window_color, border="0", command = select_btn_home)
btn_home.pack()


label_sep = tkinter.Label(master=frame_left_top, image=image_sep, border="0")
label_sep.pack()

btn_desktop = tkinter.Button(master=frame_left_top,image=image_desktop, background=window_color, border="0", command=  selected_btn_desktop)
btn_desktop.pack(side = "top")



btn_documents = tkinter.Button(master=frame_left_top,image=image_documents, background=window_color, border="0", command = selected_btn_docs)
btn_documents.pack(side = "top")


btn_downloads = tkinter.Button(master=frame_left_top,image=image_downloads, background=window_color, border="0", command = selected_btn_downlaods)
btn_downloads.pack(side = "top")



btn_pictures = tkinter.Button(master=frame_left_top,image=image_pictures, background=window_color, border="0", command = selected_btn_pictures)
btn_pictures.pack(side = "top")




btn_videos = tkinter.Button(master=frame_left_top,image=image_videos, background=window_color, border="0", command = selected_btn_videos)
btn_videos.pack(side = "top")


label_sep_2 = tkinter.Label(master=frame_left_top, image=image_sep, border="0")
label_sep_2.pack(side = "top")



btn_this_pc = tkinter.Button(master=frame_left_top,image=image_this_pc, background=window_color, border="0", command = selected_btn_this_pc)
btn_this_pc.pack(side = "top")




btn_networks = tkinter.Button(master=frame_left_top,image=image_networks, background=window_color, border="0", command = selected_btn_networks)
btn_networks.pack(side = "top")



lebel_unuseful = tkinter.Label(master=frame_left_top, background=window_color)
lebel_unuseful.pack(pady=188)

#1C1C1C
label_bottom = tkinter.Label(master=frame_bottom, background="#1C1C1C", foreground="#DDDDDD", text=len(os.listdir(path)), font=font_bottom)
label_bottom.pack(side="left", fill="x")

image_prev = tkinter.PhotoImage(file=r"imgs\prev.png")
image_back = tkinter.PhotoImage(file=r"imgs\back.png")
image_forward = tkinter.PhotoImage(file=r"imgs\forward.png")
image_prev_options = tkinter.PhotoImage(file=r"imgs\prev_options.png")



btn_back = tkinter.Button(frame_top_second,image=image_back, bg=window_color, command=prev, border="0")
btn_back.pack(side="left", pady=5)


btn_forward = tkinter.Button(frame_top_second,image=image_forward, bg=window_color, command=prev, border="0")
btn_forward.pack(side="left", pady=5)
btn_prev_options = tkinter.Button(frame_top_second,image=image_prev_options, bg=window_color, command=prev, border="0")
btn_prev_options.pack(side="left", pady=5)




btn_prev = tkinter.Button(frame_top_second,image=image_prev, bg=window_color, command=prev, border="0")
btn_prev.pack(side="left", pady=5)


search_bar = tkinter.Entry(frame_top_second, width=15, textvariable=var, background=window_color, foreground="white", font=FONT)
search_bar.pack(side="right", pady=5)


directory_text_box = tkinter.Text(frame_top_second, width=120, height=1, bg= window_color, font=FONT, foreground="white")
directory_text_box.pack(side="left", padx=10, pady=5)




  
def selectfirst_tab(event):
    folder_listbox.select_set(0)


def show_files_enter(event):
    global path
    selection = folder_listbox.get(folder_listbox.curselection())
    if selection:
            if move_dir:
                selected_path = os.path.join(path, selection)
                path = selected_path
                what_file_extention()

def directory_show(event):
    global directory_text_box    
    directory_text_box.config(state="normal")
    directory_text_box.delete("1.0","end")
    directory_text_box.insert(tkinter.END, path)        
    directory_text_box.config(state=tkinter.DISABLED)



m = tkinter.Menu(folder_listbox, tearoff = 0)
m.add_command(label ="delete", command=delete)
m.add_command(label ="rename", command=rename)
m.add_command(label="new", command=new)
m.add_command(label="copy", command=copy)
m.add_command(label="paste", command=paste)

def do_popup(event):
	try:
		m.tk_popup(event.x_root, event.y_root)
	finally:
		m.grab_release()



def convert_bytes(size):
    """ Convert bytes to KB, or MB or GB"""
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0








def change_bottom_text_event(event):
    global label_bottom
    global path
    selected_path_file = folder_listbox.get(folder_listbox.curselection())
    path_size = os.path.join(path, selected_path_file)
    if os.path.isfile(path_size):
        f_size = os.path.getsize(path_size)
        x = convert_bytes(f_size)
        text = (" " + str(len(os.listdir(path))) + " items | 1 item selected " + x + " |")
        label_bottom.config(text=text) 
    else:
        text = (" " + str(len(os.listdir(path))) + " items |")
        label_bottom.config(text=text)



   


folder_listbox.bind("<Button-3>", do_popup)
folder_listbox.bind("<Double-Button-1>", show_files_enter)
folder_listbox.bind("<Key-space>", show_files_enter)
folder_listbox.bind("<Return>", show_files_enter)
folder_listbox.bind("<BackSpace>",lambda event: prev())
search_bar.bind("<Return>", search)
directory_text_box.bind("<Button-1>", directory_show)
folder_listbox.bind("<<ListboxSelect>>", change_bottom_text_event)
redraw()










window.mainloop()