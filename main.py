#from SLG_Scripts import SLG_Scripts
from SLG_Images import SLG_Images_tig
from SLG_Images import SLG_Images_tic
from SLG_Images import SLG_Images_TIM
from SLG_Images import SLG_Images_alb
from SLG_Audio import SLG_Audio_VOI
from SLG_Archives import SLG_Archives_szs
from SLG_Archives import SLG_Archives_SFP
from SLG_GUI import SLG_GUI

#testmode = True
testmode = False

#Scripts were just barely ready, but there were some complications...
#I have no time for solving it right now, so maybe just create some other tool sometime.

#For structures decompiling wasn't always work good, and crutches are needed for every single game...
#And I thought it has one specific encryption on later versions, even tried cryptoattacked it...
#Bug, guess, not it... *Sigh*.
#So I need some time to rereverse it.

def test_script(dir, out_dir, out_name):
    #newScript = SLG_Scripts(dir, 'cp932', 0)
    newScript = SLG_Scripts(dir, 'cp932', 1)
    newScript.decompile(out_dir, out_name)

    #NominalSize:
    mainer = newScript.getNominalSizes()

    ##MainLin:
    #mainer = newScript.getStatMainLib()
    #mainer.sort(key=lambda main_el: main_el[0])

    ##Files:
    #mainer = newScript.getFileList()

#    for i in mainer:
#        print(i, mainer[i])
#        #print(i)

    del newScript

def image_tig_test():

    #newImage = SLG_Images_tig("bg12.tig", "bg12.png", 0)
    #newImage = SLG_Images_tig("castle.tig", "castle.png", 0)
    newImage = SLG_Images_tig("Bmp", "Bmp_new", 1)
    newImage.convert()
    del newImage

def image_TIM_test():
    #newImage = SLG_Images_TIM("武将情報.TIM", "_武将情報.bmp", 0)
    newImage = SLG_Images_TIM("_武将情報.bmp", "武将情報.TIM", 0)
    newImage.reconvert()
    del newImage

def image_alb_test():
    #newImage = SLG_Images_alb("bg01_hiru.alb", "bg01_hiru.png", 0, "none")
    newImage = SLG_Images_alb("bg01_hiru.png", "bg01_hiru.alb", 0, SLG_Images_alb.version_lib[0])
    #newImage.convert()
    newImage.reconvert()
    del newImage

def audio_VOI_test():
    #newAudio = SLG_Audio_VOI('fuji_0024.VOI', 'fuji_0024.ogg', 0)
    newAudio = SLG_Audio_VOI('fuji_0024.ogg', 'fuji_0024.VOI', 0)
    #newAudio.convert()
    newAudio.reconvert()
    del newAudio

def archive_szs_test():
    #newArchive = SLG_Archives_szs('ending.szs', 'ending', -1)
    newArchive = SLG_Archives_szs('ending', 'ending.szs', 0)
    #newArchive.unpack()
    newArchive.repack()
    del newArchive

def archive_SFP_test():
    #newArchive = SLG_Archives_SFP('slg_se.SPD', 'slg_se.SPL', 'slg_se', -1)
    newArchive = SLG_Archives_SFP('slg_se.SPD', 'slg_se.SPL', 'slg_se', 5)
    #newArchive.unpack()
    newArchive.repack()
    del newArchive

def file_test(file_one, file_two):
    file_one = open(file_one, 'rb')
    file_two = open(file_two, 'rb')

    byte_one = file_one.read(1)
    byte_two = file_two.read(1)
    count = 10
    i = 0
    while ((byte_one != b'') and (byte_two != b'') and (count >= 0)):
        if (byte_one != byte_two):
            count -= 1
            print(i, hex(byte_one[0]), hex(byte_two[0]))
        i += 1
        byte_one = file_one.read(1)
        byte_two = file_two.read(1)
    if (count == 10):
        print("Differences not found.")

    file_two.close()
    file_one.close()


if __name__ == '__main__':
    if (testmode):
        #test_script("main", "", "__temp_main.txt")
        #test_script("main", "test_script", "")
        #test_script("main_sengokuhime3", "test_script_sengokuhime3", "")

        #image_tig_test()

        #image_TIM_test()

        #image_alb_test()

        #audio_VOI_test()

        #archive_szs_test()

        #archive_SFP_test()

        #file_test("ending.szs", "_ending.szs")

        pass
    else:
        basic_GUI = SLG_GUI()