import os
import struct
import time

class SLG_Images:
    #Определение.
    def __init__(self):
        self._fromer = ''
        self._toer = ''
        self._type = ''
        self._mode = -1

    #Основные методы взаимодействия с пользователями.
    def convert(self):
        if (self._mode == 0):
            self._convert_file(self._fromer, self._toer, False)
        elif (self._mode == 1):
            self._convert_files_in_dir(self._fromer, self._toer, False, self._type)
        else:
            raise SLG_ImagesError("Wrong file/dir mode!")
    def reconvert(self):
        if (self._mode == 0):
            self._convert_file(self._fromer, self._toer, True)
        elif (self._mode == 1):
            self._convert_files_in_dir(self._fromer, self._toer, True, self._type)
        else:
            raise SLG_ImagesError("Wrong file/dir mode!")

    #Основные технические методы:
    def _convert_file(self, fromer, toer, reverse):
        pass
    def _convert_files_in_dir(self, fromer, toer, reverse, type):
        pass

    #Прочие технические методы:
    def _key_count(self, key_base):
        new_key = key_base
        new_key *= 0x0343fd
        new_key += 0x269ec3
        return new_key
    def _key_num(self, key_base):
        return ((key_base >> 16) & 0xff)
    def _create_key_table(self, key_base, key_size, firster):
        tabler = []
        for i in range(key_size):
            if (firster):
                tabler.append(key_base)
                firster = False
                continue
            key_base = self._key_count(key_base)
            if (key_base >= 4_294_967_296):
                key_base %= 4_294_967_296
            tabler.append(key_base)
        return tabler

class SLG_Images_tig(SLG_Images):
    def __init__(self, fromer, toer, mode):
        super(SLG_Images_tig, self).__init__()

        self._fromer = fromer
        self._toer = toer
        self._mode = mode #0 - файл -> файл. 1 - директория -> директория.
        #self.__type = type #png, jpg...
        self._type = ".png" #У tig лишь один вариант.

    #Основные технические методы:
    def _convert_file(self, fromer, toer, reverse):
        key = 0x7f7f7f7f
        file_in = open(fromer, 'rb')
        file_out = open(toer, 'wb')
        all_lenner = os.stat(fromer).st_size

        z = 0
        i = 0
        timer_zero = time.time()

        current_bytes = file_in.read(1)
        print("====== " + fromer + ": Status/Статус:")
        while (current_bytes != b''):
            if (key >= 4_294_967_296):
                key %= 4_294_967_296
            if ((i % (all_lenner // 5)) == 0):
                times = time.time()
                timer_new = times - timer_zero
                timer_zero = times
                print(str(z) + "%... " + str(round(timer_new, 3)) + " с.")
                z += 20
            key = self._key_count(key)
            inter = struct.unpack('B', current_bytes)[0]
            if (reverse):
                inter += self._key_num(key)
            else:
                inter -= self._key_num(key)
            inter %= 256
            current_bytes = struct.pack('B', inter)
            file_out.write(current_bytes)

            current_bytes = file_in.read(1)
            i += 1
        timer_new = time.time() - timer_zero
        if (z <= 100):
            print(fromer + ": " + str(z) + "%... " + str(round(timer_new, 3)) + " с.")
        file_in.close()
        file_out.close()
    def _convert_files_in_dir(self, fromer, toer, reverse, type):
        if (not (os.path.exists(toer))):
            os.makedirs(toer)
        for subdir, dirs, files in os.walk(fromer):
            for file in files:
                this_file = os.path.join(subdir, file)
                errer = this_file.split(os.sep)
                errer.pop(0)
                new_this_file = errer[0]
                errer.pop(0)
                for i in errer:
                    os.path.join(new_this_file, i)
                try:
                    if (reverse):
                        lenser = 0 - len(type)
                        if (new_this_file[lenser:] == type):
                            new_this_file = new_this_file[:lenser]
                    else:
                        if (new_this_file[-4:] == '.tig'):
                            new_this_file = new_this_file[:-4]
                except:
                    pass
                new_this_file = os.path.join(toer, new_this_file)
                if (reverse):
                    new_this_file = str(new_this_file) + ".tig"
                else:
                    new_this_file = str(new_this_file) + type
                self._convert_file(this_file, new_this_file, reverse)

class SLG_Images_tic(SLG_Images):
    def __init__(self, fromer, toer, mode):
        super(SLG_Images_tic, self).__init__()

        self._fromer = fromer
        self._toer = toer
        self._mode = mode #0 - файл -> файл. 1 - директория -> директория.
        #self.__type = type #png, jpg...
        self._type = ".jpg" #У tig лишь один вариант.

    #Основные технические методы:
    def _convert_file(self, fromer, toer, reverse):
        key = 0x7f7f7f7f
        file_in = open(fromer, 'rb')
        file_out = open(toer, 'wb')
        all_lenner = os.stat(fromer).st_size

        z = 0
        i = 0
        timer_zero = time.time()

        current_bytes = file_in.read(1)
        print("====== " + fromer + ": Status/Статус:")
        while (current_bytes != b''):
            if (key >= 4_294_967_296):
                key %= 4_294_967_296
            if ((i % (all_lenner // 5)) == 0):
                times = time.time()
                timer_new = times - timer_zero
                timer_zero = times
                print(str(z) + "%... " + str(round(timer_new, 3)) + " с.")
                z += 20
            key = self._key_count(key)
            inter = struct.unpack('B', current_bytes)[0]
            if (reverse):
                inter += self._key_num(key)
            else:
                inter -= self._key_num(key)
            inter %= 256
            current_bytes = struct.pack('B', inter)
            file_out.write(current_bytes)

            current_bytes = file_in.read(1)
            i += 1
        timer_new = time.time() - timer_zero
        if (z <= 100):
            print(fromer + ": " + str(z) + "%... " + str(round(timer_new, 3)) + " с.")
        file_in.close()
        file_out.close()
    def _convert_files_in_dir(self, fromer, toer, reverse, type):
        if (not (os.path.exists(toer))):
            os.makedirs(toer)
        for subdir, dirs, files in os.walk(fromer):
            for file in files:
                this_file = os.path.join(subdir, file)
                errer = this_file.split(os.sep)
                errer.pop(0)
                new_this_file = errer[0]
                errer.pop(0)
                for i in errer:
                    os.path.join(new_this_file, i)
                try:
                    if (reverse):
                        lenser = 0 - len(type)
                        if (new_this_file[lenser:] == type):
                            new_this_file = new_this_file[:lenser]
                    else:
                        if (new_this_file[-4:] == '.tic'):
                            new_this_file = new_this_file[:-4]
                except:
                    pass
                new_this_file = os.path.join(toer, new_this_file)
                if (reverse):
                    new_this_file = str(new_this_file) + ".tic"
                else:
                    new_this_file = str(new_this_file) + type
                self._convert_file(this_file, new_this_file, reverse)

class SLG_Images_TIM(SLG_Images):
    def __init__(self, fromer, toer, mode):
        super(SLG_Images_TIM, self).__init__()

        self._fromer = fromer
        self._toer = toer
        self._mode = mode #0 - файл -> файл. 1 - директория -> директория.
        #self.__type = type #png, jpg...
        self._type = ".bmp" #Выход и вход будут лишь в .bmp.

    #Основные технические методы.
    def _convert_file(self, fromer, toer, reverse):
        file_in = open(fromer, 'rb')
        file_out = open(toer, 'wb')
        all_lenner = os.stat(fromer).st_size

        if (reverse):
            file_ins = open(fromer + "._tech", 'rb')
            file_out.write(file_ins.read(512))
            file_ins.close()
            file_ins = open(fromer + "._key", 'r')
            key = int(file_ins.readline().split(" ")[1][2:], 16)
            file_in.read(2+4+2+2+4)
            header_len = struct.unpack('I', file_in.read(4))[0]
            #Размер изображения = all_lenner - header_len - 14.
            width = struct.unpack('I', file_in.read(4))[0]
            height = struct.unpack('I', file_in.read(4))[0]
            image_len = all_lenner - header_len - 14
            stride = image_len // height
            file_in.read(header_len - 4 - 4 - 4) # - 4 - 4

            good_header = b''
            good_header += bytes(72)
            good_header += struct.pack('I', width)
            good_header += bytes(80)
            good_header += struct.pack('I', height)
            good_header += bytes(26)
            good_header += struct.pack('I', stride)
            good_header += bytes(32)
            good_header += b'TIM Data Ver 1.00'
            good_header += bytes(273)
            if (len(good_header) != 512):
                raise SLG_ImagesError("TIM header size is not matching!")
            for i in range(512):
                key = self._key_count(key)
                if (key >= 4_294_967_296):
                    key %= 4_294_967_296
                inter = good_header[i]
                inter += self._key_num(key)
                inter %= 256
                file_out.write(struct.pack('B', inter))

            tablerer = self._create_key_table(key, 0x1000, True)
            z = tablerer.index(key)+1

            current_byte = file_in.read(1)
            while (current_byte != b''):
                inter = current_byte[0]
                inter += self._key_num(tablerer[z % len(tablerer)])
                inter %= 256
                file_out.write(struct.pack('B', inter))
                current_byte = file_in.read(1)
                z += 1
        else:
            header = file_in.read(1024)
            key = (header[18] | header[42] << 8 | header[98] << 16 | header[118] << 24) % 4_294_967_296
            file_outs = open(toer + "._key", 'w')
            file_outs.write("key: " + hex(key))
            file_outs.close()
            file_outs = open(toer + "._tech", 'wb')
            file_outs.write(header[:512])
            file_outs.close()
            good_header = b''

            for i in range(512, 1024):
                key = self._key_count(key)
                if (key >= 4_294_967_296):
                    key %= 4_294_967_296
                inter = header[i]
                inter -= self._key_num(key)
                inter %= 256
                good_header += struct.pack('B', inter)
            width = struct.unpack('I', good_header[72:76])[0]
            height = struct.unpack('I', good_header[156:160])[0]
            stride = struct.unpack('I', good_header[186:190])[0]
            print(width, height, stride)


            file_out.write(b'BM')
            file_out.write(struct.pack('I', all_lenner-1024+54))
            file_out.write(struct.pack('H', 0))
            file_out.write(struct.pack('H', 0))
            file_out.write(struct.pack('I', 54))

            file_out.write(struct.pack('I', 40))
            file_out.write(struct.pack('I', width))
            file_out.write(struct.pack('I', height))
            file_out.write(struct.pack('H', 1))
            file_out.write(struct.pack('H', 24))
            file_out.write(struct.pack('I', 0))
            file_out.write(struct.pack('I', all_lenner-1024))
            file_out.write(struct.pack('I', 3780))
            file_out.write(struct.pack('I', 3780))
            file_out.write(struct.pack('I', 0))
            file_out.write(struct.pack('I', 0))

            tablerer = self._create_key_table(key, 0x1000, True)
            z = tablerer.index(key)+1

            current_byte = file_in.read(1)
            while (current_byte != b''):
                inter = current_byte[0]
                inter -= self._key_num(tablerer[z % len(tablerer)])
                inter %= 256
                file_out.write(struct.pack('B', inter))
                current_byte = file_in.read(1)
                z += 1

        file_in.close()
        file_out.close()
    def _convert_files_in_dir(self, fromer, toer, reverse, type):
        if (not (os.path.exists(toer))):
            os.makedirs(toer)
        for subdir, dirs, files in os.walk(fromer):
            for file in files:
                try:
                    if (file[-5:] == '._key'):
                        continue
                    if (file[-6:] == '._tech'):
                        continue
                except:
                    pass
                this_file = os.path.join(subdir, file)
                errer = this_file.split(os.sep)
                errer.pop(0)
                new_this_file = errer[0]
                errer.pop(0)
                for i in errer:
                    os.path.join(new_this_file, i)
                try:
                    if (reverse):
                        lenser = 0 - len(type)
                        if (new_this_file[lenser:] == type):
                            new_this_file = new_this_file[:lenser]
                    else:
                        if (new_this_file[-4:] == '.TIM'):
                            new_this_file = new_this_file[:-4]
                except:
                    pass
                new_this_file = os.path.join(toer, new_this_file)
                if (reverse):
                    new_this_file = str(new_this_file) + ".TIM"
                else:
                    new_this_file = str(new_this_file) + type
                self._convert_file(this_file, new_this_file, reverse)

class SLG_Images_alb(SLG_Images):
    version_lib =\
        [
        "ALB1.21\00",
        ]
    #Определение.
    def __init__(self, fromer, toer, mode, version):
        super(SLG_Images_alb, self).__init__()

        self._fromer = fromer
        self._toer = toer
        self._mode = mode #0 - файл -> файл. 1 - директория -> директория.
        #self.__type = type #png, jpg...
        self._type = ".png" #alb может быть лишь png...
        self._version = version
        #self._shag = 524
        self._shag = 0xffff

    #Основные методы взаимодействия с пользователем.
    def getVersion(self):
        return self._version
    def getShag(self):
        return self._shag
    def setShag(self, shag):
        self._shag = shag

    #Основные технические методы.
    def _convert_file(self, fromer, toer, reverse):
        in_file = open(fromer, 'rb')
        out_file = open(toer, 'wb')
        if (reverse):
            def _create_standart_table(next_section):
                dict = b'PH'
                dict += struct.pack('H', 256*2)
                dict += struct.pack('H', next_section)
                dict += struct.pack('B', 0)
                dict += struct.pack('B', 0)
                for i in range(256):
                    dict += struct.pack('B', i)
                    dict += struct.pack('B', 1)
                return dict

            out_file.write(self.getSignatureFromVersion(self._version).encode('cp932'))
            out_file.write(struct.pack('Q', os.stat(fromer).st_size))

            new_bytes = in_file.read(self._shag)
            while (new_bytes != b''):
                actual_len = len(new_bytes)
                dictionary = _create_standart_table(actual_len)
                out_file.write(dictionary)
                out_file.write(new_bytes)
                new_bytes = in_file.read(self._shag)

        else:
            version = self.getVersionFromSignature(in_file.read(8).decode('cp932'))
            if (self._version == 'none'):
                self._version = version
            else:
                if (self._version != version):
                    raise SLG_ImagesError("Version mismatch: nominal "
                                          + self._version + " with practical " + version + "!")
            unpacked_size = struct.unpack('Q', in_file.read(8))[0]
            print("File size (real, unpacked):", os.stat(fromer).st_size, unpacked_size)

            def _unpackDictNew():
                dictionary = []
                for z in range(256):
                    dictionary.append([0, 0])
                if (in_file.read(2) != b'PH'):
                    raise SLG_ImagesError("Unsupported version of alb format!")
                tsizer = struct.unpack('H', in_file.read(2))[0]
                psizer = struct.unpack('H', in_file.read(2))[0]
                print("Section sizers", tsizer, psizer)
                packed = struct.unpack('B', in_file.read(1))[0]
                pack_flag = True
                if (packed == 0):
                    pack_flag = False
                definer = struct.unpack('B', in_file.read(1))[0]
                i = 0

                fromer = in_file.read(tsizer)
                fromer_reader = 0
                if (pack_flag):
                    while (i < 256):
                        new_byte = fromer[fromer_reader]
                        fromer_reader += 1
                        if (new_byte == definer):
                            counter = fromer[fromer_reader]
                            fromer_reader += 1
                            for z in range(counter):
                                terr = []
                                terr.append(i)
                                terr.append(0)
                                dictionary[i] = terr
                                i += 1
                        else:
                            terr = []
                            terr.append(new_byte)
                            terr.append(fromer[fromer_reader])
                            fromer_reader += 1
                            dictionary[i] = terr
                            i += 1
                else:
                    for i in range(256):
                        terr = []
                        for zzz in range(2):
                            terr.append(fromer[fromer_reader])
                            fromer_reader += 1
                        dictionary[i] = terr
                        i += 1
                return dictionary, psizer

            section_number = 0
            while (in_file.tell() != os.stat(fromer).st_size):
                section_number += 1
                dict, psize = _unpackDictNew()
                evil_bytes = in_file.read(psize)
                good_bytes = b''
                read_bytes = 0
                stack = []
                while (True):
                    byter = 0
                    if (len(stack) != 0):
                        byter = stack.pop()
                    elif (read_bytes < len(evil_bytes)):
                        byter = evil_bytes[read_bytes]
                        read_bytes += 1
                    else:
                        break
                    if (byter == dict[byter][0]):
                        good_bytes += struct.pack('B', byter)
                    else:
                        stack.append(dict[byter][1])
                        stack.append(dict[byter][0])
                #print(len(good_bytes))
                out_file.write(good_bytes)
            print("Number of sections", section_number)
            stack = []

        in_file.close()
        out_file.close()
    def _convert_files_in_dir(self, fromer, toer, reverse, type):
        if (not (os.path.exists(toer))):
            os.makedirs(toer)
        for subdir, dirs, files in os.walk(fromer):
            for file in files:
                this_file = os.path.join(subdir, file)
                errer = this_file.split(os.sep)
                errer.pop(0)
                new_this_file = errer[0]
                errer.pop(0)
                for i in errer:
                    os.path.join(new_this_file, i)
                try:
                    if (reverse):
                        lenser = 0 - len(type)
                        if (new_this_file[lenser:] == type):
                            new_this_file = new_this_file[:lenser]
                    else:
                        if (new_this_file[-4:] == '.alb'):
                            new_this_file = new_this_file[:-4]
                except:
                    pass
                new_this_file = os.path.join(toer, new_this_file)
                if (reverse):
                    new_this_file = str(new_this_file) + ".alb"
                else:
                    new_this_file = str(new_this_file) + type
                self._convert_file(this_file, new_this_file, reverse)

    #Вспомогательные технические методы.
    @staticmethod
    def getSignatureFromVersion(version):
        return "ALB" + version + '\x00'
    @staticmethod
    def getVersionFromSignature(signature):
        return signature[3:-1]


class SLG_ImagesError(Exception):
    def __init__(self, text):
        self.txt = text