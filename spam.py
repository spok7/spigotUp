import argparse
from pathlib import Path
from datetime import datetime, timedelta

if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", help="specifies the target directory from which to prune backups",
                        action='store', dest="target")
    args = parser.parse_args()
    
    # select backups folder appropriately
    # default location of backups folder in same dir as script
    backups = Path(__file__).resolve().parent / "backups"
    if args.target:
        backups = Path(args.target)
    
    # throw error if restoring from invalid target
    if not backups.is_dir():
        raise FileNotFoundError("ERROR: Target backups directory does not exist")

    dom = ["01", "01", "03", "04", "05", "06", "07", "08", "09"]
    dom.extend([str(i) for i in range(10, 31)])
    for year in range(2000, 2010):
        for month in ["01", "01", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
            for day in dom:
                new_path = backups / f"test-{year}-{month}-{day}-1234.zip"
                new_path.touch()