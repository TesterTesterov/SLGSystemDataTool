import struct
import os
import time

class SLG_Archives:
    #Определение.
    def __init__(self):
        self._fromer = ''
        self._toer = ''
        self._version = 0

    #Основные методы взаимодействия с пользователем.
    def unpack(self):
        if (not (os.path.isfile(self._fromer))):
            raise FileNotFoundError("There is no such archive!")
        self._unpack(self._fromer, self._toer, self._version)
    def repack(self):
        if (not (os.path.isdir(self._fromer))):
            raise FileNotFoundError("There is no such directory!")
        self._pack(self._fromer, self._toer, self._version)
    def getVersion(self):
        return self._version

    #Основные технические методы.
    def _unpack(self, fromer, toer, version):
        pass
    def _pack(self, fromer, toer, version):
        pass

    #Вспомогательные технические методы.
    def _get_string_from_sea(self, byters, byter):
        k = 0
        try:
            while ((byters[k] != byter) and (k < len(byters))):
                k += 1
        except:
            pass
        return byters[:k].decode('cp932')
    def _get_string_to_sea(self, stringer, numer, byterer):
        byter = stringer.encode('cp932')
        if (len(byter) > numer):
            raise Exception("The string " + stringer + " is too big for " + str(numer) + " bytes!")
        strer = struct.pack('B', byterer)
        while (len(byter) < numer):
            byter += strer
        return byter

class SLG_Archives_szs(SLG_Archives):
    version_signature_library = (
        'SZS100__',
    )
    #Определение.
    def __init__(self, fromer, toer, version):
        super(SLG_Archives_szs, self).__init__()
        self._fromer = fromer
        self._toer = toer
        self._version = version

    #Основные технические методы.
    def _unpack(self, fromer, toer, version):
        file_in = open(fromer, 'rb')
        signature = self._get_string_from_sea(file_in.read(8), 0)
        if (self._version == -1):
            self._version = struct.unpack('I', file_in.read(4))[0]
        else:
            file_in.read(4)
        if (signature != self.version_signature_library[self._version]):
            raise SLG_ArchivesError("Version/signature mismatch: " + str(version) + " " +
                                    signature + " " + self.version_signature_library[self._version] + ".")
        files_num = struct.unpack('I', file_in.read(4))[0]

        files_lib = []
        for i in range(files_num):
            name = self._get_string_from_sea(file_in.read(256), 0).replace(';', os.sep)
            offset = struct.unpack('Q', file_in.read(8))[0]
            size = struct.unpack('Q', file_in.read(8))[0]
            files_lib.append([name, offset, size])
        time_zero = time.time()
        kostil = True
        for i in files_lib:
            file_in.seek(i[1], 0)
            path = os.path.join(toer, i[0])
            dir = os.path.split(path)[0]

            if (not (os.path.isdir(dir))):
                os.makedirs(dir)
            file_out = open(path, 'wb')
            for z in range(i[2]):
                file_out.write(struct.pack('B', file_in.read(1)[0] ^ 0x90))
            file_out.close()

            times = time.time()
            print(path + " extracted for " + str(times - time_zero) + " c.")
            time_zero = times

        file_in.close()
    def _pack(self, fromer, toer, version):
        file_out = open(toer, 'wb')
        file_out.write(self._get_string_to_sea(self.version_signature_library[version], 8, 0))
        file_out.write(struct.pack('I', self._version))
        allFiles = []
        for root, dirs, files in os.walk(fromer):
            for name in files:
                allFiles.append(os.path.join(root, name))
        offset = 272 * len(allFiles) + 16
        file_out.write(struct.pack('I', len(allFiles)))
        time_zero = time.time()
        ornot = len(fromer + os.sep)
        for i in allFiles:
            file_len = os.stat(i).st_size
            file_out.write(self._get_string_to_sea(i[ornot:].replace(os.sep, ';'), 256, 0))
            file_out.write(struct.pack('Q', offset))
            file_out.write(struct.pack('Q', file_len))
            offset += file_len
        for i in allFiles:
            file_iner = open(i, 'rb')
            new_byte = file_iner.read(1)
            while (new_byte != b''):
                file_out.write(struct.pack('B', new_byte[0] ^ 0x90))
                new_byte = file_iner.read(1)
            timez = time.time()
            print("File " + i + " successfully packed for " + str(timez - time_zero) + " c!")
            time_zero = timez
            file_iner.close()
        file_out.close()

class SLG_Archives_SFP(SLG_Archives):
    version_lib = (('5', 'none'),
                   )

    #Определение.
    def __init__(self, SPD, SPL, dir, version):
        super(SLG_Archives_SFP, self).__init__()
        self._SPD = SPD
        self._SPL = SPL
        self._dir = dir
        self._version = version

    #Основные методы взаимодействия с пользователем.
    def unpack(self):
        if ((not (os.path.isfile(self._SPD))) and (not (os.path.isfile(self._SPL)))):
            raise FileNotFoundError("There is no such archive!")
        self._unpacker(self._SPD, self._SPL, self._dir, self._version)
    def repack(self):
        if (not (os.path.isdir(self._dir))):
            raise FileNotFoundError("There is no such directory!")
        self._packer(self._SPD, self._SPL, self._dir, self._version)

    #Основные технические методы.
    def _unpacker(self, SPD, SPL, dir, version):
        file_in = open(SPL, 'rb')
        file_in.seek(8, 0)
        signature = struct.unpack('I', file_in.read(4))[0]
        if (self._version == -1):
            self._version = signature
        else:
            if (self._version != signature):
                raise SLG_ArchivesError("Version mismatch: " + str(self._version) + " with " + str(signature) + " from file!")
        files_mod = struct.unpack('I', file_in.read(4))[0]
        file_in.seek(32, 0)

        data_library = []
        files_num = 0
        while True:
            trer = []
            #Смещение имени.
            trer.append(struct.unpack('I', file_in.read(4))[0])
            #Размер.
            trer.append(struct.unpack('I', file_in.read(4))[0])
            #Часть смещения в SPD.
            trer.append(struct.unpack('I', file_in.read(4))[0]*files_mod)
            #Проверка на то, не закончилась ли доска файлов.
            if (struct.unpack('I', file_in.read(4))[0] != 0):
                break
            files_num += 1
            data_library.append(trer)

        time_zero = time.time()
        file_data = open(SPD, 'rb')
        for i in data_library:
            file_in.seek(i[0], 0)
            byter = file_in.read(1)
            sum_bytes = b''
            while ((byter != b'\x00') and (byter != b'')):
                sum_bytes += byter
                byter = file_in.read(1)
            strer = sum_bytes.decode('cp932')
            i.append(strer)

            file_data.seek(i[2], 0)
            path = os.path.join(dir, i[3])
            dir = os.path.split(path)[0]

            if (not (os.path.isdir(dir))):
                os.makedirs(dir)
            file_out = open(path, 'wb')
            file_out.write(file_data.read(i[1]))
            file_out.close()

            timez = time.time()
            print("File " + i[3] + " successfully unpacked for " + str(round(timez - time_zero, 3)) + "c!")
            time_zero = timez
        #for i in data_library:
        #    print(i, i[1]+i[2], (32-(i[1]+i[2])%32)%32)
        file_in.close()
        file_data.close()
    def _packer(self, SPD, SPL, dir, version):
        len_SPD = 1024
        len_SPL = 32
        allFiles = []
        for root, dirs, files in os.walk(dir):
            for name in files:
                #Имя, смещение имени, размер, смещение без модификатора.
                trer = []
                pather = os.path.join(root, name)
                size = os.stat(pather).st_size

                trer.append(pather)
                trer.append(0) #Позже вычислим.
                trer.append(size)
                trer.append(len_SPD//32)
                len_SPD += size + ((32-(size % 32)) % 32)
                len_SPL += 16

                allFiles.append(trer)
        out_data = open(SPD, 'wb')
        out_data.write(b'SFP\x00\x00\x00\x00\x00')
        out_data.write(struct.pack('I', version))
        out_data.write(struct.pack('I', 32))
        out_data.write(struct.pack('Q', len_SPD))
        out_data.write(bytes(1024-16-8))

        ornot = len(dir + os.sep)
        time_zero = time.time()
        for i in allFiles:
            i[1] = len_SPL
            file_name = i[0][ornot:]
            len_SPL += len(file_name.encode('cp932')) + 1
            in_file = open(i[0], 'rb')
            out_data.write(in_file.read())
            out_data.write(bytes((32-(os.stat(i[0]).st_size % 32)) % 32))
            in_file.close()

            timez = time.time()
            print("File " + i[0] + " successfully packed for " + str(round(timez - time_zero, 3)) + "c!")
            time_zero = timez
        out_data.close()

        out_list = open(SPL, 'wb')
        out_list.write(b'SFP\x00\x00\x00\x00\x00')
        out_list.write(struct.pack('I', version))
        out_list.write(struct.pack('I', 32))
        out_list.write(struct.pack('Q', len_SPL))
        out_list.write(bytes(32-16-8))
        for i in allFiles:
            #Имя, смещение имени, размер, смещение без модификатора.
            for k in range(1, 4):
                out_list.write(struct.pack('I', i[k]))
            out_list.write(bytes(4))
        for i in allFiles:
            file_name = i[0][ornot:]
            out_list.write(file_name.encode('cp932'))
            out_list.write(bytes(1))
        out_list.close()


class SLG_ArchivesError(Exception):
    def __init__(self, text):
        self.txt = text