import os
import time
from PIL import Image
import imageio.v2 as imageio  # Fixed the import to avoid deprecation warning
import shutil

class HEICScanner:
    def __init__(self):
        # Try to find Desktop folder under OneDrive, including domain-based folder names
        self.desktop_path = None
        user_profile = os.environ.get("USERPROFILE", "")
        
        # Add print statement to debug USERPROFILE
        print(f"USERPROFILE: {user_profile}")
        
        # First check if OneDrive exists (it may be under "OneDrive - <domain>")
        onedrive_base_path = os.path.join(user_profile, "OneDrive")
        if os.path.exists(onedrive_base_path):
            # Look for Desktop under OneDrive (including domain names like "OneDrive - someDomain")
            for root, dirs, _ in os.walk(onedrive_base_path):
                if "Desktop" in dirs:
                    self.desktop_path = os.path.join(root, "Desktop")
                    break
        
        # If OneDrive isn't found or Desktop wasn't found in OneDrive, fall back to regular Desktop
        if not self.desktop_path or not os.path.exists(self.desktop_path):
            self.desktop_path = os.path.join(user_profile, "Desktop")
        
        # Explicitly check for the "OneDrive - inglesina.com" Desktop folder
        if not self.desktop_path or not os.path.exists(self.desktop_path):
            specific_onedrive_path = os.path.join(user_profile, "OneDrive - inglesina.com", "Desktop")
            if os.path.exists(specific_onedrive_path):
                self.desktop_path = specific_onedrive_path
        
        # Verifica che la cartella Desktop esista
        if not os.path.exists(self.desktop_path):
            print(f"Impossibile trovare la cartella Desktop in {self.desktop_path}.")
            raise EnvironmentError(f"Unable to find Desktop folder at {self.desktop_path}")
        
        print(f"Found Desktop at: {self.desktop_path}")

        # Define the target folder (HeicConverts) on Desktop
        self.target_folder = os.path.join(self.desktop_path, "HeicConverts")

        # Check if the folder exists, if not, create it
        if not os.path.exists(self.target_folder):
            print(f"Folder {self.target_folder} not found. Creating it...")
            os.makedirs(self.target_folder)
            print(f"Folder {self.target_folder} created.")

        # Define the Heic, Png, and NotConverted folders
        self.heic_folder = os.path.join(self.target_folder, "Heic")
        self.png_folder = os.path.join(self.target_folder, "Png")
        self.not_converted_folder = os.path.join(self.target_folder, "NotConverted")

        # Create the necessary folders if they do not exist
        if not os.path.exists(self.heic_folder):
            os.makedirs(self.heic_folder)
        if not os.path.exists(self.png_folder):
            os.makedirs(self.png_folder)
        if not os.path.exists(self.not_converted_folder):
            os.makedirs(self.not_converted_folder)

    def scan_and_convert(self):
        # Create a set to track processed files to avoid converting the same file repeatedly
        processed_files = set()

        while True:
            # Walk through only files directly in the target folder (not subdirectories)
            for file in os.listdir(self.target_folder):
                file_path = os.path.join(self.target_folder, file)
                # Skip if it's a directory (we don't want to walk into subdirectories like Heic, Png, or NotConverted)
                if os.path.isdir(file_path):
                    continue
                
                if file.lower().endswith(".heic"):
                    # Process .heic files only if they haven't been processed yet
                    if file_path not in processed_files:
                        self.convert_heic_to_png(file_path)
                        processed_files.add(file_path)
                else:
                    # Move non-HEIC files to NotConverted folder
                    if file_path not in processed_files:
                        self.move_file(file_path, self.not_converted_folder)
                        processed_files.add(file_path)
            
            # Wait for a short period before checking again (e.g., 10 seconds)
            time.sleep(10)

    def convert_heic_to_png(self, heic_file_path):
        try:
            # Read the HEIC image using imageio
            heic_image = imageio.imread(heic_file_path)
            
            # Convert to PIL Image for further handling
            image = Image.fromarray(heic_image)
            
            # Save as PNG in the same directory as the original HEIC file
            png_file_path = os.path.splitext(heic_file_path)[0] + ".png"
            image.save(png_file_path, format="PNG")
            
            # Optionally print out the conversion process (for debugging or logs)
            print(f"Converted: {heic_file_path} to {png_file_path}")

            # Move the original HEIC file to the Heic folder
            self.move_file(heic_file_path, self.heic_folder)

            # Move the newly created PNG file to the Png folder
            self.move_file(png_file_path, self.png_folder)
            
        except Exception as e:
            # Print any errors in conversion
            print(f"Error converting {heic_file_path}: {str(e)}")

    def move_file(self, file_path, target_folder):
        try:
            # Move the file to the target folder
            if os.path.exists(file_path):
                # Ensure the target folder exists
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                
                # Move the file
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
    main()  # Automatically runs the conversion without any UI
