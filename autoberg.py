from colorama import just_fix_windows_console
from termcolor import colored
import subprocess
import platform
import shutil
import sys
import os
import re


# Check your system :3
sys_type = platform.machine()
if sys.platform.startswith("win"):
    # Interface Generation :)
    interfaces_file = "wintools\\generate_interfaces_file.exe"
    # What we're looking for :)
    file_search = ["steam_api.dll", 
                   "steam_api64.dll"]
    # Things are here!
    toolsdir = "wintools\\"

elif sys.platform.startswith("linux"):
    interfaces_file = "lintools/find_interfaces.sh"
    file_search = ["libsteam_api.so"]
    # You're on x64!
    if sys_type.endswith("64"):
        toolsdir = "lintools/x86_64/"
    # You're on x86!
    else:
        toolsdir = "lintools/x86/"

else:
    print("Unsupported OS, Sorry! :(")
    sys.exit(1)

# Find our files :3
def find_file(file_search, dir_path):
    found_file = []
    print("Finding files in: {}".format(colored(os.path.basename(dir_path), "yellow")))
    # Search through subdirectories
    for root, dir, files in os.walk(dir_path):
        for file_name in file_search:
            if file_name in files:
                print("Found {}!".format(colored(os.path.basename(file_name), "green")))
                # If we found our files :)
                found_file.append(os.path.join(root, file_name))
    # If we didn't find our files :(
    if len(found_file) == 0:
        print("{}: Files don't exist :(".format(colored("Oopsies", "yellow")))
        sys.exit(1)

    # Return list
    return found_file

# Rename original files and copy Mr Berg's Emu :)
def CopyEmu(files, file_search, toolsdir):
    try:
        # Rename original files
        for original_filename_path in files:
            # Original filename
            old_name = os.path.basename(original_filename_path)
            path = original_filename_path.replace(old_name, "")
            for file_name in file_search:
                # New filename
                new_name = file_name + ".original"
                if file_name == old_name:
                    # Rename original file
                    print("Renaming original {} to {}".format(colored(old_name, "red"), colored(new_name, "green")))
                    os.rename(os.path.join(path, old_name), 
                              os.path.join(path, new_name))
                    # Copy Emu
                    print("Copying Mr Berg's emu to {}".format(colored(path, "yellow")))
                    shutil.copyfile(toolsdir + file_name, path + file_name)
    except Exception as e:
        print(f"Error in Copying Emu: {e}")

# Generate Interfaces
def InterfaceGen(files, interfaces_file):
    try:
        for filename in files:
            path = filename.replace(os.path.basename(filename), "")
            print("Generating interfaces from {}".format(colored(os.path.basename(filename), "green")))
            # Not fully tested this on linux ごめんね~~ :(
            if sys.platform.startswith("linux"):
                subprocess.call([interfaces_file, "\"" + filename + ".original\" > steam_interfaces.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                subprocess.call([interfaces_file, filename + ".original"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Copying interfaces to {}".format(colored(path, "green")))
            shutil.move("steam_interfaces.txt", path)
    except Exception as e:
        print(f"Error in InterfaceGen: {e}")

# steam_appid.txt file
def AppId(dir_path):
    appid_file = open("steam_appid.txt", "w")
    print("\nPaste in the appid of game by {} link or the {} :)".format(colored("store.steampowered.com", "yellow"), colored("appid", "yellow")))
    try:
        while True:
            input_appid = input("\t> ")
            if re.match(r'^\d+$', re.sub(r"\s+", "", input_appid)):
                appid_file.write(input_appid)
                appid_file.close()
                print("Wrote to steam_appid.txt with appid of: {}".format(colored(input_appid, "yellow")))
                break
            elif re.match(r'.*\w+\.\w+\.com.*', input_appid):
                appid = re.search(r'/app/(\d+)/', input_appid)
                appid_file.write(appid.group(1))
                appid_file.close()
                print("Wrote to steam_appid.txt with appid of: {}".format(colored(appid.group(1), "yellow")))
                break
            else:
                print("psst~ Hi~ paste in the link to the store page or the appid ;P")
        print("Copying steam_appid.txt to {}".format(colored(dir_path, "green")))
        shutil.move("steam_appid.txt", dir_path)
    except Exception as e:
        print(f"Error in AppId creation: {e}")


def main():
    # Colors!
    just_fix_windows_console()
    print(colored("Hiya! made by Toapyy!\n", "magenta"), 
          colored("autoberg v1.0!\n", "cyan"))
    try:
        if len(sys.argv) < 2:
            print("{}: Invalid usage :(".format(colored("Oopsies", "yellow")))
            print("Usage: autoberg <folder>\n")
            dir_path = input("Input filepath (double quotes if there's spaces! \"C:\\Users\\User 1\\Folder\"):")
        else:
            dir_path = sys.argv[1]

        # Find files
        files = find_file(file_search, dir_path)
        # Copy Emu
        CopyEmu(files, file_search, toolsdir)
        # Generate Interfaces
        InterfaceGen(files, interfaces_file)
        # Make steam_appid.txt
        AppId(dir_path)

        print("\nEverything done! Have Fun!")
    except Exception as e:
        print(f"Error occured in main: {e}")


if __name__ == '__main__':
    main()