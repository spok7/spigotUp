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

    dom = ["01", "02", "03", "04", "05", "06", "07", "08", "09"]
    dom.extend([str(i) for i in range(10, 25)])
    months = ["01", "01", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    months = ["01"]
    for year in range(2000, 2003):
        for month in months:
            for day in dom:
                for time in ["0000", "1200"]:
                    new_path = backups / f"test-{year}-{month}-{day}-{time}.zip"
                    new_path.touch()