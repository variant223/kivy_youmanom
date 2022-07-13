import sqlite3
import datetime
import csv
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.animation import Animation
from kivy.graphics import Color
#from kivymd.uix.list import OneLineListItem
#from kivy.utils import get_color_from_hex
import socket
import json

#Window.size = (300, 500)
#Window.clearcolor = (1, 0, 0, 1)

class MainApp(MDApp):
   global screen_manager
   screen_manager = ScreenManager()
  
   def build(self):
      self.title = "E-MANOMETR"
      self.theme_cls.primary_palette='BlueGray'
    
      screen_manager.add_widget(Builder.load_file("splashScreen.kv"))
      screen_manager.add_widget(Builder.load_file("mainScreen.kv"))
   
      return screen_manager
   
   
   def on_start(self):
      Clock.schedule_once(self.change_screen, 5)
     
     
     
     
   def change_screen(self, dt):
      screen_manager.current = "mainScreen"

global gl_text_server
gl_text_server = '192.168.100.8'  # временно переключение сервера тут localhost
                                # ipconfig для определение IP сервера

class ProfileWindow(Screen):

   #########################
   #Сосздание глобальных переменных
   #########################
   global gl_text_read
   global gl_button_read
   global gl_label_map_read
   global gl_label_data_read

   global gl_text_write
   global gl_text_map_write
   global gl_text_data_write
   global gl_button_write
   global gl_label_update

   global gl_name_server_db
   global gl_button_server_db
#   global gl_text_server
#   global gl_text_server_2



   global dt
   dt = datetime.datetime.now()

   def change_server(self):
      gl_text_server = self.kv_name_server_db.text
      print(gl_text_server) #localhost


   def change_conf(self):
#      global gl_text_server
      if gl_text_server == '192.168.100.8':
         gl_text_write = self.kv_text_write.text
         gl_text_map_write = self.kv_text_map_write.text
         gl_text_data_write = self.kv_text_data_write.text

         ###########################################################################
         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
         sock.connect((gl_text_server, 55007))  # подключемся к серверному сокету
         # key [Код операции, Номер, Место установки, Дата установки ]
         # Код операции: 0-запись, 1-изменение, 2-чтение
         key = ['0', gl_text_write, gl_text_map_write, gl_text_data_write]
         sock.send(json.dumps(key).encode('UTF-8'))
         # sock.send(bytes(send , encoding = 'UTF-8'))  # отправляем сообщение
         # time.sleep(3)
         data = sock.recv(1024)  # читаем ответ от серверного сокета
         key2 = json.loads(data.decode('UTF-8'))
         sock.close()  # закрываем соединение
         print(key2)
         print(key2[1])

         if key2[1] != 'no' and key2[2] != 'no':
            self.kv_label_update.text = str("Данные обновлены")

         else:
            print('Такая запись уже существует')
            self.kv_label_update.text = str("Такой номер существует. Изменить?")

            self.kv_button_write_2.text = str("Подтвердить")
            self.kv_button_write_2.size_hint_y = 0.5

#         self.kv_text_write.text = str(key2[0])
#         self.kv_label_map_write.text = str(key2[1])
#         self.kv_label_data_write.text = str(key2[2])
         #############################################################################

      else:
         gl_text_write = self.kv_text_write.text
         gl_text_map_write = self.kv_text_map_write.text
         gl_text_data_write = self.kv_text_data_write.text
         gl_button_write = self.kv_button_write.text
         gl_label_update = self.kv_label_update.text

         gl_name_server_db = self.kv_name_server_db.text
   #      gl_button_server_db = self.kv_button_server_db.text



         db = sqlite3.connect('test2.db')
         sql = db.cursor()

         sql.execute("""CREATE TABLE IF NOT EXISTS manom(
             number TEXT,
             map TEXT,
             data TEXT,
             time TEXT
             )""")
         db.commit()


         sql.execute(f"SELECT data FROM manom WHERE number = '{gl_text_write}'")
         if sql.fetchone() is None:
             sql.execute(f"INSERT INTO manom VALUES (?, ?, ?, ?)", (gl_text_write, gl_text_map_write, gl_text_data_write, dt))
             db.commit()

             print('Зарегестрировано')
             self.kv_label_update.text = str("Данные обновлены")

         else:
             print('Такая запись уже существует')
             self.kv_label_update.text = str("Такой номер существует. Изменить?")

             self.kv_button_write_2.text = str("Подтвердить")
             self.kv_button_write_2.size_hint_y = 0.5

             for value in sql.execute("SELECT * FROM manom"):
                 print(value[0])

   def change_conf_2(self):
#      global gl_text_server
      if gl_text_server == '192.168.100.8':
         gl_text_write = self.kv_text_write.text
         gl_text_map_write = self.kv_text_map_write.text
         gl_text_data_write = self.kv_text_data_write.text

         ###########################################################################
         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
         sock.connect((gl_text_server, 55007))  # подключемся к серверному сокету
         # key [Код операции, Номер, Место установки, Дата установки ]
         # Код операции: 0-запись, 1-изменение, 2-чтение
         key = ['1', gl_text_write, gl_text_map_write, gl_text_data_write]
         sock.send(json.dumps(key).encode('UTF-8'))
         # sock.send(bytes(send , encoding = 'UTF-8'))  # отправляем сообщение
         # time.sleep(3)
         data = sock.recv(1024)  # читаем ответ от серверного сокета
         key2 = json.loads(data.decode('UTF-8'))
         sock.close()  # закрываем соединение
         print(key2)
         print(key2[1])

         self.kv_label_update.text = str("Данные обновлены")

         self.kv_button_write_2.text = str("")
         self.kv_button_write_2.size_hint_y = 0.0001

      #         self.kv_text_write.text = str(key2[0])
      #         self.kv_label_map_write.text = str(key2[1])
      #         self.kv_label_data_write.text = str(key2[2])
      #############################################################################
      else:

         gl_text_write = self.kv_text_write.text
         gl_text_map_write = self.kv_text_map_write.text
         gl_text_data_write = self.kv_text_data_write.text



         db = sqlite3.connect('test2.db') #отрытие базы данных
         sql = db.cursor() # работа с базой данных
         sql.execute(f"SELECT data FROM manom WHERE number = '{gl_text_write}'")
   #      if sql.fetchone() is None:
   #      sql.execute(f"UPDATE manom VALUES (?, ?, ?, ?)", (gl_text_write, gl_text_map_write, gl_text_data_write, dt))
         sql.execute(f"UPDATE manom SET map = '{gl_text_map_write}', data = '{gl_text_data_write}', time = '{dt}' WHERE number = '{gl_text_write}'")
         db.commit()

         print('Зарегестрировано')
         self.kv_label_update.text = str("Данные обновлены")

         self.kv_button_write_2.text = str("")
         self.kv_button_write_2.size_hint_y = 0.0001


   def change_manom(self):
#      global gl_text_server
      gl_text_read = self.kv_text_read.text
      gl_button_read = self.kv_button_read.text
      gl_label_map_read = self.kv_label_map_read.text
      gl_label_data_read = self.kv_label_data_read.text

      if gl_text_server == '192.168.100.8':
         ###########################################################################
         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
         sock.connect((gl_text_server, 55007))  # подключемся к серверному сокету
         # key [Код операции, Номер, Место установки, Дата установки ]
         # Код операции: 0-запись, 1-изменение, 2-чтение
         key = ['2', gl_text_read, 'Надым', '2013']
         sock.send(json.dumps(key).encode('UTF-8'))
         # sock.send(bytes(send , encoding = 'UTF-8'))  # отправляем сообщение
         # time.sleep(3)
         data = sock.recv(1024)  # читаем ответ от серверного сокета
         key2 = json.loads(data.decode('UTF-8'))
         sock.close()  # закрываем соединение
         print(key2)

         self.kv_text_read.text = str(key2[0])
         self.kv_label_map_read.text = str(key2[1])
         self.kv_label_data_read.text = str(key2[2])
         #############################################################################

      else:
         db = sqlite3.connect('test2.db') #отрытие базы данных
         sql = db.cursor() # работа с базой данных



         sql.execute(f"SELECT number FROM manom WHERE number = '{gl_text_read}'") # чтение базы данных manom сортрованой от новых данных к старым

         if sql.fetchone() is not None:
            sql.execute(f"SELECT * FROM manom WHERE number = '{gl_text_read}'")  # чтение базы данных manom сортрованой от новых данных к старым
            one_result = sql.fetchone()

            print("номер есть")

            self.kv_text_read.text = str(one_result[0])
            self.kv_label_map_read.text = str(one_result[1])
            self.kv_label_data_read.text = str(one_result[2])
         else:
   #         self.kv_text_read.text = str("-")
            self.kv_label_map_read.text = str("-")
            self.kv_label_data_read.text = str("-")
            print("нет номера")


   def change_exp_csv(self):
#      global gl_text_server
      if gl_text_server == '192.168.100.8':
         ###########################################################################
         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
         sock.connect((gl_text_server, 55007))  # подключемся к серверному сокету
         # key [Код операции, Номер, Место установки, Дата установки ]
         # Код операции: 0-запись, 1-изменение, 2-чтение
         key = ['3', '1', 'Надым', '2013']
         sock.send(json.dumps(key).encode('UTF-8'))
         # sock.send(bytes(send , encoding = 'UTF-8'))  # отправляем сообщение
         # time.sleep(3)
         data = sock.recv(1024)  # читаем ответ от серверного сокета
         key2 = json.loads(data.decode('UTF-8'))
         sock.close()  # закрываем соединение
         print(key2)
         with open("Output.csv", mode="a", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
            file_writer.writerow(key2)
#         self.kv_text_read.text = str(key2[0])
#         self.kv_label_map_read.text = str(key2[1])
#         self.kv_label_data_read.text = str(key2[2])
         #############################################################################

      else:
         db = sqlite3.connect('test2.db') #отрытие базы данных
         sql = db.cursor() # работа с базой данных

         for value in sql.execute("SELECT * FROM manom"):
            print(value)
   #         with open("Output4.csv", mode="w", encoding='utf-8') as w_file:
   #            file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
   #            file_writer.writerow(["Номер", "Место установки", "Дата установки", "Время записи"])
   #            file_writer.writerow(value)
            with open("Output.csv", mode="a", encoding='utf-8') as w_file:
               file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
               file_writer.writerow(value)

   def change_inp_csv(self):
      with open("Input.csv", encoding='utf-8') as r_file:
         # Создаем объект reader, указываем символ-разделитель ";"
         file_reader_main = csv.reader(r_file, delimiter=";")
         # Счетчик для подсчета количества строк и вывода заголовков столбцов
         count = 0
         # Считывание данных из CSV файла
         for row_main in file_reader_main:
#            if count == 0:
               # Вывод строки, содержащей заголовки для столбцов
#               print(f'Файл содержит столбцы: {", ".join(row_main)}')
#            else:
            # Вывод строк
            print(f'{row_main[0]} - {row_main[1]} - {row_main[2]} - {row_main[3]}.')

            gl_text_write = self.kv_text_write.text
            gl_text_map_write = self.kv_text_map_write.text
            gl_text_data_write = self.kv_text_data_write.text

            db = sqlite3.connect('test2.db')  # отрытие базы данных
            sql = db.cursor()  # работа с базой данных
            sql.execute(f"SELECT data FROM manom WHERE number = '{row_main[0]}'")
            if sql.fetchone() is None:
               sql.execute(f"INSERT INTO manom VALUES (?, ?, ?, ?)", (row_main[0], row_main[1], row_main[2], row_main[3]))
               db.commit()

               print('Зарегестрировано')
#                  self.kv_label_update.text = str("Данные обновлены")

            else:
#               print('Такая запись уже существует')
#                  self.kv_label_update.text = str("Такой номер существует. Изменить?")
               sql.execute(f"UPDATE manom SET map = '{row_main[1]}', data = '{row_main[2]}', time = '{row_main[3]}' WHERE number = '{row_main[0]}'")
               db.commit()




MainApp().run()
