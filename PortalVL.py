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

def extract_zip(zip_path, target_path, language):
    print("Extracting files from ZIP...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in zip_ref.namelist():
            if 'scenes' in member:
                target_file_path = os.path.join(target_path, language, 'scenes', member.replace(f'{language}/scenes/', ''))
            elif 'scripts' in member:
                target_file_path = os.path.join(target_path, language, 'scripts', member.replace(f'{language}/scripts/', ''))
            elif 'sounds' in member:
                target_file_path = os.path.join(target_path, language, 'sound', member.replace(f'{language}/sounds/', ''))
            else:
                target_file_path = os.path.join(target_path, member)

            if member.endswith('/'):
                os.makedirs(target_file_path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
                with zip_ref.open(member) as source, open(target_file_path, 'wb') as target:
                    shutil.copyfileobj(source, target)
    print("Extraction completed!")

def apply_files_to_source_unpack(source_unpack_path, extracted_folder, language, folder_name):
    print(f"Applying {folder_name} files to Source Unpack...")
    if folder_name == "scenes":
        target_folder = os.path.join(source_unpack_path, "portal", "scenes")
    elif folder_name == "scripts":
        target_folder = os.path.join(source_unpack_path, "portal", "scripts")
    else:
        target_folder = os.path.join(source_unpack_path, folder_name)

    if not os.path.exists(target_folder):
        os.makedirs(target_folder, exist_ok=True)

    source_folder = os.path.join(extracted_folder, language, folder_name)
    for dirpath, dirnames, filenames in os.walk(source_folder):
        relative_dir = os.path.relpath(dirpath, source_folder)
        target_dir = os.path.join(target_folder, relative_dir)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)

        for file in filenames:
            source_file = os.path.join(dirpath, file)
            target_file = os.path.join(target_dir, file)
            try:
                shutil.copy2(source_file, target_file)
                print(f"Applied: {file}")
            except PermissionError:
                print(f"Permission denied for file: {file}. Skipping it.")
            except Exception as e:
                print(f"An error occurred while copying {file}: {e}")

    print(f"{folder_name} files applied successfully!")

def replace_sound_files_in_source_unpack(source_unpack_path, extracted_sound_folder):
    print("Replacing sound files in Source Unpack...")
    sound_folders = ['ambient', 'npc', 'vo/aperture_ai', 'vo/escape']

    for folder in sound_folders:
        source_folder = os.path.join(extracted_sound_folder, folder)
        if os.path.exists(source_folder):
            target_folder = os.path.join(source_unpack_path, "portal/sound", folder)
            if not os.path.exists(target_folder):
                os.makedirs(target_folder, exist_ok=True)
            for file in os.listdir(source_folder):
                source_file = os.path.join(source_folder, file)
                target_file = os.path.join(target_folder, file)
                os.makedirs(os.path.dirname(target_file), exist_ok=True)

                try:
                    shutil.copy2(source_file, target_file)
                    print(f"Applied: {file} to {folder}")
                except PermissionError:
                    print(f"Permission denied for file: {file}. Skipping it.")
                except Exception as e:
                    print(f"An error occurred while copying {file}: {e}")
        else:
            print(f"Warning: {folder} folder not found in extracted ZIP.")
    
    print("Sound file replacement completed!")

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
        "escape_02_ spheredestroy2-00.wav",
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
    print("5. Spanish")
    print("6. ShutUpGLaDOS (Minimal Voice Line Preset by XnonXte)")
    print("7. Exit")

    try:
        choice = int(input("Choose an option (1-7): ").strip())
        if choice == 7:
            print("Exiting the program.")
            return

        language_map = {1: "german", 2: "english", 3: "french", 4: "russian", 5: "spanish"}
        if choice not in language_map and choice != 6:
            print("Invalid option. Please try again.")
            return

        if choice == 6:
            source_unpack_path = input("Enter the path to the Source Unpack folder (before /portal folder): ").strip()
            apply_minimal_voice_lines_preset(source_unpack_path)
            return

        language = language_map[choice]

        zip_url = f"https://0x0.c0de.wtf/portalVL/{language}.zip"
        zip_download_path = f"{language}.zip"
        source_unpack_path = input("Enter the path to the Source Unpack folder (before /portal folder): ").strip()
        extracted_folder = f"extracted_{language}"

        download_zip(zip_url, zip_download_path)
        os.makedirs(extracted_folder, exist_ok=True)
        extract_zip(zip_download_path, extracted_folder, language)

        apply_files_to_source_unpack(source_unpack_path, extracted_folder, language, "scenes")
        apply_files_to_source_unpack(source_unpack_path, extracted_folder, language, "scripts")

        replace_sound_files_in_source_unpack(source_unpack_path, os.path.join(extracted_folder, language, "sound"))

        apply_preset = input("Do you want to apply ShutUpGLaDOS (Minimal Voice Line Preset by XnonXte)? (y/n): ").strip().lower()
        skip = False

        if language == "russian" and apply_preset == 'y':
            proceed = input("WARNING: WILL BREAK, DO YOU WANT TO PROCEED? (y/n): ").strip().lower()
            if proceed != 'y':
                skip = True

        if apply_preset == 'y' and not skip:
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