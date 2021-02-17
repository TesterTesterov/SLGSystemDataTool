import struct
import os

class SLG_Audio:
    #Определение.
    def __init__(self):
        self._fromer = ''
        self._toer = ''
        self._type = ''
        self._mode = -1

    #Основные методы взаимодействия с пользователем.
    def convert(self):
        if (self._mode == 0):
            self._convert_file(self._fromer, self._toer, False)
        elif (self._mode == 1):
            self._convert_files_in_dir(self._fromer, self._toer, False, self._type)
        else:
            raise SLG_AudioError("Wrong file/dir mode!")
    def reconvert(self):
        if (self._mode == 0):
            self._convert_file(self._fromer, self._toer, True)
        elif (self._mode == 1):
            self._convert_files_in_dir(self._fromer, self._toer, True, self._type)
        else:
            raise SLG_AudioError("Wrong file/dir mode!")

    #Основные технические методы:
    def _convert_file(self, fromer, toer, reverse):
        pass
    def _convert_files_in_dir(self, fromer, toer, reverse, type):
        pass

class SLG_Audio_VOI(SLG_Audio):
    #Определение.
    def __init__(self, fromer, toer, mode):
        super(SLG_Audio_VOI, self).__init__()

        self._fromer = fromer
        self._toer = toer
        self._type = '.ogg' #У VOI один режим.
        self._mode = mode

    #Основные технические методы:
    def _convert_file(self, fromer, toer, reverse):
        in_file = open(fromer, 'rb')
        out_file = open(toer, 'wb')
        if (reverse):
            ins_file = open(fromer + "._tech", 'rb')
            out_file.write(ins_file.read())
            ins_file.close()
            out_file.write(in_file.read())
        else:
            in_file.seek(0x1e, 0)
            tech_section = struct.unpack('B', in_file.read(1))[0] + 0x20
            in_file.seek(0, 0)
            outs_file = open(toer + "._tech", 'wb')
            outs_file.write(in_file.read(tech_section))
            outs_file.close()
            out_file.write(in_file.read())
        in_file.close()
        out_file.close()
    def _convert_files_in_dir(self, fromer, toer, reverse, type):
        if (not (os.path.exists(toer))):
            os.makedirs(toer)
        for subdir, dirs, files in os.walk(fromer):
            for file in files:
                try:
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
                        if ((new_this_file[-4:] == '.VOI') or (new_this_file[-4:] == '.voi')):
                            new_this_file = new_this_file[:-4]
                except:
                    pass
                new_this_file = os.path.join(toer, new_this_file)
                if (reverse):
                    new_this_file = str(new_this_file) + ".VOI"
                else:
                    new_this_file = str(new_this_file) + type
                self._convert_file(this_file, new_this_file, reverse)

class SLG_AudioError(Exception):
    def __init__(self, text):
        self.txt = text