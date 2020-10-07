import argparse
from pathlib import Path

if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", help="specifies the target directory from which to prune backups",
                        action='store', dest="target")
    
    args = parser.parse_args()
    
    # 
    backups = Path("backups")
    backups.mkdir(exist_ok=True)