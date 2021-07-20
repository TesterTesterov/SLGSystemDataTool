import locale
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ctypes
import threading

from SLG_Images import SLG_Images_tig
from SLG_Images import SLG_Images_tic
from SLG_Images import SLG_Images_TIM
from SLG_Images import SLG_Images_alb
from SLG_Images import SLG_ImagesError
from SLG_Audio import SLG_Audio_VOI
from SLG_Audio import SLG_AudioError
from SLG_Archives import SLG_Archives_szs
from SLG_Archives import SLG_Archives_SFP
from SLG_Archives import SLG_ArchivesError


class SLG_GUI():
    top_name_lib = {
        "eng": "SLGSystemDataTool by Tester",
        "rus": "SLGSystemDataTool от Tester-а"
    }
    strings_lib = {
        "eng": (
            "РУССКИЙ",
            "ENGLISH",

            "Main section",
            "szs archives",
            "SFP archives (.SPD + .SPL)",
            "tig images",
            "tic images",
            "TIM images",
            "alb images",
            "VOI audio",
        ),
        "rus": (
            "РУССКИЙ",
            "ENGLISH",

            "Главный раздел",
            "Архивы szs",
            "Архивы SFP (.SPD + .SPL)",
            "Картинки tig",
            "Картинки tic",
            "Картинки TIM",
            "Картинки alb",
            "Аудио VOI",
        )
    }
    _top_relief_lib = {
        "eng": (
            tk.RAISED,
            tk.SUNKEN
        ),
        "rus": (
            tk.SUNKEN,
            tk.RAISED
        )
    }
    def __init__(self):
        self._window = tk.Tk()
        self._width = 600
        self._height = 400
        self._possible_versions = [0, 1]
        self._lang = self._define_language()
        self._currentPanel = 0
        self._window.geometry('{}x{}+{}+{}'.format(
            self._width,
            self._height,
            self._window.winfo_screenwidth() // 2 - self._width // 2,
            self._window.winfo_screenheight() // 2 - self._height // 2))
        self._window.resizable(width=False, height=False)
        self._window["bg"] = 'grey'


        self._topButtons = []
        self._topButtons.append(tk.Button(master=self._window,
                                           command=self.toRussian,
                                           relief=tk.RAISED,
                                           font=('Helvetica', 14)))
        self._topButtons.append(tk.Button(master=self._window,
                                           command=self.toEnglish,
                                           relief=tk.RAISED,
                                           font=('Helvetica', 14)))
        self._topButtons[0].place(relx=0.0, rely=0.0, relwidth=0.5, relheight=0.1)
        self._topButtons[1].place(relx=0.5, rely=0.0, relwidth=0.5, relheight=0.1)

        self._frames = []
        self._frames.append(SLG_MainFrame(self._window))
        self._frames.append(SLG_szsArchiveFrame(self._window))
        self._frames.append(SLG_SFPArchiveFrame(self._window))
        self._frames.append(SLG_tigImageFrame(self._window))
        self._frames.append(SLG_ticImageFrame(self._window))
        self._frames.append(SLG_TIMImageFrame(self._window))
        self._frames.append(SLG_albImageFrame(self._window))
        self._frames.append(SLG_VOIAudioFrame(self._window))

        self._razdelButtons = []
        for i in range(8):
            self._razdelButtons.append(tk.Button(master=self._window,
                                           relief=tk.RAISED,
                                           borderwidth=8,
                                           font=('Helvetica', 12)))
            self._razdelButtons[i].place(relx=0.0, rely=0.1125*(i+1), relwidth=0.35, relheight=0.1)
        self._razdelButtons[0]["command"] = self.toZeroFrame
        self._razdelButtons[1]["command"] = self.toFirstFrame
        self._razdelButtons[2]["command"] = self.toSecondFrame
        self._razdelButtons[3]["command"] = self.toThirdFrame
        self._razdelButtons[4]["command"] = self.toForthFrame
        self._razdelButtons[5]["command"] = self.toFithFrame
        self._razdelButtons[6]["command"] = self.toSixthFrame
        self._razdelButtons[7]["command"] = self.toSeventhFrame

        self._change_language()
        self._change_frame()
        self._window.mainloop()

    def toZeroFrame(self):
        self._currentPanel = 0
        self._change_frame()
    def toFirstFrame(self):
        self._currentPanel = 1
        self._change_frame()
    def toSecondFrame(self):
        self._currentPanel = 2
        self._change_frame()
    def toThirdFrame(self):
        self._currentPanel = 3
        self._change_frame()
    def toForthFrame(self):
        self._currentPanel = 4
        self._change_frame()
    def toFithFrame(self):
        self._currentPanel = 5
        self._change_frame()
    def toSixthFrame(self):
        self._currentPanel = 6
        self._change_frame()
    def toSeventhFrame(self):
        self._currentPanel = 7
        self._change_frame()
    def _change_frame(self):
        for i in range(8):
            if (i == self._currentPanel):
                self._frames[i].place(relx=0.4, rely=0.125, relwidth=0.575, relheight=0.875)
                self._razdelButtons[i]["relief"] = tk.SUNKEN
                self._razdelButtons[i]["state"] = tk.DISABLED
            else:
                self._frames[i].place_forget()
                self._razdelButtons[i]["relief"] = tk.RAISED
                self._razdelButtons[i]["state"] = tk.NORMAL

    def toRussian(self):
        self._lang = 'rus'
        self._change_language()
    def toEnglish(self):
        self._lang = 'eng'
        self._change_language()
    def _change_language(self):
        failer = True
        for i in self.strings_lib:
            if (self._lang == i):
                failer = False
        if (failer):
            print("Verily, sorry I am!\nThis language is not supportred!")
            self._lang = 'eng'

        for i in range(2):
            self._topButtons[i]["text"] = self.strings_lib[self._lang][i]
            self._topButtons[i]["relief"] = self._top_relief_lib[self._lang][i]
        for i in range(8):
            self._razdelButtons[i]["text"] = self.strings_lib[self._lang][i+2]
            self._frames[i].translate_to(self._lang)
        self._window.title(self.top_name_lib[self._lang])
    def _define_language(self):
        is_rus = False
        windll = ctypes.windll.kernel32
        superlocale = locale.windows_locale[windll.GetUserDefaultUILanguage()][:2]
        if (superlocale == 'ru'):
            is_rus = True
        elif (superlocale == 'uk'):
            is_rus = True
        elif (superlocale == 'sr'):
            is_rus = True
        elif (superlocale == 'bg'):
            is_rus = True
        elif (superlocale == 'kk'):
            is_rus = True
        elif (superlocale == 'be'):
            is_rus = True
        elif (superlocale == 'hy'):
            is_rus = True
        elif (superlocale == 'az'):
            is_rus = True

        if (is_rus):
            return 'rus'
        else:
            return 'eng'

class SLG_MasterFrame(tk.Frame):
    strings_lib = {
        'eng': ('none'),
        'rus': ('ничего')
    }

    def __init__(self, master):
        super(SLG_MasterFrame, self).__init__()
        self.master = master
        self["background"] = 'white'
        self["relief"] = tk.RAISED
        self["borderwidth"] = 5

    def translate_to_eng(self):
        self.translate_to('eng')
    def translate_to_rus(self):
        self.translate_to('rus')

    def translate_to(self, language):
        pass

class SLG_MainFrame(SLG_MasterFrame):
    strings_lib = {
        'eng': (
            'Choose the help mode',
            'Tool help',
            'About SLG System engine',
            'About szs archives',
            'About SFP (SPD+SPL) archives',
            'About tig images',
            'About tic images',
            'About TIM images',
            'About alb images',
            'About VOI audio (or voi)',
            'About mdm and mda video',
        ),
        'rus': (
            'Выберите режим справки',
            'Помощь по средству',
            'Справка о движке SLG System',
            'Об архивах szs',
            'Об архивах SFP (SPD+SPL)',
            'О картинках tig',
            'О картинках tic',
            'О картинках TIM',
            'О картинках alb',
            'Об аудиофайлах VOI (или voi)',
            'Об видеофайлах mdm и mda',
        )
    }

    message_lib = {
        'eng': (
            '''Dual languaged (eng+rus) tool for extracting, repacking, converting and reconverting resources of SLG System Engine, such as archives (szs, SFP (SPD+SPL)), images (tig, tic, TIM, alb) and audio (VOI). It has some information about video (mdm, mda) too (the tool is not needed for it's editing). SLG System is an engine, used in some visual novels and jRPG's, such is legendary series Sengoku Hime and Sankoku Hime.\n\nIt has the following features:\n\n- Help module.\n- Extraction the archives in a specific directories.\n- Repacking archives from a specific directories files.\n- Convertion engine image and audio file to standart one.\n- Reconvertion standart image and audio file to engine one.\n- Convertation engine images in directory.\n- Reconvertation standart images in directory.\n\nHow to use?\n\n- Choose the file format, file of which thou want to convert/reconvert/extract/repack.\n- Choose the version (if needed).\n- Choose the mood (if needed), directories or files.\n- Choose the files or/and directories.\n- Select the command and push it's button.''',
            '''SLG System Engine is not very popular, but also not very obsqure engine, used in Gesen 18 (may be not only whose) games. It's in fact some sort of modified Tenka Touitsu ADVANCE engine. There are a lot of good visual novels and jRPG's written on it, such as Sengoku Hime and Sankoku Hime series.\n\nOldest versions of it, such as Shihen 69's version, uses no specific archives. For images it has exotic alb format, for audiodata — VOI format.\nIn some versions older, such as in Sengoku Hime 1, alb no londer used for images. Instead there are tig, TIM and probably tic formats.\nLater version, such as Sengoku Hime 3's, uses also szs and SFP (SPD+SPL) archives.\nAnd the latest versions uses also a mdm and mda video files. Games on these versions, such as Sengoku Hime 4, has new file structure.''',
            '''Standart SLG System's resource archive, it often contains scripts, images and such data.\nHas non-compressed, but slightly obfusificated (xor 0x90) data.''',
            '''Special bicomponental SLG System's music archive, it contains only (or mostly) audio data. Still theoretically it can contain other types of data.\nSPD component contains data, while SPL — it's list.\nContains raw data.''',
            '''Obfusificated png. Most common image type in games based on SLG System (with exception of ealiest versions).\nNew byte = old byte + key, there each next key = (last key * a + b) >> 16.''',
            '''Obfusificated jpg (same type as tig). Very rare. I don't remember myself there you can find one.''',
            '''Special image of SLG System. Has some technical data, may be encrypted with different keys per image.\nEncrypted closely as tig or tic, but the image data itself's keys are rotated in range 0x1000.''',
            '''Very exotic and awfully compressed png image, commonly used in games on the oldest SLG System's versions.\nIt's so heavily encrypted that alb size doubles source png size! Never repeat the mistakes of the format developers, seriously!\nI won't even explain about this awful compression. Look in this mess yourself if you want.\nThis tool creates better alb (which games on the engine understands), which size is about source png's.''',
            '''Commonly used SLG System's audio format. Just some technical data and raw ogg.''',
            '''Videoformat, used in games on latest SLG System. Probably just a simple mpeg, so you don't need any specific tools to convert it.\nEncoded by TMPGEnc, as stated in files.'''
        ),
        'rus': (
            '''Двуязычное (англ + рус) средство для распаковки, перепаковки, конвертации и реконвертации ресурсов движка SLG System, таких как архивов (szs, SFP (SPD+SPL), картинок (tig, tic, TIM, alb) и аудиофайлов (VOI). В справке средства также приведены некоторые данные по видеоформатам движка (mdm, mda), для редактирования которых сие средство не требуется. SLG System есть движок, используемый в ряде визуальных новелл и японских ролевых игр (jRPG), в частности в легендарных сериях Принцессы Сэнгоку, Принцессы Троецарствия.\n\nИмеет следующие возможности:\n\n- Справочный модуль.\n- Извлечение архивов в выбранные директории.\n- Создание архивов из файлов в выбранной директории.\n- Конвертация картинки и аудиофайла движка в стандартную.\n- Реконвертация стандартной картинки и аудиофайла в таковую у движка.\n- Конвертация картинок и аудиофайлов движка в директории.\n- Реконвертация стандартных картинок и аудиофайлов в директории.\n\nКак использовать?\n\n- Выберите формат файлов, что вы конвертировать/реконвертировать/извлечь/запаковать жаждете.\n- Выберите версию (коли надобно).\n- Выберите режим (коли надобно, пофайловый али попапковый.\n- Выберите файлы и/иль директории (папки).\n- Выберите команду и нажмите на соответствующую кнопку.''',
            '''SLG System является не слишком популярным, но и не слишком неизвестным движком, используемым в играх Gesen 18 и, вероятно, Unicorn-A. На самом деле является своего рода модификацией движка Тэнка то:ицу ADVANCE. На нём написано немало сдобный визуальных новелл и японских ролевых игр (jRPG), например серии Принцессы Сэнгоку и Принцессы Троецарствия.\n\nСтарейшие его версии не используют каких-либо особенных архивных форматов. Для картинок в них используется своеобразный формат alb, а для звуков — VOI.\nДвижок несколькими версиями спустя, например в Принцессах Сэнгоку 1, уже не использует alb. Вместо них применяются tig, TIM и, вероятно, tic.\nБолее поздние версии, как, например, в Принцессах Сэнгоку 3, используют также архивы szs и SFP (SPD+SPL).\nИ последние же версии используют видеофайлы mdm и mda. У игр на сих версиях, например Принцессах Сэнгоку 4, структура файлов уже иная.''',
            '''Стандартный архив ресурсов движка SLG System. Часто содержит скрипты, картинки и прочее подобное.\nСодержит несжатые, но немного обфусицированные (xor 0x90) данные.''',
            '''Специальный двукомпонентный архив движка SLG System. Содержит только (или почти только) аудиоданные, однако в теории может содержать и другие типы данных.\nКомпонент SDP содержит сами данные, в то время как SPL — их список.\nДанные не обфусифицированы.''',
            '''Обфусифицированная png. Наиболее частый формат картинок игр на движке SLG System (кроме старейших версий).\nНовый байт = старый байт + ключ, где каждый следующий кюч = (прошлый ключ * a + b) >> 16.''',
            '''Обфусифицированная (так же, как и tig) jpg. Крайне редко встречается. Даже сам не помню, где можно найти представителя.''',
            '''Особая картинка движка SLG System. Вмещает некоторые технические данные, каждая картинка может быть зашифрована своим ключём.\nШифрование похоже на таковое у tig и tic, но у самих данных изображения ключи повторяются в диапазоне 0x1000.''',
            '''Вельми экзотичный формат, ужасно сжатая картинка png, что повсеместно используется в играх на старейших разновидностях SLG System.\nНастолько могуче сжата, что размер alb вдвое больше, чем у исходной зтп! Никогда не повторяйте ошибок горе-разработчиков формата, серьёзно!\nДаже не буду объяснять про сей ужасный алгоритм сжатия. Посмотрите на сей бардак сами, коль желаете.\nСие средство создаёт лучшие alb (кои игры на движке понимают) размером примерно с исходные png.''',
            '''Повсеместно используемый аудиоформат движка SLG System. Просто некоторые технические данные в сочетании с простым ogg.''',
            '''Видеоформат, используемый в играх на последних версиях SLG System. Судя по всему, простой mpeg, так что для его конвертации не потребуется никаких специальных средств.\nЗакодирован, как указано в файлах, с помощью TMPGEnc.'''
        )
    }

    def __init__(self, master):
        super(SLG_MasterFrame, self).__init__()
        self.master = master
        self["background"] = 'white'
        self["relief"] = tk.RAISED
        self["borderwidth"] = 5

        self._language = 'eng'

        self._lbl_spr = tk.Label(
            master=self,
            font=('Calibri Bold', 14),
            bg='white',
        )
        self._lbl_spr.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=0.1)

        self._about_buttons = []
        for i in range(10):
            self._about_buttons.append(tk.Button(
                master=self,
                font=('Calibri', 14)
            ))
            self._about_buttons[i].place(relx=0.0, rely=0.091*(i+1), relwidth=1.0, relheight=0.091)
        self._about_buttons[0]["command"] = self._tool_help
        self._about_buttons[1]["command"] = self._engine_help
        self._about_buttons[2]["command"] = self._szs_help
        self._about_buttons[3]["command"] = self._SFP_help
        self._about_buttons[4]["command"] = self._tig_help
        self._about_buttons[5]["command"] = self._tic_help
        self._about_buttons[6]["command"] = self._TIM_help
        self._about_buttons[7]["command"] = self._alb_help
        self._about_buttons[8]["command"] = self._VOI_help
        self._about_buttons[9]["command"] = self._video_help

    def translate_to(self, language):
        self._language = language
        self._lbl_spr["text"] = self.strings_lib[language][0]
        for i in range(10):
            self._about_buttons[i]["text"] = self.strings_lib[language][i+1]

    def _tool_help(self):
        k = 0
        self._show_message(self.strings_lib[self._language][k+1], self.message_lib[self._language][k])
    def _engine_help(self):
        k = 1
        self._show_message(self.strings_lib[self._language][k+1], self.message_lib[self._language][k])
    def _szs_help(self):
        k = 2
        self._show_message(self.strings_lib[self._language][k+1], self.message_lib[self._language][k])
    def _SFP_help(self):
        k = 3
        self._show_message(self.strings_lib[self._language][k+1], self.message_lib[self._language][k])
    def _tig_help(self):
        k = 4
        self._show_message(self.strings_lib[self._language][k+1], self.message_lib[self._language][k])
    def _tic_help(self):
        k = 5
        self._show_message(self.strings_lib[self._language][k+1], self.message_lib[self._language][k])
    def _TIM_help(self):
        k = 6
        self._show_message(self.strings_lib[self._language][k+1], self.message_lib[self._language][k])
    def _alb_help(self):
        k = 7
        self._show_message(self.strings_lib[self._language][k+1], self.message_lib[self._language][k])
    def _VOI_help(self):
        k = 8
        self._show_message(self.strings_lib[self._language][k+1], self.message_lib[self._language][k])
    def _video_help(self):
        k = 9
        self._show_message(self.strings_lib[self._language][k+1], self.message_lib[self._language][k])

    def _show_message(self, title, message):
        messagebox.showinfo(title, message)

class SLG_szsArchiveFrame(SLG_MasterFrame):
    strings_lib = {
        'eng': ('Version:',
                'Choose the szs archive file:',
                'Choose the directory:',
                'Szs archives',
                '*.szs',
                'All files',
                '*',
                'Unpack archive to the directory',
                'Create archive from the directory files',
                'Such archive is not exist!',
                'Such directory is not exist!',
                'Version/signature mismatch!',
                'Archive successfully extracted!',
                'Archive successfully created!',
                'Extraction in process...\nThis can take some time.\nFeel free to drink some tea.',
                'Creation in process...\nThis can take some time.\nFeel free to drink some tea.'
                ),
        'rus': ('Версия:',
                'Выберите архив szs:',
                'Выберите директорию:',
                'Картинки szs',
                '*.szs',
                'Все файлы',
                '*',
                'Распаковать архив в директорию',
                'Создать архив из файлов в директории',
                'Сего файла не существует!',
                'Сей директории не существует!',
                'Несовпадение версии и сигнатуры!',
                'Архив успешно извлечён!',
                'Архив успешно создан!',
                'Выполнение извлечения...\nСие может занять некоторое время.\nМожете пока попить чайку.',
                'Выполнение создания...\nСие может занять некоторое время.\nМожете пока попить чайку.'
                )
    }

    def __init__(self, master):
        super(SLG_MasterFrame, self).__init__()
        self.master = master
        self["background"] = 'white'
        self["relief"] = tk.RAISED
        self["borderwidth"] = 5

        self._language = 'eng'

        self._arc_version = tk.StringVar()
        self._file_arc = tk.StringVar()
        self._file_dir = tk.StringVar()

        self._lblvers = tk.Label(master=self,
                                 background='white',
                                 font=('Helvetica', 14))
        self._arc_versions = []
        for i in range(len(SLG_Archives_szs.version_signature_library)):
            self._arc_versions.append(i)
        self._arc_versions.append('???')
        self._arc_version.set(self._arc_versions[0])
        self._cmb_choose_version = ttk.Combobox(
            master=self,
            font=('Helvetica', 14),
            values=self._arc_versions,
            textvariable=self._arc_version,
            state='readonly'
        )
        self._lblvers.place(relx=0.0, rely=0.0, relwidth=0.5, relheight=0.1)
        self._cmb_choose_version.place(relx=0.5, rely=0.0, relwidth=0.5, relheight=0.1)

        self._lblszs = tk.Label(master=self,
                                background='white',
                                font=('Helvetica', 14))
        self._ent_arc = tk.Entry(
            master=self,
            textvariable=self._file_arc,
            font=('Helvetica', 8),
            borderwidth=5
        )
        self._btn_what_arc = tk.Button(
            master=self,
            command=self._what_arc,
            relief=tk.RAISED,
            font=('Helvetica', 14),
            text='...'
        )
        self._lbldir = tk.Label(master=self,
                                background='white',
                                font=('Helvetica', 14))
        self._ent_dir = tk.Entry(
            master=self,
            textvariable=self._file_dir,
            font=('Helvetica', 8),
            borderwidth=5
        )
        self._btn_what_dir = tk.Button(
            master=self,
            command=self._what_dir,
            relief=tk.RAISED,
            font=('Helvetica', 14),
            text='...'
        )
        self._lblszs.place(relx=0.0, rely=0.1, relwidth=1.0, relheight=0.1)
        self._ent_arc.place(relx=0.0, rely=0.2, relwidth=0.85, relheight=0.1)
        self._btn_what_arc.place(relx=0.85, rely=0.2, relwidth=0.15, relheight=0.1)
        self._lbldir.place(relx=0.0, rely=0.3, relwidth=1.0, relheight=0.1)
        self._ent_dir.place(relx=0.0, rely=0.4, relwidth=0.85, relheight=0.1)
        self._btn_what_dir.place(relx=0.85, rely=0.4, relwidth=0.15, relheight=0.1)

        self._btn_unpack = tk.Button(
            master=self,
            command=self._unpack,
            relief=tk.RAISED,
            font=('Helvetica', 12),
        )
        self._btn_pack = tk.Button(
            master=self,
            command=self._pack,
            relief=tk.RAISED,
            font=('Helvetica', 12),
        )
        self._txt_status = tk.Text(
            master=self,
            bg='white',
            state=tk.DISABLED,
        )

        self._btn_unpack.place(relx=0.0, rely=0.5, relwidth=1.0, relheight=0.1)
        self._btn_pack.place(relx=0.0, rely=0.6, relwidth=1.0, relheight=0.1)
        self._txt_status.place(relx=0.0, rely=0.7, relwidth=1.0, relheight=0.3)

    def translate_to(self, language):
        self._language = language
        self._lblvers["text"] = self.strings_lib[language][0]
        self._lblszs["text"] = self.strings_lib[language][1]
        self._lbldir["text"] = self.strings_lib[language][2]
        self._btn_unpack["text"] = self.strings_lib[language][7]
        self._btn_pack["text"] = self.strings_lib[language][8]

    def _what_arc(self):
        ftypes = [(self.strings_lib[self._language][3], self.strings_lib[self._language][4]),
                  (self.strings_lib[self._language][5], self.strings_lib[self._language][6])]
        dialg = filedialog.Open(self, filetypes=ftypes, initialdir=os.getcwd())
        file = dialg.show()
        if (file != ''):
            self._file_arc.set(file)
    def _what_dir(self):
        direr = filedialog.askdirectory()
        if (direr != ''):
            self._file_dir.set(direr)

    def _unpack(self):
        self._set_new_msg(self.strings_lib[self._language][14])
        unpack = threading.Thread(target=self._unpack_funcer)
        unpack.start()
    def _unpack_funcer(self):
        self._btn_unpack["state"] = tk.DISABLED
        self._btn_pack["state"] = tk.DISABLED
        try:
            versioner = self._arc_version.get()
            try:
                verser = int(versioner)
            except:
                verser = -1
            newArchive = SLG_Archives_szs(self._file_arc.get(), self._file_dir.get(), verser)
            newArchive.unpack()
            self._set_new_msg(self.strings_lib[self._language][12])
        except FileNotFoundError as ex:
            if (str(ex) == "There is no such archive!"):
                self._set_new_msg(self.strings_lib[self._language][9])
            else:
                self._set_new_msg(self.strings_lib[self._language][10])
        except SLG_ArchivesError:
            self._set_new_msg(self.strings_lib[self._language][11])
        except Exception as ex:
            self._set_new_msg(ex)
        finally:
            try:
                del newArchive
            except:
                pass
            self._btn_unpack["state"] = tk.NORMAL
            self._btn_pack["state"] = tk.NORMAL
    def _pack(self):
        self._set_new_msg(self.strings_lib[self._language][15])
        pack = threading.Thread(target=self._pack_funcer)
        pack.start()
    def _pack_funcer(self):
        self._btn_unpack["state"] = tk.DISABLED
        self._btn_pack["state"] = tk.DISABLED
        try:
            versioner = self._arc_version.get()
            try:
                verser = int(versioner)
            except:
                verser = -1
            newArchive = SLG_Archives_szs(self._file_dir.get(), self._file_arc.get(), verser)
            newArchive.repack()
            self._set_new_msg(self.strings_lib[self._language][13])
        except FileNotFoundError as ex:
            if (str(ex) == "There is no such directory!"):
                self._set_new_msg(self.strings_lib[self._language][10])
            else:
                self._set_new_msg(self.strings_lib[self._language][9])
        except SLG_ArchivesError:
            self._set_new_msg(self.strings_lib[self._language][11])
        except Exception as ex:
            self._set_new_msg(str(ex))
        finally:
            try:
                del newArchive
            except:
                pass
            self._btn_unpack["state"] = tk.NORMAL
            self._btn_pack["state"] = tk.NORMAL

    def _set_new_msg(self, msg):
            self._txt_status["state"] = tk.NORMAL
            self._txt_status.delete(1.0, tk.END)
            self._txt_status.insert(1.0, msg)
            self._txt_status["state"] = tk.DISABLED

class SLG_SFPArchiveFrame(SLG_MasterFrame):
    strings_lib = {
        'eng': ('Version:',
                'Choose the SFP archive components:',
                'Choose the directory:',
                'SPD component',
                '*.SPD',
                'All files',
                '*',
                'Unpack archive to the directory',
                'Create archive from the directory files',
                'Such archive is not exist!',
                'Such directory is not exist!',
                'Version mismatch!',
                'Archive successfully extracted!',
                'Archive successfully created!',
                'Extraction in process...\nThis can take some time.\nFeel free to drink some tea.',
                'Creation in process...\nThis can take some time.\nFeel free to drink some tea.',
                'SPL component',
                '*.SPL',
                ),
        'rus': ('Версия:',
                'Выберите компоненты архива SFP:',
                'Выберите директорию:',
                'Компонент SPD',
                '*.SPD',
                'Все файлы',
                '*',
                'Распаковать архив в директорию',
                'Создать архив из файлов в директории',
                'Сего файла не существует!',
                'Сей директории не существует!',
                'Несовпадение версии!',
                'Архив успешно извлечён!',
                'Архив успешно создан!',
                'Выполнение извлечения...\nСие может занять некоторое время.\nМожете пока попить чайку.',
                'Выполнение создания...\nСие может занять некоторое время.\nМожете пока попить чайку.',
                'Компонент SPL',
                '*.SPL',
                )
    }

    def __init__(self, master):
        super(SLG_MasterFrame, self).__init__()
        self.master = master
        self["background"] = 'white'
        self["relief"] = tk.RAISED
        self["borderwidth"] = 5

        self._language = 'eng'

        self._arc_version = tk.StringVar()
        self._file_SPD = tk.StringVar()
        self._file_SPL = tk.StringVar()
        self._file_dir = tk.StringVar()

        self._lblvers = tk.Label(master=self,
                                 background='white',
                                 font=('Helvetica', 14))
        self._arc_versions = []
        for i in SLG_Archives_SFP.version_lib:
            self._arc_versions.append(i[0])
        self._arc_versions.append('???')
        self._arc_version.set(self._arc_versions[0])
        self._cmb_choose_version = ttk.Combobox(
            master=self,
            font=('Helvetica', 14),
            values=self._arc_versions,
            textvariable=self._arc_version,
            state='readonly'
        )
        self._lblvers.place(relx=0.0, rely=0.0, relwidth=0.5, relheight=0.1)
        self._cmb_choose_version.place(relx=0.5, rely=0.0, relwidth=0.5, relheight=0.1)

        self._lblszs = tk.Label(master=self,
                                background='white',
                                font=('Helvetica', 14))
        self._lbl_SPD = tk.Label(master=self,
                                background='white',
                                font=('Helvetica', 14),
                                text='SPD:')
        self._ent_SPD = tk.Entry(
            master=self,
            textvariable=self._file_SPD,
            font=('Helvetica', 8),
            borderwidth=5
        )
        self._btn_what_SPD = tk.Button(
            master=self,
            command=self._what_SPD,
            relief=tk.RAISED,
            font=('Helvetica', 14),
            text='...'
        )
        self._lbl_SPL = tk.Label(master=self,
                                background='white',
                                font=('Helvetica', 14),
                                text='SPL:')
        self._ent_SPL = tk.Entry(
            master=self,
            textvariable=self._file_SPL,
            font=('Helvetica', 8),
            borderwidth=5
        )
        self._btn_what_SPL = tk.Button(
            master=self,
            command=self._what_SPL,
            relief=tk.RAISED,
            font=('Helvetica', 14),
            text='...'
        )
        self._lbldir = tk.Label(master=self,
                                background='white',
                                font=('Helvetica', 14))
        self._ent_dir = tk.Entry(
            master=self,
            textvariable=self._file_dir,
            font=('Helvetica', 8),
            borderwidth=5
        )
        self._btn_what_dir = tk.Button(
            master=self,
            command=self._what_dir,
            relief=tk.RAISED,
            font=('Helvetica', 14),
            text='...'
        )
        self._lblszs.place(relx=0.0, rely=0.1, relwidth=1.0, relheight=0.1)
        self._lbl_SPD.place(relx=0.0, rely=0.2, relwidth=0.15, relheight=0.1)
        self._ent_SPD.place(relx=0.15, rely=0.2, relwidth=0.7, relheight=0.1)
        self._btn_what_SPD.place(relx=0.85, rely=0.2, relwidth=0.15, relheight=0.1)
        self._lbl_SPL.place(relx=0.0, rely=0.3, relwidth=0.15, relheight=0.1)
        self._ent_SPL.place(relx=0.15, rely=0.3, relwidth=0.7, relheight=0.1)
        self._btn_what_SPL.place(relx=0.85, rely=0.3, relwidth=0.15, relheight=0.1)
        self._lbldir.place(relx=0.0, rely=0.4, relwidth=1.0, relheight=0.1)
        self._ent_dir.place(relx=0.0, rely=0.5, relwidth=0.85, relheight=0.1)
        self._btn_what_dir.place(relx=0.85, rely=0.5, relwidth=0.15, relheight=0.1)

        self._btn_unpack = tk.Button(
            master=self,
            command=self._unpack,
            relief=tk.RAISED,
            font=('Helvetica', 12),
        )
        self._btn_pack = tk.Button(
            master=self,
            command=self._pack,
            relief=tk.RAISED,
            font=('Helvetica', 12),
        )
        self._txt_status = tk.Text(
            master=self,
            bg='white',
            state=tk.DISABLED,
        )

        self._btn_unpack.place(relx=0.0, rely=0.6, relwidth=1.0, relheight=0.1)
        self._btn_pack.place(relx=0.0, rely=0.7, relwidth=1.0, relheight=0.1)
        self._txt_status.place(relx=0.0, rely=0.8, relwidth=1.0, relheight=0.2)

    def translate_to(self, language):
        self._language = language
        self._lblvers["text"] = self.strings_lib[language][0]
        self._lblszs["text"] = self.strings_lib[language][1]
        self._lbldir["text"] = self.strings_lib[language][2]
        self._btn_unpack["text"] = self.strings_lib[language][7]
        self._btn_pack["text"] = self.strings_lib[language][8]

    def _what_SPD(self):
        ftypes = [(self.strings_lib[self._language][3], self.strings_lib[self._language][4]),
                  (self.strings_lib[self._language][5], self.strings_lib[self._language][6])]
        dialg = filedialog.Open(self, filetypes=ftypes, initialdir=os.getcwd())
        file = dialg.show()
        if (file != ''):
            self._file_SPD.set(file)
    def _what_SPL(self):
        ftypes = [(self.strings_lib[self._language][16], self.strings_lib[self._language][17]),
                  (self.strings_lib[self._language][5], self.strings_lib[self._language][6])]
        dialg = filedialog.Open(self, filetypes=ftypes, initialdir=os.getcwd())
        file = dialg.show()
        if (file != ''):
            self._file_SPL.set(file)
    def _what_dir(self):
        direr = filedialog.askdirectory()
        if (direr != ''):
            self._file_dir.set(direr)

    def _unpack(self):
        self._set_new_msg(self.strings_lib[self._language][14])
        unpack = threading.Thread(target=self._unpack_funcer)
        unpack.start()
    def _unpack_funcer(self):
        self._btn_unpack["state"] = tk.DISABLED
        self._btn_pack["state"] = tk.DISABLED
        try:
            versioner = self._arc_version.get()
            try:
                verser = int(versioner)
            except:
                verser = -1
            newArchive = SLG_Archives_SFP(self._file_SPD.get(), self._file_SPL.get(),
                                          self._file_dir.get(), verser)
            newArchive.unpack()
            self._set_new_msg(self.strings_lib[self._language][12])
        except FileNotFoundError as ex:
            if (str(ex) == "There is no such archive!"):
                self._set_new_msg(self.strings_lib[self._language][9])
            else:
                self._set_new_msg(self.strings_lib[self._language][10])
        except SLG_ArchivesError:
            self._set_new_msg(self.strings_lib[self._language][11])
        except Exception as ex:
            self._set_new_msg(ex)
        finally:
            try:
                del newArchive
            except:
                pass
            self._btn_unpack["state"] = tk.NORMAL
            self._btn_pack["state"] = tk.NORMAL
    def _pack(self):
        self._set_new_msg(self.strings_lib[self._language][15])
        pack = threading.Thread(target=self._pack_funcer)
        pack.start()
    def _pack_funcer(self):
        self._btn_unpack["state"] = tk.DISABLED
        self._btn_pack["state"] = tk.DISABLED
        try:
            versioner = self._arc_version.get()
            try:
                verser = int(versioner)
            except:
                verser = -1
            newArchive = SLG_Archives_SFP(self._file_SPD.get(), self._file_SPL.get(),
                                          self._file_dir.get(), verser)
            newArchive.repack()
            self._set_new_msg(self.strings_lib[self._language][13])
        except FileNotFoundError as ex:
            if (str(ex) == "There is no such directory!"):
                self._set_new_msg(self.strings_lib[self._language][10])
            else:
                self._set_new_msg(self.strings_lib[self._language][9])
        except SLG_ArchivesError:
            self._set_new_msg(self.strings_lib[self._language][11])
        except Exception as ex:
            self._set_new_msg(str(ex))
        finally:
            try:
                del newArchive
            except:
                pass
            self._btn_unpack["state"] = tk.NORMAL
            self._btn_pack["state"] = tk.NORMAL

    def _set_new_msg(self, msg):
            self._txt_status["state"] = tk.NORMAL
            self._txt_status.delete(1.0, tk.END)
            self._txt_status.insert(1.0, msg)
            self._txt_status["state"] = tk.DISABLED

class SLG_tigImageFrame(SLG_MasterFrame):
    _to_what = '.png'
    strings_lib = {
        'eng': ('Choose the mode:',
                'Choose the tig image file:',
                'Choose the png image file:',
                'Tig images',
                '*.tig',
                'All files',
                '*',
                'Convert tig to png',
                'Reconvert tig from png',
                'Such archive is not exist!',
                'Such directory is not exist!',
                'Version/signature mismatch!',
                'Image successfully converted!',
                'Image successfully reconverted!',
                'Conversion in process...\nThis can take some time.\nFeel free to drink some tea.',
                'Reconversion in process...\nThis can take some time.\nFeel free to drink some tea.',
                'Files',
                'Directories',
                'Png images',
                '*.png',
                'Choose the directory with tig images:',
                'Choose the directory with png images:'
                ),
        'rus': ('Выберите режим:',
                'Выберите картинку tig:',
                'Выберите картинку png:',
                'Картинки tig',
                '*.tig',
                'Все файлы',
                '*',
                'Конвертировать tig в png',
                'Реконвертировать tig из png',
                'Сего файла не существует!',
                'Сей директории не существует!',
                'Несовпадение версии и сигнатуры!',
                'Конвертация прошла успешно!',
                'Реконвертация прошла успешно!',
                'Выполнение конвертации...\nСие может занять некоторое время.\nМожете пока попить чайку.',
                'Выполнение реконвертации...\nСие может занять некоторое время.\nМожете пока попить чайку.',
                'Файлы',
                'Директории',
                'Картинки png',
                '*.png',
                'Выберите папку с картинками tig:',
                'Выберите папку с картинками png:'
                )
    }

    def __init__(self, master):
        super(SLG_MasterFrame, self).__init__()
        self.master = master
        self["background"] = 'white'
        self["relief"] = tk.RAISED
        self["borderwidth"] = 5

        self._language = 'eng'

        self._mode = tk.IntVar()
        self._file_arc = tk.StringVar()
        self._file_dir = tk.StringVar()

        self._mode.set(0)

        self._lblvers = tk.Label(master=self,
                                 background='white',
                                 font=('Helvetica', 14))
        self._mode_one = tk.Radiobutton(master=self,
                                        background='white',
                                        font=('Helvetica', 14),
                                        variable=self._mode,
                                        value=0)
        self._mode_two = tk.Radiobutton(master=self,
                                        background='white',
                                        font=('Helvetica', 14),
                                        variable=self._mode,
                                        value=1)
        self._mode_one.bind('<Button-1>', self._mode_change)
        self._mode_two.bind('<Button-1>', self._mode_change)
        self._lblvers.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=0.1)
        self._mode_one.place(relx=0.0, rely=0.1, relwidth=0.5, relheight=0.1)
        self._mode_two.place(relx=0.5, rely=0.1, relwidth=0.5, relheight=0.1)

        self._lblszs = tk.Label(master=self,
                                background='white',
                                font=('Helvetica', 14))
        self._ent_arc = tk.Entry(
            master=self,
            textvariable=self._file_arc,
            font=('Helvetica', 8),
            borderwidth=5
        )
        self._btn_what_arc = tk.Button(
            master=self,
            command=self._what_arc,
            relief=tk.RAISED,
            font=('Helvetica', 14),
            text='...'
        )
        self._lbldir = tk.Label(master=self,
                                background='white',
                                font=('Helvetica', 14))
        self._ent_dir = tk.Entry(
            master=self,
            textvariable=self._file_dir,
            font=('Helvetica', 8),
            borderwidth=5
        )
        self._btn_what_dir = tk.Button(
            master=self,
            command=self._what_dir,
            relief=tk.RAISED,
            font=('Helvetica', 14),
            text='...'
        )
        self._lblszs.place(relx=0.0, rely=0.2, relwidth=1.0, relheight=0.1)
        self._ent_arc.place(relx=0.0, rely=0.3, relwidth=0.85, relheight=0.1)
        self._btn_what_arc.place(relx=0.85, rely=0.3, relwidth=0.15, relheight=0.1)
        self._lbldir.place(relx=0.0, rely=0.4, relwidth=1.0, relheight=0.1)
        self._ent_dir.place(relx=0.0, rely=0.5, relwidth=0.85, relheight=0.1)
        self._btn_what_dir.place(relx=0.85, rely=0.5, relwidth=0.15, relheight=0.1)

        self._btn_unpack = tk.Button(
            master=self,
            command=self._unpack,
            relief=tk.RAISED,
            font=('Helvetica', 12),
        )
        self._btn_pack = tk.Button(
            master=self,
            command=self._pack,
            relief=tk.RAISED,
            font=('Helvetica', 12),
        )
        self._txt_status = tk.Text(
            master=self,
            bg='white',
            state=tk.DISABLED,
        )

        self._btn_unpack.place(relx=0.0, rely=0.6, relwidth=1.0, relheight=0.1)
        self._btn_pack.place(relx=0.0, rely=0.7, relwidth=1.0, relheight=0.1)
        self._txt_status.place(relx=0.0, rely=0.8, relwidth=1.0, relheight=0.2)

    def translate_to(self, language):
        self._language = language
        self._lblvers["text"] = self.strings_lib[language][0]
        self._remake_razd_nadp(self._mode.get())
        self._btn_unpack["text"] = self.strings_lib[language][7]
        self._btn_pack["text"] = self.strings_lib[language][8]
        self._mode_one["text"] = self.strings_lib[language][16]
        self._mode_two["text"] = self.strings_lib[language][17]
    def _remake_razd_nadp(self, moder):
        self._lblszs["text"] = self.strings_lib[self._language][19*moder+1]
        self._lbldir["text"] = self.strings_lib[self._language][19*moder+2]

    def _what_arc(self):
        if (self._mode.get() == 0):
            ftypes = [(self.strings_lib[self._language][3], self.strings_lib[self._language][4]),
                      (self.strings_lib[self._language][5], self.strings_lib[self._language][6])]
            dialg = filedialog.Open(self, filetypes=ftypes, initialdir=os.getcwd())
            file = dialg.show()
            if (file != ''):
                self._file_arc.set(file)
        else:
            direr = filedialog.askdirectory()
            if (direr != ''):
                self._file_arc.set(direr)
    def _what_dir(self):
        if (self._mode.get() == 0):
            ftypes = [(self.strings_lib[self._language][18], self.strings_lib[self._language][19]),
                      (self.strings_lib[self._language][5], self.strings_lib[self._language][6])]
            dialg = filedialog.Open(self, filetypes=ftypes, initialdir=os.getcwd())
            file = dialg.show()
            if (file != ''):
                self._file_dir.set(file)
        else:
            direr = filedialog.askdirectory()
            if (direr != ''):
                self._file_dir.set(direr)

    def _unpack(self):
        self._set_new_msg(self.strings_lib[self._language][14])
        unpack = threading.Thread(target=self._unpack_funcer)
        unpack.start()
    def _unpack_funcer(self):
        self._btn_unpack["state"] = tk.DISABLED
        self._btn_pack["state"] = tk.DISABLED
        try:
            if (self._mode.get() == 0):
                namer = self._file_dir.get()
                try:
                    if (namer[(0-len(self._to_what)):] != self._to_what):
                        namer += self._to_what
                except:
                    pass
                newImage = SLG_Images_tig(self._file_arc.get(), namer, 0)
                newImage.convert()
            else:
                newImage = SLG_Images_tig(self._file_arc.get(), self._file_dir.get(), 1)
                newImage.convert()
            self._set_new_msg(self.strings_lib[self._language][12])
        except FileNotFoundError as ex:
            if (self._mode.get() == 0):
                self._set_new_msg(self.strings_lib[self._language][9])
            else:
                self._set_new_msg(self.strings_lib[self._language][10])
        except Exception as ex:
            self._set_new_msg(ex)
        finally:
            try:
                del newImage
            except:
                pass
            self._btn_unpack["state"] = tk.NORMAL
            self._btn_pack["state"] = tk.NORMAL
    def _pack(self):
        self._set_new_msg(self.strings_lib[self._language][15])
        pack = threading.Thread(target=self._pack_funcer)
        pack.start()
    def _pack_funcer(self):
        self._btn_unpack["state"] = tk.DISABLED
        self._btn_pack["state"] = tk.DISABLED
        try:
            if (self._mode.get() == 0):
                newImage = SLG_Images_tig(self._file_dir.get(), self._file_arc.get(), 0)
                newImage.reconvert()
            else:
                newImage = SLG_Images_tig(self._file_dir.get(), self._file_arc.get(), 1)
                newImage.reconvert()
            self._set_new_msg(self.strings_lib[self._language][13])
        except FileNotFoundError as ex:
            if (self._mode.get() == 0):
                self._set_new_msg(self.strings_lib[self._language][9])
            else:
                self._set_new_msg(self.strings_lib[self._language][10])
        except Exception as ex:
            self._set_new_msg(ex)
        finally:
            try:
                del newImage
            except:
                pass
            self._btn_unpack["state"] = tk.NORMAL
            self._btn_pack["state"] = tk.NORMAL
    def _mode_change(self, *args):
        self._remake_razd_nadp((self._mode.get() + 1) % 2)
        if (self._mode.get() == 1):
            if (self._file_arc.get() != ''):
                if (os.path.isdir(self._file_arc.get())):
                    self._file_arc.set('')
            if (self._file_dir.get() != ''):
                if (os.path.isdir(self._file_dir.get())):
                    self._file_dir.set('')
        else:
            if (self._file_arc.get() != ''):
                if (os.path.isfile(self._file_arc.get())):
                    self._file_arc.set(os.path.split(self._file_arc.get())[0])
            if (self._file_dir.get() != ''):
                if (os.path.isfile(self._file_dir.get())):
                    self._file_dir.set(os.path.split(self._file_dir.get())[0])

    def _set_new_msg(self, msg):
        self._txt_status["state"] = tk.NORMAL
        self._txt_status.delete(1.0, tk.END)
        self._txt_status.insert(1.0, msg)
        self._txt_status["state"] = tk.DISABLED

class SLG_ticImageFrame(SLG_tigImageFrame):
    _to_what = '.jpg'
    strings_lib = {
        'eng': ('Choose the mode:',
                'Choose the tic image file:',
                'Choose the png image file:',
                'Tic images',
                '*.tic',
                'All files',
                '*',
                'Convert tic to jpg',
                'Reconvert tic from jpg',
                'Such archive is not exist!',
                'Such directory is not exist!',
                'Version/signature mismatch!',
                'Image successfully converted!',
                'Image successfully reconverted!',
                'Conversion in process...\nThis can take some time.\nFeel free to drink some tea.',
                'Reconversion in process...\nThis can take some time.\nFeel free to drink some tea.',
                'Files',
                'Directories',
                'Jpg images',
                '*.jpg; *.jpeg',
                'Choose the directory with tic images:',
                'Choose the directory with jpg images:'
                ),
        'rus': ('Выберите режим:',
                'Выберите картинку tic:',
                'Выберите картинку jpg:',
                'Картинки tic',
                '*.tic',
                'Все файлы',
                '*',
                'Конвертировать tic в jpg',
                'Реконвертировать tic из jpg',
                'Сего файла не существует!',
                'Сей директории не существует!',
                'Несовпадение версии и сигнатуры!',
                'Конвертация прошла успешно!',
                'Реконвертация прошла успешно!',
                'Выполнение конвертации...\nСие может занять некоторое время.\nМожете пока попить чайку.',
                'Выполнение реконвертации...\nСие может занять некоторое время.\nМожете пока попить чайку.',
                'Файлы',
                'Директории',
                'Картинки jpg',
                '*.jpg; *.jpeg',
                'Выберите папку с картинками tic:',
                'Выберите папку с картинками png:'
                )
    }
    def _unpack_funcer(self):
        self._btn_unpack["state"] = tk.DISABLED
        self._btn_pack["state"] = tk.DISABLED
        try:
            if (self._mode.get() == 0):
                namer = self._file_dir.get()
                try:
                    if (namer[(0-len(self._to_what)):] != self._to_what):
                        namer += self._to_what
                except:
                    pass
                newImage = SLG_Images_tic(self._file_arc.get(), namer, 0)
                newImage.convert()
            else:
                newImage = SLG_Images_tic(self._file_arc.get(), self._file_dir.get(), 1)
                newImage.convert()
            self._set_new_msg(self.strings_lib[self._language][12])
        except FileNotFoundError as ex:
            if (self._mode.get() == 0):
                self._set_new_msg(self.strings_lib[self._language][9])
            else:
                self._set_new_msg(self.strings_lib[self._language][10])
        except Exception as ex:
            self._set_new_msg(ex)
        finally:
            try:
                del newImage
            except:
                pass
            self._btn_unpack["state"] = tk.NORMAL
            self._btn_pack["state"] = tk.NORMAL
    def _pack_funcer(self):
        self._btn_unpack["state"] = tk.DISABLED
        self._btn_pack["state"] = tk.DISABLED
        try:
            if (self._mode.get() == 0):
                newImage = SLG_Images_tic(self._file_dir.get(), self._file_arc.get(), 0)
                newImage.reconvert()
            else:
                newImage = SLG_Images_tic(self._file_dir.get(), self._file_arc.get(), 1)
                newImage.reconvert()
            self._set_new_msg(self.strings_lib[self._language][13])
        except FileNotFoundError as ex:
            if (self._mode.get() == 0):
                self._set_new_msg(self.strings_lib[self._language][9])
            else:
                self._set_new_msg(self.strings_lib[self._language][10])
        except Exception as ex:
            self._set_new_msg(ex)
        finally:
            try:
                del newImage
            except:
                pass
            self._btn_unpack["state"] = tk.NORMAL
            self._btn_pack["state"] = tk.NORMAL

class SLG_TIMImageFrame(SLG_tigImageFrame):
    _to_what = '.bmp'
    strings_lib = {
        'eng': ('Choose the mode:',
                'Choose the TIM image file:',
                'Choose the bmp image file:',
                'TIM images',
                '*.TIM',
                'All files',
                '*',
                'Convert TIM to bmp (+ ._key, ._tech)',
                'Reconvert TIM from bmp (+ ._key, ._tech)',
                'Such archive is not exist!',
                'Such directory is not exist!',
                'Version/signature mismatch!',
                'Image successfully converted!',
                'Image successfully reconverted!',
                'Conversion in process...\nThis can take some time.\nFeel free to drink some tea.',
                'Reconversion in process...\nThis can take some time.\nFeel free to drink some tea.',
                'Files',
                'Directories',
                'Bmp images',
                '*.bmp',
                'Choose the directory with TIM images:',
                'Choose the directory with bmp images:',
                'Version: ',
                ),
        'rus': ('Выберите режим:',
                'Выберите картинку TIM:',
                'Выберите картинку bmp:',
                'Картинки TIM',
                '*.TIM',
                'Все файлы',
                '*',
                'Конвертировать TIM в bmp (+ ._key, ._tech)',
                'Реконвертировать TIM из bmp (+ ._key, ._tech)',
                'Сего файла не существует!',
                'Сей директории не существует!',
                'Несовпадение версии и сигнатуры!',
                'Конвертация прошла успешно!',
                'Реконвертация прошла успешно!',
                'Выполнение конвертации...\nСие может занять некоторое время.\nМожете пока попить чайку.',
                'Выполнение реконвертации...\nСие может занять некоторое время.\nМожете пока попить чайку.',
                'Файлы',
                'Директории',
                'Картинки bmp',
                '*.bmp',
                'Выберите папку с картинками TIM:',
                'Выберите папку с картинками bmp:',
                'Версия: '
                )
    }

    def _unpack_funcer(self):
        self._btn_unpack["state"] = tk.DISABLED
        self._btn_pack["state"] = tk.DISABLED
        try:
            if (self._mode.get() == 0):
                namer = self._file_dir.get()
                try:
                    if (namer[(0-len(self._to_what)):] != self._to_what):
                        namer += self._to_what
                except:
                    pass
                newImage = SLG_Images_TIM(self._file_arc.get(), namer, 0)
                newImage.convert()
            else:
                newImage = SLG_Images_TIM(self._file_arc.get(), self._file_dir.get(), 1)
                newImage.convert()
            self._set_new_msg(self.strings_lib[self._language][12])
        except FileNotFoundError as ex:
            if (self._mode.get() == 0):
                self._set_new_msg(self.strings_lib[self._language][9])
            else:
                self._set_new_msg(self.strings_lib[self._language][10])
        except SLG_ImagesError as ex:
            self._set_new_msg(self.strings_lib[self._language][11])
        except Exception as ex:
            self._set_new_msg(ex)
        finally:
            try:
                del newImage
            except:
                pass
            self._btn_unpack["state"] = tk.NORMAL
            self._btn_pack["state"] = tk.NORMAL
    def _pack_funcer(self):
        self._btn_unpack["state"] = tk.DISABLED
        self._btn_pack["state"] = tk.DISABLED
        try:
            if (self._mode.get() == 0):
                newImage = SLG_Images_TIM(self._file_dir.get(), self._file_arc.get(), 0)
                newImage.reconvert()
            else:
                newImage = SLG_Images_TIM(self._file_dir.get(), self._file_arc.get(), 1)
                newImage.reconvert()
            self._set_new_msg(self.strings_lib[self._language][13])
        except FileNotFoundError as ex:
            if (self._mode.get() == 0):
                self._set_new_msg(self.strings_lib[self._language][9])
            else:
                self._set_new_msg(self.strings_lib[self._language][10])
        except SLG_ImagesError as ex:
            self._set_new_msg(self.strings_lib[self._language][11])
        except Exception as ex:
            self._set_new_msg(ex)
        finally:
            try:
                del newImage
            except:
                pass
            self._btn_unpack["state"] = tk.NORMAL
            self._btn_pack["state"] = tk.NORMAL

class SLG_albImageFrame(SLG_tigImageFrame):
    _to_what = '.png'
    strings_lib = {
        'eng': ('Choose the mode:',
                'Choose the alb image file:',
                'Choose the png image file:',
                'Alb images',
                '*.alb',
                'All files',
                '*',
                'Convert alb to png',
                'Reconvert alb from png',
                'Such archive is not exist!',
                'Such directory is not exist!',
                'Version/signature mismatch!',
                'Image successfully converted!',
                'Image successfully reconverted!',
                'Conversion in process...\nThis can take some time.\nFeel free to drink some tea.',
                'Reconversion in process...\nThis can take some time.\nFeel free to drink some tea.',
                'Files',
                'Directories',
                'Png images',
                '*.png',
                'Choose the directory with alb images:',
                'Choose the directory with png images:',
                'Version: ',
                ),
        'rus': ('Выберите режим:',
                'Выберите картинку alb:',
                'Выберите картинку png:',
                'Картинки alb',
                '*.alb',
                'Все файлы',
                '*',
                'Конвертировать alb в png',
                'Реконвертировать alb из png',
                'Сего файла не существует!',
                'Сей директории не существует!',
                'Несовпадение версии и сигнатуры!',
                'Конвертация прошла успешно!',
                'Реконвертация прошла успешно!',
                'Выполнение конвертации...\nСие может занять некоторое время.\nМожете пока попить чайку.',
                'Выполнение реконвертации...\nСие может занять некоторое время.\nМожете пока попить чайку.',
                'Файлы',
                'Директории',
                'Картинки png',
                '*.png',
                'Выберите папку с картинками alb:',
                'Выберите папку с картинками png:',
                'Версия: '
                )
    }

    def __init__(self, master):
        super(SLG_MasterFrame, self).__init__()
        self.master = master
        self["background"] = 'white'
        self["relief"] = tk.RAISED
        self["borderwidth"] = 5

        self._language = 'eng'

        self._mode = tk.IntVar()
        self._file_arc = tk.StringVar()
        self._file_dir = tk.StringVar()
        self._version = tk.StringVar()

        self._lblversion = tk.Label(master=self,
                                 background='white',
                                 font=('Helvetica', 14))
        self._arc_versions = []
        for i in SLG_Images_alb.version_lib:
            self._arc_versions.append(SLG_Images_alb.getVersionFromSignature(i))
        self._arc_versions.append('???')
        self._version.set(self._arc_versions[0])
        self._cmb_choose_version = ttk.Combobox(
            master=self,
            font=('Helvetica', 14),
            values=self._arc_versions,
            textvariable=self._version,
            state='readonly'
        )
        self._lblversion.place(relx=0.0, rely=0.0, relwidth=0.5, relheight=0.1)
        self._cmb_choose_version.place(relx=0.5, rely=0.0, relwidth=0.5, relheight=0.1)

        self._mode.set(0)

        self._lblvers = tk.Label(master=self,
                                 background='white',
                                 font=('Helvetica', 14))
        self._mode_one = tk.Radiobutton(master=self,
                                        background='white',
                                        font=('Helvetica', 14),
                                        variable=self._mode,
                                        value=0)
        self._mode_two = tk.Radiobutton(master=self,
                                        background='white',
                                        font=('Helvetica', 14),
                                        variable=self._mode,
                                        value=1)
        self._mode_one.bind('<Button-1>', self._mode_change)
        self._mode_two.bind('<Button-1>', self._mode_change)
        self._lblvers.place(relx=0.0, rely=0.1, relwidth=1.0, relheight=0.05)
        self._mode_one.place(relx=0.0, rely=0.15, relwidth=0.5, relheight=0.05)
        self._mode_two.place(relx=0.5, rely=0.15, relwidth=0.5, relheight=0.05)

        self._lblszs = tk.Label(master=self,
                                background='white',
                                font=('Helvetica', 14))
        self._ent_arc = tk.Entry(
            master=self,
            textvariable=self._file_arc,
            font=('Helvetica', 8),
            borderwidth=5
        )
        self._btn_what_arc = tk.Button(
            master=self,
            command=self._what_arc,
            relief=tk.RAISED,
            font=('Helvetica', 14),
            text='...'
        )
        self._lbldir = tk.Label(master=self,
                                background='white',
                                font=('Helvetica', 14))
        self._ent_dir = tk.Entry(
            master=self,
            textvariable=self._file_dir,
            font=('Helvetica', 8),
            borderwidth=5
        )
        self._btn_what_dir = tk.Button(
            master=self,
            command=self._what_dir,
            relief=tk.RAISED,
            font=('Helvetica', 14),
            text='...'
        )
        self._lblszs.place(relx=0.0, rely=0.2, relwidth=1.0, relheight=0.1)
        self._ent_arc.place(relx=0.0, rely=0.3, relwidth=0.85, relheight=0.1)
        self._btn_what_arc.place(relx=0.85, rely=0.3, relwidth=0.15, relheight=0.1)
        self._lbldir.place(relx=0.0, rely=0.4, relwidth=1.0, relheight=0.1)
        self._ent_dir.place(relx=0.0, rely=0.5, relwidth=0.85, relheight=0.1)
        self._btn_what_dir.place(relx=0.85, rely=0.5, relwidth=0.15, relheight=0.1)

        self._btn_unpack = tk.Button(
            master=self,
            command=self._unpack,
            relief=tk.RAISED,
            font=('Helvetica', 12),
        )
        self._btn_pack = tk.Button(
            master=self,
            command=self._pack,
            relief=tk.RAISED,
            font=('Helvetica', 12),
        )
        self._txt_status = tk.Text(
            master=self,
            bg='white',
            state=tk.DISABLED,
        )

        self._btn_unpack.place(relx=0.0, rely=0.6, relwidth=1.0, relheight=0.1)
        self._btn_pack.place(relx=0.0, rely=0.7, relwidth=1.0, relheight=0.1)
        self._txt_status.place(relx=0.0, rely=0.8, relwidth=1.0, relheight=0.2)

    def translate_to(self, language):
        self._language = language
        self._lblvers["text"] = self.strings_lib[language][0]
        self._remake_razd_nadp(self._mode.get())
        self._btn_unpack["text"] = self.strings_lib[language][7]
        self._btn_pack["text"] = self.strings_lib[language][8]
        self._mode_one["text"] = self.strings_lib[language][16]
        self._mode_two["text"] = self.strings_lib[language][17]
        self._lblversion["text"] = self.strings_lib[language][22]

    def _unpack_funcer(self):
        self._btn_unpack["state"] = tk.DISABLED
        self._btn_pack["state"] = tk.DISABLED
        try:
            verser = self._version.get()
            if (verser == '???'):
                verser = 'none'
            if (self._mode.get() == 0):
                namer = self._file_dir.get()
                try:
                    if (namer[(0-len(self._to_what)):] != self._to_what):
                        namer += self._to_what
                except:
                    pass
                newImage = SLG_Images_alb(self._file_arc.get(), namer, 0, verser)
                newImage.convert()
            else:
                newImage = SLG_Images_alb(self._file_arc.get(), self._file_dir.get(), 1, verser)
                newImage.convert()
            self._set_new_msg(self.strings_lib[self._language][12])
        except FileNotFoundError as ex:
            if (self._mode.get() == 0):
                self._set_new_msg(self.strings_lib[self._language][9])
            else:
                self._set_new_msg(self.strings_lib[self._language][10])
        except SLG_ImagesError as ex:
            self._set_new_msg(self.strings_lib[self._language][11])
        except Exception as ex:
            self._set_new_msg(ex)
        finally:
            try:
                del newImage
            except:
                pass
            self._btn_unpack["state"] = tk.NORMAL
            self._btn_pack["state"] = tk.NORMAL
    def _pack_funcer(self):
        self._btn_unpack["state"] = tk.DISABLED
        self._btn_pack["state"] = tk.DISABLED
        try:
            verser = self._version.get()
            if (verser == '???'):
                verser = 'none'
            if (self._mode.get() == 0):
                newImage = SLG_Images_alb(self._file_dir.get(), self._file_arc.get(), 0, verser)
                newImage.reconvert()
            else:
                newImage = SLG_Images_alb(self._file_dir.get(), self._file_arc.get(), 1, verser)
                newImage.reconvert()
            self._set_new_msg(self.strings_lib[self._language][13])
        except FileNotFoundError as ex:
            if (self._mode.get() == 0):
                self._set_new_msg(self.strings_lib[self._language][9])
            else:
                self._set_new_msg(self.strings_lib[self._language][10])
        except SLG_ImagesError as ex:
            self._set_new_msg(self.strings_lib[self._language][11])
        except Exception as ex:
            self._set_new_msg(ex)
        finally:
            try:
                del newImage
            except:
                pass
            self._btn_unpack["state"] = tk.NORMAL
            self._btn_pack["state"] = tk.NORMAL

class SLG_VOIAudioFrame(SLG_tigImageFrame):
    _to_what = '.ogg'
    strings_lib = {
        'eng': ('Choose the mode:',
                'Choose the VOI audio file:',
                'Choose the ogg audio file:',
                'VOI audio',
                '*.VOI',
                'All files',
                '*',
                'Convert VOI to ogg (+ _.tech)',
                'Reconvert VOI from ogg (+ _.tech)',
                'Such archive is not exist!',
                'Such directory is not exist!',
                'Version/signature mismatch!',
                'Image successfully converted!',
                'Image successfully reconverted!',
                'Conversion in process...\nThis can take some time.\nFeel free to drink some tea.',
                'Reconversion in process...\nThis can take some time.\nFeel free to drink some tea.',
                'Files',
                'Directories',
                'Ogg audio',
                '*.ogg',
                'Choose the directory with VOI audio:',
                'Choose the directory with ogg audio:'
                ),
        'rus': ('Выберите режим:',
                'Выберите аудиофайл VOI:',
                'Выберите аудиофайл ogg:',
                'Аудиофайлы VOI',
                '*.VOI',
                'Все файлы',
                '*',
                'Конвертировать VOI в ogg (+ _.tech)',
                'Реконвертировать VOI из ogg (+ _.tech)',
                'Сего файла не существует!',
                'Сей директории не существует!',
                'Несовпадение версии и сигнатуры!',
                'Конвертация прошла успешно!',
                'Реконвертация прошла успешно!',
                'Выполнение конвертации...\nСие может занять некоторое время.\nМожете пока попить чайку.',
                'Выполнение реконвертации...\nСие может занять некоторое время.\nМожете пока попить чайку.',
                'Файлы',
                'Директории',
                'Аудиофайлы ogg',
                '*.ogg',
                'Выберите папку с аудиофайлами VOI:',
                'Выберите папку с аудиофайлами ogg:'
                )
    }
    def _unpack_funcer(self):
        self._btn_unpack["state"] = tk.DISABLED
        self._btn_pack["state"] = tk.DISABLED
        try:
            if (self._mode.get() == 0):
                namer = self._file_dir.get()
                try:
                    if (namer[(0-len(self._to_what)):] != self._to_what):
                        namer += self._to_what
                except:
                    pass
                newAudio = SLG_Audio_VOI(self._file_arc.get(), namer, 0)
                newAudio.convert()
            else:
                newAudio = SLG_Audio_VOI(self._file_arc.get(), self._file_dir.get(), 1)
                newAudio.convert()
            self._set_new_msg(self.strings_lib[self._language][12])
        except FileNotFoundError as ex:
            if (self._mode.get() == 0):
                self._set_new_msg(self.strings_lib[self._language][9])
            else:
                self._set_new_msg(self.strings_lib[self._language][10])
        except Exception as ex:
            self._set_new_msg(ex)
        finally:
            try:
                del newAudio
            except:
                pass
            self._btn_unpack["state"] = tk.NORMAL
            self._btn_pack["state"] = tk.NORMAL
    def _pack_funcer(self):
        self._btn_unpack["state"] = tk.DISABLED
        self._btn_pack["state"] = tk.DISABLED
        try:
            if (self._mode.get() == 0):
                newAudio = SLG_Audio_VOI(self._file_dir.get(), self._file_arc.get(), 0)
                newAudio.reconvert()
            else:
                newAudio = SLG_Audio_VOI(self._file_dir.get(), self._file_arc.get(), 1)
                newAudio.reconvert()
            self._set_new_msg(self.strings_lib[self._language][13])
        except FileNotFoundError as ex:
            if (self._mode.get() == 0):
                self._set_new_msg(self.strings_lib[self._language][9])
            else:
                self._set_new_msg(self.strings_lib[self._language][10])
        except Exception as ex:
            self._set_new_msg(ex)
        finally:
            try:
                del newAudio
            except:
                pass
            self._btn_unpack["state"] = tk.NORMAL
            self._btn_pack["state"] = tk.NORMAL