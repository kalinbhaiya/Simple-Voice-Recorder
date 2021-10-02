# TODO : Creating a simple voice recorder

from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as file
import webbrowser as wb
import sounddevice as sd
from scipy.io.wavfile import write
import os
import threading
import humanfriendly


time2=1
class Sound_Recorder:
    def __init__(self,master):
        self.master = master
        ttk.Style().theme_use('vista')

        self.geometry = master.geometry('400x200')
        self.title = master.title('VoiceRecorder')
        self.background = master.config(background='white')
        self.label = ttk.Label(master, text='Welcome To Voice Recorder!', font='curive 15 bold italic',
                               foreground='aqua', background='white').pack()
        self.label2 = ttk.Label(master, text='Enter The Duration Of The Recording Here : ', foreground='black',
                                background='white', font='curisve 12 bold').place(x=5, y=50)
        self.label3 = ttk.Label(master, text='Status : ', font='cursive 15 bold', foreground='blue',
                                background='white').place(x=120, y=100)
        self.label4 = ttk.Label(master, text='Waiting...', font='cursive 15 bold italic', foreground='red',
                                background='white')
        self.label4.place(x=200, y=100)

        self.entry = ttk.Entry(master,width=8)
        self.entry.place(x=340,y=52)

        style = ttk.Style()
        self.record_button = ttk.Button(master,text='Record',style='xd.TButton',command=self.timer)
        self.record_button.pack(side=BOTTOM)
        self.record_button.bind('<Button-1>', self.bind_function)
        style.configure(style='xd.TButton',font=('cursive',15,'bold','italic'),foreground='red',background='yellow')
        style.map(style='xd.TButton',foreground=[('active','blue')],background=[('active','red')])

        self.menu_bar = Menu(master)
        self.menu = Menu(self.menu_bar,tearoff=0)
        self.menu.add_command(label='Credits',command=self.credits)
        self.menu.add_command(label='About',command=self.about)
        self.menu.add_command(label='Instructions',command=self.instructions)
        self.menu_bar.add_cascade(menu=self.menu,label='Help')
        self.menu2 = Menu(self.menu_bar,tearoff=0)
        self.menu3 = Menu(self.menu_bar,tearoff=0)
        self.menu3.add_command(label='Exit',command=self.exit1)
        self.menu_bar.add_cascade(label='App',menu=self.menu3)
        self.master.config(menu=self.menu_bar)
        self.master.protocol('WM_DELETE_WINDOW',self.exit1)
        self.master.eval('tk::PlaceWindow . center')

    def exit1(self):
        sys.exit()

    def credits(self):
        messagebox.showinfo('VoiceRecorder','VoiceRecorder App Created By Muhammad Muzammil Alam!')

    def about(self):
        messagebox.showinfo('Viper', "Author : \nMuhammad Muzammil Alam\
                                                    Author's E-mail Address : \nmuzammil.alam231@gmail.com\
                                                    Author's Github Profile : \nhttps://github.com/kalinbhaiya\
                                                    Author's Facebook Profile : \nhttps://www.facebook.com/profile.php?id=100052280166322 Author's Instagram Profile : \nhttps://www.instagram.com/m.muzammil1231/")

        wb.open_new_tab('https://github.com/kalinbhaiya')
        wb.open_new_tab('https://www.facebook.com/profile.php?id=100052280166322')
        wb.open_new_tab('https://www.instagram.com/m.muzammil1231/')

    def instructions(self):
        messagebox.showinfo('VoiceRecorder','Enter the duration of the recording in seconds. Click on \'Record\', and start RECORDING!, Thanks!')

    def bind_function(self,event):
        self.thread()

    def timer(self):
        global time2
        try:
            time1 = int(self.entry.get())
            def countdown():

                time1 = int(self.entry.get())
                if time2>time1:
                    self.set_time_to_1()
                    root.destroy()

                else:
                    formatted_time = humanfriendly.format_timespan(time2)
                    label.config(text=f'Elapsed Time : {formatted_time}',font='curisve 40 bold italic',bg='black',fg='aqua')
                    self.increment_time()
                    label.after(1000, countdown)

            root = Toplevel()
            root.resizable(False, False)
            root.config(background='black')
            label = Label(root, text='')
            label.pack()
            countdown()

        except ValueError:
            messagebox.showerror('VoiceRecorder', 'Please Enter The Time In Seconds (Integers)!')

    def set_time_to_1(self):
        global time2
        time2=1

    def increment_time(self):
        global time2
        time2+=1

    def record(self):
        self.label4.config(text='Recording...')
        time = self.entry.get()
        if time=='':
            messagebox.showerror('VoiceRecorder','Please Select The Duration For The Recording!')
            self.label4.config(text='Waiting...')

        else:
            if str(time).isnumeric():

                try:
                    final_time = int(time)
                    freq = 44100
                    duration = final_time
                    recording = sd.rec(int(duration * freq),
                                       samplerate=freq, channels=2)
                    sd.wait()
                    path = file.asksaveasfilename(filetypes=[('All Files','*.wav')],defaultextension='.wav')
                    write(path,freq,recording)
                    ques = messagebox.askquestion('VoiceRecorder','Your recording has been completed!. Do you want to listen the recording?')
                    if ques=='yes':
                        os.startfile(path)
                    else:
                        pass
                    self.label4.config(text='Waiting...')

                except ValueError:
                    messagebox.showerror('VoiceRecorder','Please Enter The Time In Seconds (Integers)!')
                    self.label4.config(text='Waiting...')

                except FileNotFoundError:
                    self.label4.config(text='Waiting...')

    def thread(self):
        thread = threading.Thread(target=self.record)
        thread.start()

window = Tk()
Sound_Recorder(window)
window.mainloop()
