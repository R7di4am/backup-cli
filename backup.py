import os
import zipfile
import re
#                                          @R7di4am                                     #
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def get_backup_folder():
    folder = os.path.expanduser("~/backups")
    os.makedirs(folder, exist_ok=True)
    
    if not os.access(folder, os.W_OK):
        print("❌ No write permission for backups folder!")
        return None
    
    return folder

def get_backup_name(action):
    zip_name = input(f"💾 Enter backup name (without .zip) to {action}: ").strip()
    return re.sub(r'[^a-zA-Z0-9_-]', '', zip_name) + ".zip"

def list_backups():
    backup_folder = get_backup_folder()
    if not backup_folder:
        return False

    files = [f for f in os.listdir(backup_folder) if f.endswith(".zip")]
    if files:
        print("\n📂 Available Backups:")
        for f in files:
            print(f" - {f}")
        return True
    
    print("❌ No backups found.")
    return False

def build_zip(folder_path, zip_name):
    backup_folder = get_backup_folder()
    if not backup_folder:
        return

    zip_path = os.path.join(backup_folder, zip_name)
    folder_path, zip_path = map(os.path.abspath, [folder_path, zip_path])
    
    if os.path.commonpath([folder_path]) == os.path.commonpath([folder_path, zip_path]):
        print("❌ Cannot store the ZIP inside the same folder!")
        return
    
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file == zip_name:
                    continue
                file_path = os.path.join(root, file)
                print(f"📦 Adding: {file_path}")
                zipf.write(file_path, os.path.relpath(file_path, folder_path))
    
    print(f"✅ Backup created: {zip_path}")

def extract_zip(zip_name):
    backup_folder = get_backup_folder()
    if not backup_folder:
        return

    zip_path = os.path.join(backup_folder, zip_name)
    extract_path = zip_path.replace(".zip", "")
    
    if os.path.exists(zip_path):
        os.makedirs(extract_path, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as zipf:
            zipf.extractall(extract_path)
            print(f"✅ Extracted to: {extract_path}")
    else:
        print(f"❌ Backup not found: {zip_path}")

def delete_zip(zip_name):
    backup_folder = get_backup_folder()
    if not backup_folder:
        return

    backup_path = os.path.join(backup_folder, zip_name)
    if os.path.exists(backup_path):
        try:
            os.remove(backup_path)
            print(f"🗑️ Deleted: {zip_name}")
        except Exception as e:
            print(f"❌ Error deleting {zip_name}: {e}")
    else:
        print(f"❌ Backup not found: {backup_path}")

def main_menu():
    print("\n🚀 Welcome To Backup Script")
    while True:
        print("\n1 => Create Backup")
        print("2 => Extract Backup")
        print("3 => List Backups")
        print("4 => Delete Backup")
        print("5 => Exit")
        
        command = input("👉 Choose an option: ").strip()
        clear_screen()
        
        if command == "1":
            folder_path = input("📂 Enter folder path: ").strip()
            if os.path.exists(folder_path) and os.path.isdir(folder_path) and os.access(folder_path, os.R_OK):
                build_zip(folder_path, get_backup_name("create"))
            else:
                print("❌ Invalid or unreadable folder path.")
        elif command == "2" and list_backups():
            extract_zip(get_backup_name("extract"))
        elif command == "3":
            list_backups()
        elif command == "4" and list_backups():
            delete_zip(get_backup_name("delete"))
        elif command == "5":
            print("👋 Exiting... Bye!")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main_menu()

#                                          @R7di4am                                     #
