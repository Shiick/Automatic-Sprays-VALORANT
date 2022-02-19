import os
import cv2
import shutil
from PIL import Image

input_path = R"C:\Users\Shiick\Desktop\AutomaticSprays\ExportOutput\Game\Personalization\Sprays" # MAKE SURE TO CHANGE THOSE FOR WHAT WORKS ON YOUR END
output_path = R"C:\Users\Shiick\Desktop\AutomaticSprays\Output"
valorant_path = "C:\Riot Games\VALORANT\live\ShooterGame\Content\Paks"
AES = "0x4BE71AF2459CF83899EC9DC2CB60E22AC4B3047E0211034BBABE9D174C069DD6"

def main():
    export_files_umodel()
    export_sprays()
    delete_temp_folder() # DELETE TEMP FOLDER CONTAINING MASKS

def export_files_umodel():
    # THIS WILL EXPORT THE NEEDED FILES
    os.system("umodel.exe -path=\"" + valorant_path + "\" -aes=\"" + AES + "\" -game=valorant -out=\ExportOutput -export *Personalization/Sprays/*/*")

def export_sprays():
    # LOOP THROUGH ALL FILES IN INPUT_PATH
    for path, subdirs, files in os.walk(input_path):
        for name in files:
            file = os.path.join(path, name)
            if (file.endswith("DF.png") and has_aem_texture(file)): # IF SPRAY
                make_folders(path) # Creates folders required for that spray
                make_spray(file)

def delete_temp_folder():
    dir_path = output_path + os.path.sep + "TEMP"

    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))

def has_aem_texture(path):
    return os.path.exists(path.replace("DF.png", "AEM.png")) # Basically checks if the AEM file exists

def make_folders(path):
    # MAKE TEMPORARY FOLDER
    temp_path = output_path + os.path.sep + "TEMP" + path.replace(input_path, "")
    folder_list = temp_path.split(os.path.sep)
    if not os.path.exists('\\'.join(folder_list)):
        os.makedirs('\\'.join(folder_list))

    # MAKE OUTPUT FOLDERS
    final_path = output_path + path.replace(input_path, "")
    folder_list = final_path.split(os.path.sep)
    if not os.path.exists('\\'.join(folder_list)):
        os.makedirs('\\'.join(folder_list))

def make_spray(path):
    # READ AEM FILE
    aem_file = cv2.imread(path.replace("DF.png", "AEM.png"), cv2.IMREAD_UNCHANGED)

    # GET BLUE CHANNEL
    blue_channel = aem_file[:,:,0]

    new_path = output_path + "\\TEMP\\" + path.replace(input_path, "")
    mask_file_path = new_path.replace("_DF.png", ".png")
    # SAVE MASK FILE WITH ONLY THE BLUE CHANNEL
    cv2.imwrite(mask_file_path, blue_channel)

    # OPEN DF FILE
    df_file = Image.open(path)

    # CREATE EMPTY IMAGE TO HIDE UNWANTED PART
    empty = Image.new('RGBA', df_file.size)

    # OPEN MASK FILE
    mask = Image.open(mask_file_path)

    im = Image.composite(df_file, empty, mask) # COMBINE EVERY LAYER

    output = output_path + path.replace(input_path, "")

    im.save(output.replace("_DF", "")) # SAVE FILE

if __name__ == '__main__':
    main()