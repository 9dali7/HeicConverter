import os
import time
from PIL import Image
import imageio.v2 as imageio 
import shutil

class HEICScanner:
    def __init__(self):
        self.desktop_path = None
        user_profile = os.environ.get("USERPROFILE", "")
        
        print(f"USERPROFILE: {user_profile}")
        
        onedrive_base_path = os.path.join(user_profile, "OneDrive")
        if os.path.exists(onedrive_base_path):
            for root, dirs, _ in os.walk(onedrive_base_path):
                if "Desktop" in dirs:
                    self.desktop_path = os.path.join(root, "Desktop")
                    break
        
        if not self.desktop_path or not os.path.exists(self.desktop_path):
            self.desktop_path = os.path.join(user_profile, "Desktop")
        
        if not self.desktop_path or not os.path.exists(self.desktop_path):
            specific_onedrive_path = os.path.join(user_profile, "OneDrive - inglesina.com", "Desktop")
            if os.path.exists(specific_onedrive_path):
                self.desktop_path = specific_onedrive_path
        
        if not os.path.exists(self.desktop_path):
            print(f"Impossibile trovare la cartella Desktop in {self.desktop_path}.")
            raise EnvironmentError(f"Unable to find Desktop folder at {self.desktop_path}")
        
        print(f"Found Desktop at: {self.desktop_path}")

        self.target_folder = os.path.join(self.desktop_path, "HeicConverts")

        if not os.path.exists(self.target_folder):
            print(f"Folder {self.target_folder} not found. Creating it...")
            os.makedirs(self.target_folder)
            print(f"Folder {self.target_folder} created.")

        self.heic_folder = os.path.join(self.target_folder, "Heic")
        self.png_folder = os.path.join(self.target_folder, "Png")
        self.not_converted_folder = os.path.join(self.target_folder, "NotConverted")

        if not os.path.exists(self.heic_folder):
            os.makedirs(self.heic_folder)
        if not os.path.exists(self.png_folder):
            os.makedirs(self.png_folder)
        if not os.path.exists(self.not_converted_folder):
            os.makedirs(self.not_converted_folder)

    def scan_and_convert(self):
        processed_files = set()

        while True:
            for file in os.listdir(self.target_folder):
                file_path = os.path.join(self.target_folder, file)
                if os.path.isdir(file_path):
                    continue
                
                if file.lower().endswith(".heic"):
                    if file_path not in processed_files:
                        self.convert_heic_to_png(file_path)
                        processed_files.add(file_path)
                else:
                    if file_path not in processed_files:
                        self.move_file(file_path, self.not_converted_folder)
                        processed_files.add(file_path)
            
            time.sleep(10)

    def convert_heic_to_png(self, heic_file_path):
        try:
            heic_image = imageio.imread(heic_file_path)
            
            image = Image.fromarray(heic_image)
            
            png_file_path = os.path.splitext(heic_file_path)[0] + ".png"
            image.save(png_file_path, format="PNG")
            
            print(f"Converted: {heic_file_path} to {png_file_path}")

            self.move_file(heic_file_path, self.heic_folder)

            self.move_file(png_file_path, self.png_folder)
            
        except Exception as e:
            print(f"Error converting {heic_file_path}: {str(e)}")

    def move_file(self, file_path, target_folder):
        try:
            if os.path.exists(file_path):
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                
                shutil.move(file_path, os.path.join(target_folder, os.path.basename(file_path)))
                print(f"Moved: {file_path} to {target_folder}")
        except Exception as e:
            print(f"Error moving {file_path}: {str(e)}")

def main():
    try:
        scanner = HEICScanner()
        scanner.scan_and_convert()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 
