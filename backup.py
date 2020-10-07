import argparse
from pathlib import Path
import zipfile
from datetime import datetime
import re


def is_valid_path(path: str) -> Path:
    """
    Returns a Path object if a file or directory exists at the specified path.
    Raises exception otherwise.
    """
    path = Path(path).resolve()
    if not path.exists():
        raise FileNotFoundError(path, "is not a valid file or directory")
    return path


def timestamp_zip(string: str) -> str:
    """
    Adds the current date and a .zip ending to the given string.
    Example:
    > timestamp("foo")
    "foo-1997-09-14-1253.zip"
    """
    timestamp = datetime.today().strftime("%Y-%m-%d-%H%M")
    return f"{string}-{timestamp}.zip"

def backup_file(path: Path, save_dir: Path) -> None:
    """
    Given the path to a file or directory, creates a zip backup to the given location.
    """
    archive = zipfile.ZipFile(save_dir, "w", zipfile.ZIP_DEFLATED)
    restore_path = str(path.parent.absolute())
    archive.writestr("restore_path.txt", restore_path)

    # handle files and directories; strip paths of files from names
    if path.is_file():
        archive.write(path, str(path)[len(restore_path):])
    else:
        for p in path.rglob("*"):
            archive.write(p, str(p)[len(restore_path):])

    archive.close()

def backup_files(paths: list, save_dir: Path) -> None:
    """
    Given the list of file paths, creates zip backups to the given location.
    """
    for f in paths:
        save_path = save_dir / timestamp_zip(f.name)
        backup_file(f, save_path)

def get_world_paths() -> list:
    """
    Returns a list of paths to the worlds on the server.
    """
    server_dir = Path(__file__).resolve().parents[1]
    world_paths = []
    for p in server_dir.iterdir():
        if p.is_dir and (p / "level.dat").is_file():
            world_paths.append(p.absolute())
    return world_paths

def get_setting_paths() -> list:
    """
    Returns a list of paths to the server setting and plugin settings.
    """
    settings_paths = []

    server_dir = Path(__file__).resolve().parents[1]
    for p in server_dir.iterdir():
        if p.is_file() and p.suffix != ".jar":
            settings_paths.append(p.absolute())
    
    plugin_dir = server_dir / "plugins"
    if plugin_dir.is_dir():
        for p in plugin_dir.iterdir():
            if p.is_dir and (p / "config.yml").is_file():
                settings_paths.append(p.absolute())

    return settings_paths


def restore_file(path: Path) -> None:
    """
    Restores the file at the given path to its original location based on restore_path.txt.
    """
    archive = zipfile.ZipFile(path, "r", zipfile.ZIP_DEFLATED)
    restore_path = str(archive.read("restore_path.txt"))[2:-1]
    for p in archive.namelist():
        if p != "restore_path.txt":
            archive.extract(p, restore_path)
    archive.close()

def restore_files(paths: list) -> None:
    """
    Restores the files at the given paths to their original locations based on restore_path.txt.
    """
    if not paths:
        print("No files selected. Are you sure there are files at the given time?")
    for p in paths:
        restore_file(p)

def is_valid_date(string: str) -> bool:
    """
    Returns whether the date is valid or not.
    """
    return re.compile(r"^(\d{4}|\d{4}-\d{2}|\d{4}-\d{2}-\d{2}|\d{4}-\d{2}-\d{2}-\d{2}|\d{4}-\d{2}-\d{2}-\d{4})$").match(string)

def filter_by_date(date: str, save_dir: Path) -> list:
    """
    Returns list of paths that match the given date range, only including the latest entries per file.
    """
    # remove ambiguity between year and time; I assure you, dear reader, this was the lesser evil
    if len(date) == 4:
        date += "-"
    
    # iterate through all files which match the date requirement
    # since alphabetical happens to be chronological at this point, grab the last backup from each file
    filtered_paths = []
    last = None
    for curr in [p for p in save_dir.glob("*") if date in str(p.stem)[-15:]]:
        if last and str(last.stem)[:-15] != str(curr.stem)[:-15]:
            filtered_paths.append(last)
        last = curr
    if last:
        filtered_paths.append(last)

    return filtered_paths

def find_world_zips(paths: list) -> list:
    """
    Returns input list with only world zips
    """
    world_zips = []
    world_checker = re.compile(r"^[^\/]+/level.dat$")
    for p in paths:
        archive = zipfile.ZipFile(p, "r", zipfile.ZIP_DEFLATED)
        for z in archive.namelist():
            if world_checker.match(z):
                world_zips.append(p)
                break
        archive.close()
    return world_zips

def find_setting_zips(paths: list) -> list:
    """
    Returns input list with only setting zips
    """
    return list(set(paths) - set(find_world_zips(paths)))


if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser()

    # if '-r' is passed, script restores instead of backs up
    parser.add_argument("-r", help="sets the script to restore files from a specific time; if -f is used, the time variable is not needed; "+\
                        "TIME format: YYYY-MM-DD-hhmm; "+\
                        "Valid TIME examples: 2020, 2020-09, 2020-09-14, 2020-09-14-12, 2020-09-14-1253",
                        action='store', dest="restore", metavar="TIME", nargs="?", const="file")

    # backs up files (-f), worlds (-w), settings (-s), or all worlds and settings (-a)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", help="selects a list of files to back up / restore",
                        action="extend", dest="files", nargs="+", type=is_valid_path)
    group.add_argument("-w", help="selects all worlds to back up / restore",
                        action="store_true", dest="worlds")
    group.add_argument("-s", help="selects to back up / restore server settings and plugin settings; "+\
                        "when in restore mode, restores all non-world files in backups folder at the given time",
                        action="store_true", dest="settings")
    group.add_argument("-all", help="selects all worlds and settings for back up / restore; "+\
                        "when in restore mode, restores all the files in backups folder at the given time",
                        action="store_true")

    # specifies an optional backups folder outside of the default /backups
    parser.add_argument("-t", help="specifies the target directory from which to save / restore backups",
                        action="store", dest="target")
    
    args = parser.parse_args()
    

    # select backups folder appropriately
    # default location of backups folder in same dir as script
    backups = Path(__file__).resolve().parent / "backups"
    if args.target:
        tpath = Path(args.target)
        # throw error if restoring from invalid target
        if args.restore and not args.files and not tpath.is_dir():
            raise FileNotFoundError("ERROR: Target backups directory does not exist")
        # update the backups folder location
        backups = tpath
    # when backing up, make dir if it doesn't exist
    backups.mkdir(exist_ok=True)


    # backup files
    if not args.restore:

        target_paths = []

        if args.files:
            print("Backing up Files")
            target_paths = args.files

        elif args.worlds:
            print("Backing up Worlds")
            target_paths = get_world_paths()

        elif args.settings:
            print("Backing up Settings")
            target_paths = get_setting_paths()

        else:
            print("Backing up Worlds and Settings")
            target_paths = get_world_paths() + get_setting_paths()

        backup_files(target_paths, backups)
        print("Backup Completed")

    # restore files
    else:

        target_paths = []

        if args.files:
            print("Restoring Files")
            target_paths = args.files

        # make sure restore time is specified by this point
        elif not is_valid_date(args.restore):
            raise ValueError("Please specify restore time in the format YYYY-MM-DD-hhmm")

        else:

            filtered_paths = filter_by_date(args.restore, backups)

            if args.worlds:
                print("Restoring Worlds")
                target_paths = find_world_zips(filtered_paths)

            elif args.settings:
                print("Restoring Settings")
                target_paths = find_setting_zips(filtered_paths)

            else:
                print("Restoring All")
                target_paths = filtered_paths

        restore_files(target_paths)
        print("Restore Completed")