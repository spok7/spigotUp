import argparse
from pathlib import Path

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
