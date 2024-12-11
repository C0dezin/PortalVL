import os
import shutil
import requests
import zipfile

def download_zip(url, output_path):
    print("Downloading ZIP file...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_path, "wb") as file:
            shutil.copyfileobj(response.raw, file)
        print("Download completed!")
    else:
        print(f"Error downloading file: {response.status_code}")
        raise Exception("Download failed")

def extract_zip(zip_path, target_path):
    print("Extracting files from ZIP...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in zip_ref.namelist():
            target_file_path = os.path.join(target_path, os.path.basename(member))
            if not member.endswith('/'):
                os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
                with zip_ref.open(member) as source, open(target_file_path, 'wb') as target:
                    shutil.copyfileobj(source, target)
    print("Extraction completed!")

def replace_vo_in_source_unpack(source_unpack_path, extracted_vo_folder):
    print("Replacing voice lines in Source Unpack...")
    target_path = os.path.join(source_unpack_path, "portal/sound/vo/aperture_ai")
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"Target folder not found: {target_path}")

    for file in os.listdir(extracted_vo_folder):
        source_file = os.path.join(extracted_vo_folder, file)
        target_file = os.path.join(target_path, file)
        
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        shutil.copy2(source_file, target_file)
        print(f"Replaced: {file}")
    print("Replacement completed!")

def apply_minimal_voice_lines_preset(source_unpack_path):
    print("Applying Minimal Voice Lines preset...")
    target_path = os.path.join(source_unpack_path, "portal/sound/vo/aperture_ai")
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"Target folder not found: {target_path}")

    allowed_files = {
        "00_part1_entry-7.wav",
        "00_part2_success-1.wav",
        "02_part2_success-2.wav",
        "06_part1_entry-1.wav",
        "11_part1_entry-3.wav",
        "13_part1_entry-1.wav",
        "14_part1_end-2.wav",
        "ding_off.wav",
        "ding_on.wav",
        "escape_02_spheredestroy2-00.wav",
        "escape_02_ballhitpain-02.wav",
        "escape_02_entry-04.wav",
        "escape_02_miscbabble-10.wav",
        "escape_02_sphere_Death_Scream.wav",
        "escape_02_spheredestroy1-01.wav",
        "escape_02_spheredestroy1-06.wav",
        "escape_02_spheredestroy3-01.wav"
    }

    for file in os.listdir(target_path):
        if file not in allowed_files:
            os.remove(os.path.join(target_path, file))
            print(f"Removed: {file}")
    print("Minimal Voice Lines preset applied successfully!")

def main():
    print("=== Portal Source Unpack Voice Line Replacer ===")
    print("1. German")
    print("2. English")
    print("3. French")
    print("4. Russian")
    print("5. Minimal Voice Lines Preset")
    print("6. Exit")

    try:
        choice = int(input("Choose an option (1-6): ").strip())
        if choice == 6:
            print("Exiting the program.")
            return

        language_map = {1: "german", 2: "english", 3: "french", 4: "russian"}
        if choice not in language_map and choice != 5:
            print("Invalid option. Please try again.")
            return

        if choice == 5:
            source_unpack_path = input("Enter the path to the Source Unpack folder (not on unpack/portal): ").strip()
            apply_minimal_voice_lines_preset(source_unpack_path)
            return

        language = language_map[choice]
        zip_url = f"https://0x0.c0de.wtf/portalVL/{language}.zip"
        zip_download_path = f"{language}.zip"
        source_unpack_path = input("Enter the path to the Source Unpack folder (not on unpack/portal): ").strip()
        extracted_folder = f"extracted_{language}"

        download_zip(zip_url, zip_download_path)
        os.makedirs(extracted_folder, exist_ok=True)
        extract_zip(zip_download_path, extracted_folder)
        replace_vo_in_source_unpack(source_unpack_path, extracted_folder)

        apply_preset = input("Do you want to apply the Minimal Voice Lines preset? (y/n): ").strip().lower()
        if apply_preset == 'y':
            apply_minimal_voice_lines_preset(source_unpack_path)

        os.remove(zip_download_path) 
        shutil.rmtree(extracted_folder)
        print("Process completed successfully!")

    except ValueError:
        print("Invalid input. Please use numbers to select options.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
