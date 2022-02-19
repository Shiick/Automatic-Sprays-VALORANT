import os
import cv2
import shutil

repo_path = R"D:\VALORANT\AutomaticSprays"

input_path = fR"{repo_path}\ExportOutput\Game\Personalization\Sprays"
output_path = fR"{repo_path}\Output"
valorant_path = R"C:\Riot Games\VALORANT\live\ShooterGame\Content\Paks"
AES = "0x4BE71AF2459CF83899EC9DC2CB60E22AC4B3047E0211034BBABE9D174C069DD6"

def main():
    export_files_umodel()
    export_sprays()
    delete_temp_folder() # DELETE TEMP FOLDER CONTAINING MASKS

def export_files_umodel():
    # THIS WILL EXPORT THE NEEDED FILES
    os.system(f'umodel.exe -path="{valorant_path}" -aes={AES} -game=valorant -out=ExportOutput -export *Personalization/Sprays/*')

def export_sprays():
    # LOOP THROUGH ALL FILES IN INPUT_PATH
    for path, _, files in os.walk(input_path):
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
        print(f"Error: {dir_path} : {e.strerror}")

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
    output = output_path + path.replace(input_path, "")

    bgra = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2BGRA)
    bgra[:, :, 3] = cv2.imread(path.replace("DF.png", "AEM.png"))[:, :, 0]

    cv2.imwrite(output.replace("_DF", ""), bgra)# , [cv2.IMWRITE_PNG_COMPRESSION, 1])

if __name__ == '__main__':
    main()
