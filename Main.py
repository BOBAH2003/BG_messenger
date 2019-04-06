import tkinter as tk
from time import sleep

from threading import Thread

import client_pc


class Main(tk.Frame): # основное рабочее окно
    back_color = '#5B5B5B'
    wid_color = '#757575'
    text_color = 'white'
    message = None
    id = None
    x = None
    y = None
    def __init__(self, root):
        super().__init__(root)

        self.init_main()

    def init_main(self):
        # ---создаем и отрисовываем главные рабочие области окна-------
        Main.main_board = tk.Frame(bg=Main.back_color, height=int(Main.y / 20), bd=5)
        Main.society_board = tk.Frame(bg='#E8E8E8', width=int(Main.x / 6.12), bd=5)
        Main.send_board = tk.Frame(bg='#E8E8E8', height=int(Main.y / 6), width=int(Main.x / 2), bd=5)
        Main.message_board = tk.Frame(bg='#E8E8E8', height=int(Main.y / 2.25), width=int(Main.x / 2))

        # ---создаем кнопки, которые будут вызываться вне класса-------
        Main.new_message_but = tk.Button(Main.main_board, text='создать диалог', bg='#5B5B5B'
            , fg='white', height=2, bd=3, command=Message)
        Main.login_but = tk.Button(Main.main_board,text='Вход', width=6, bg='#5B5B5B', fg='white', height=2, bd=3,
            command=WindowLogin)

        # ---все для отправки сообщений---------------------------------
        Main.send_text = tk.Text(Main.send_board, bg='#E8E8E8', width=int(Main.x / 20))

        self.image = tk.PhotoImage(file='send.png')
        Main.send_but = tk.Button(Main.send_board, image=self.image,
                            height=32, width=32, bd=0,
                            command=lambda : Message.send_mes(None))

        # ---отрисовываем все необходимое------------------------------

        Main.main_board.pack(side=tk.TOP, fill=tk.X)
        Main.main_board.pack_propagate(False)

        Main.society_board.pack(side=tk.LEFT, fill=tk.Y)
        Main.society_board.pack_propagate(False)

        Main.send_board.pack(side=tk.BOTTOM, anchor='e')
        Main.send_board.pack_propagate(False)

        Main.message_board.pack(anchor='e')
        Main.message_board.pack_propagate(False)

        Main.login_but.pack(side=tk.RIGHT, padx=5)


class Message(tk.Toplevel): # все, что связанно с сообщениями.
    saved_id = None # id пользователя с которым в данный момент ведется переписка.
    def __init__(self):
        super().__init__(root)

        self.window()

    def window(self): # диалоговое окно создания диалога.
        self['bg'] = Main.back_color
        self.geometry('{0}x{1}+{2}+{3}'.format(str(int(Main.x / 4.5)),
                    str(int(Main.y/4)), str(int(Main.x / 3)), str(int(Main.y / 3))))
        self.resizable(False, False)
        self.focus_set()
        self.grab_set()

        self.create = tk.Button(self, text='Создать',
                            bg=Main.wid_color,
                            fg=Main.text_color,
                            command=self.create_button)
        self.close = tk.Button(self, text='Отмена',
                            bg=Main.wid_color,
                            fg=Main.text_color,
                            command=self.destroy)

        self.id_input = tk.Entry(self, bg=Main.wid_color, fg=Main.text_color)
        self.name_input = tk.Entry(self, bg=Main.wid_color, fg=Main.text_color)

        tk.Label(self,text='ID пользователя(5 знаков):', bg=Main.back_color, fg=Main.text_color).pack(pady=int(Main.y/200))
        self.id_input.pack()
        tk.Label(self, text='Имя:', bg=Main.back_color, fg='white').pack(pady=int(Main.y / 200))
        self.name_input.pack()
        self.create.pack(pady=int(Main.y / 200))
        self.close.pack(pady=int(Main.y / 200))

    def create_button(self): # создание контакта
        if client_pc.id_request(self.id_input.get()) == 'True':
            Message.society.append(self.id_input.get())
            tk.Button(Main.society_board,
                  text='Контакт:\nИмя: {0}\nID: {1}'.format(self.name_input.get(), self.id_input.get()),
                  bg=Main.wid_color, anchor='w', fg='white',
                  command=lambda id=self.id_input.get():
                  self.draw(id),
                  justify=tk.LEFT).pack(side=tk.TOP, fill=tk.X)
            self.destroy()
        else:
            tk.Label(self, text='Пользователя с таким id\nне существует.',
                     bg=Main.back_color, fg='white').pack()

    def send_mes(self):
        message = str(Main.send_text.get(1.0, tk.END))[0:-1]
        Main.send_text.delete(1.0, tk.END)

        if Message.saved_id != None:
            client_pc.message_send(Main.id, Message.saved_id, message)


    def draw(self=None, id=None):
        if id != None:
            Message.saved_id = str(id)

        if Message.saved_id != None:
            position = {Main.id:'e', Message.saved_id:'w'}
            mess_keeper = list(Main.message['to_me'] + Main.message['from_me'])
            mess_keeper.sort(key=lambda date: date[-19:-9])

            for widget in Main.message_board.winfo_children():
                widget.destroy()

            for message in  mess_keeper:
                if Message.saved_id in message[2:7] or Message.saved_id in message[11:16]:
                    wid_mes = tk.Label(Main.message_board,
                                         text=message[20:-23].replace('\\n', '\n'),
                                         bg='#E8E8E8',
                                         width=int(Main.x / 4.05),
                                         anchor=position[message[2:7]])
                    wid_mes.pack(side=tk.TOP, anchor=position[message[2:7]])


class WindowLogin(tk.Toplevel): # все, что косается входа в акк
    def __init__(self):
        super().__init__(root)

        self.main()

    def main(self): # окно, в котором распологается интерфейс для осуществления входа в аккаунт.
        self.geometry('{0}x{1}+{2}+{3}'.format(str(int(Main.x / 4.5)),
                    str(int(Main.y/4)), str(int(Main.x / 3)), str(int(Main.y / 3))))
        self['bg'] = Main.back_color
        self.resizable(False, False)
        self.focus_set()
        self.grab_set()

        self.log_input = tk.Entry(self, width=30, bg=Main.wid_color, fg=Main.text_color)
        self.pas_input = tk.Entry(self, width=30, show='•', bg=Main.wid_color, fg=Main.text_color)

        self.log_but = tk.Button(self, text='Вход', bg=Main.wid_color,
                                 fg=Main.text_color, width=6, command=self.login)
        self.reg_but = tk.Button(self, text='Регистрация', bg=Main.wid_color,
                                 fg=Main.text_color, width=11, command=self.registration)
        self.exit_but = tk.Button(self, text='Отмена', bg=Main.wid_color,
                                  fg=Main.text_color, width=6, command=lambda: self.destroy())

        tk.Label(self, text='Логин:', anchor='w', bg=Main.back_color,
                 fg=Main.text_color, width=6).pack(side=tk.TOP, anchor='w', padx=int(Main.x / 40), pady=int(Main.y / 400))
        self.log_input.pack(side=tk.TOP, anchor='w', padx=int(Main.x / 40))

        tk.Label(self, text='Пароль:', anchor='w', bg=Main.back_color,
                 fg = Main.text_color, width=6).pack(side=tk.TOP, anchor='w', padx=int(Main.x / 40), pady=int(Main.y / 400))
        self.pas_input.pack(side=tk.TOP, anchor='w', padx=int(Main.x / 40))

        self.log_but.pack(pady=int(Main.y / 200))
        self.reg_but.pack()
        self.exit_but.pack(pady=int(Main.y / 200))


    def login(self): # проверка данных пользователя для входа.
        Main.id = client_pc.login(self.log_input.get(), self.pas_input.get())

        if Main.id != False:
            Main.new_message_but.pack(side=tk.RIGHT, padx=3)
            Main.login_but['text'] = str(Main.id) + '\nВыход'
            Main.login_but['command'] = self.exit

            Thread(target=self.check_message).start() # постоянное обновление сообщений.

            Main.send_text.pack(side=tk.LEFT)
            Main.send_but.pack(side=tk.TOP, anchor='w', padx=5)

            self.destroy()
        else:
            tk.Label(self, text='Неправильный логин или пароль,\nповторите попытку.',
                     bg=Main.back_color, fg=Main.text_color, width=26).pack(side=tk.TOP,
                     padx=int(Main.x / 40), pady=int(Main.y / 400))
            self.log_input.delete(0, tk.END)
            self.pas_input.delete(0, tk.END)

    def exit(self): # выход из акк
        Main.id = None
        for widget in Main.message_board.winfo_children():
            widget.destroy()
        for widget in Main.society_board.winfo_children():
            widget.destroy()
        Main.new_message_but.pack_forget()
        Main.login_but['text'] = 'Вход'
        Main.login_but['command'] = WindowLogin

    def check_message(self): # обновление сообщений
        sum_message = 0
        Message.society = []
        while True:
            try:
                Main.message = client_pc.message_request(Main.id)

                for message in Main.message['to_me']:
                    if message[2:7] not in str(Message.society):
                        Message.society.append(message[2:7])
                        tk.Button(Main.society_board,
                            text='Контакт:\nИмя: ???\nID: {0}'.format(message[2:7]),
                            bg=Main.wid_color, anchor='w', fg='white',
                            justify=tk.LEFT,
                            command=lambda id=message[2:7]:Message.draw(id=id)).pack(side=tk.TOP, fill=tk.X)

                for message in Main.message['from_me']:
                    if message[11:16] not in str(Message.society):
                        Message.society.append(message[11:16])
                        tk.Button(Main.society_board,
                            text='Контакт:\nИмя: ???\nID: {0}'.format(message[11:16]),
                            bg=Main.wid_color, anchor='w', fg='white',
                            justify=tk.LEFT,
                            command=lambda id=message[11:16]:Message.draw(id=id)).pack(side=tk.TOP, fill=tk.X)

                if len(str(Main.message.values())) > sum_message: # проверка на наличие НОВЫХ сообщений
                    Message.draw()
                    sum_message = len(str(Main.message.values()))

                if len(Main.main_board.winfo_children()) == 0: # закрытие потока, если главное окно закрывается
                    break

                sleep(1)

            except:
                break



    def registration(self): # регистрация
        self.label_info = tk.Label(self, text='Введите данные в поля регистрации\n и кликните по кнопке еще раз.',
                                   bg=Main.back_color, fg=Main.text_color).pack(side=tk.TOP)
        self.reg_but['command'] = lambda login = self.log_input.get(),\
            password = self.pas_input.get(): client_pc.registration(login, password)


if __name__ == '__main__':
    root = tk.Tk()
    Main.x = root.winfo_screenwidth()
    Main.y = root.winfo_screenheight()
    app = Main(root)
    app.pack()
    root.geometry('{0}x{1}+{2}+{3}'.format(str(int(Main.x/3*2)),
                str(int(Main.y/3*2)), str(int(Main.x/6)), str(int(Main.y/6))))
    root.title('VG-messenger(v0.2)')
    root.resizable(False, False)
    root['bg'] = Main.back_color
    root.configure(bg=Main.back_color)
    root.mainloop()
