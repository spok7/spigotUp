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
    
    paths = reversed(sorted([p for p in backups.iterdir()]))
    paths_to_remove = []
    removed_something = False
    
    ref_date = None
    last_path = None
    
    i = 1
    delta_max = [timedelta(0), timedelta(1), timedelta(7), timedelta(30), timedelta(365), timedelta.max]
    delta_min = delta_max[i]

    for curr_path in paths:

        # if the backups is of the same file
        if last_path and str(last_path.stem)[:-15] == str(curr_path.stem)[:-15]:

            dlst = str(curr_path.stem)[-15:].split("-")
            cur_date = datetime(int(dlst[0]), int(dlst[1]), int(dlst[2]), int(dlst[3][:2]), int(dlst[3][2:]))

            timediff = ref_date - cur_date

            # if greater than current max, move to next max
            while timediff > delta_max[i]:
                delta_min = delta_max[i]
                i += 1
                if removed_something:
                    paths_to_remove.pop(-1)
                    removed_something = False

            # if greater than next step to max, add back the last removed item
            while timediff > delta_min + delta_max[i - 1]:
                delta_min += delta_max[i - 1]
                if removed_something:
                    paths_to_remove.pop(-1)
                    removed_something = False

            # remove other paths greater than the minimum
            if timediff > delta_min:
                paths_to_remove.append(curr_path)
                removed_something = True
        
        else:
            removed_something = False
            dlst = str(curr_path.stem)[-15:].split("-")
            ref_date = datetime(int(dlst[0]), int(dlst[1]), int(dlst[2]), int(dlst[3][:2]), int(dlst[3][2:]))
            i = 1

        last_path = curr_path
    
    if removed_something:
        paths_to_remove.pop(-1)

    for p in paths_to_remove:
        p.unlink()