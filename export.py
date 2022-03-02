import os
import cv2
import subprocess

VALORANT_PATH = R"C:\Riot Games\VALORANT\live\ShooterGame\Content\Paks"
AES = "0x4BE71AF2459CF83899EC9DC2CB60E22AC4B3047E0211034BBABE9D174C069DD6"

repo_path = os.path.dirname(os.path.realpath(__file__))
input_path = fR"{repo_path}\ExportOutput\Game\Personalization\Sprays"
output_path = fR"{repo_path}\Output"

def main() -> None:
    export_files_umodel()
    export_sprays()

def export_files_umodel():
    """EXPORT THE NEEDED FILES"""
    subprocess.run([
        'umodel.exe',
        f'-path="{VALORANT_PATH}"',
        f'-aes={AES}',
        '-game=valorant',
        '-out=ExportOutput',
        '-nomesh',
        '-nostat',
        '-noanim',
        '-export',
        '/Game/Personalization/Sprays/*/*'])

def export_sprays() -> None:
    """LOOP THROUGH ALL FILES IN INPUT_PATH"""
    for path, _, files in os.walk(input_path):
        for name in files:
            file = os.path.join(path, name)
            if (file.endswith("DF.png") and has_aem_texture(file)): # IF SPRAY
                make_folders(path) # Creates folders required for that spray
                make_spray(file)

def has_aem_texture(path: str) -> bool:
    """Checks if the AEM file exists"""
    return os.path.exists(path.replace("DF.png", "AEM.png"))

def make_folders(path: str) -> None:
    """MAKE OUTPUT FOLDERS"""
    final_path = output_path + path.replace(input_path, "")
    os.makedirs(final_path, exist_ok=True)

def make_spray(path: str) -> None:
    output = output_path + path.replace(input_path, "")

    bgra = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2BGRA)
    bgra[:, :, 3] = cv2.imread(path.replace("DF.png", "AEM.png"))[:, :, 0]

    cv2.imwrite(output.replace("_DF", ""), bgra)# , [cv2.IMWRITE_PNG_COMPRESSION, 1])

if __name__ == '__main__':
    main()
