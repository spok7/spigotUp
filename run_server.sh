#!/bin/bash
######## EDIT SERVER CONSTANTS HERE ########
min_mem="3G"
max_mem="6G"
save_backup="true"
prune_backups="true"
############################################

# navigate to the server folder
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."

# create a backup and prune the folder if necessary
if [ "${save_backup}" == "true" ]
then
    python3 spigotUp/backup.py -w
    if [ "${prune_backups}" == "true" ]
    then
        python3 spigotUp/prune_backups.py
    fi
fi

# create the eula if necessary
if [ ! -f eula.txt ]
then
    echo "eula=true" > eula.txt
fi

# run the server
java -server -Xms"${min_mem}" -Xmx"${max_mem}" -XX:+UseConcMarkSweepGC -jar spigot*.jar nogui


# give user chance to quit before restarting

echo "The server is going to restart in 5 seconds!"
echo "--- Press Ctrl + C to cancel. ---"

for i in 5 4 3 2 1
do
	echo "  Restarting in $i..."
	sleep 1
done

echo "--- The Server is Restarting! --- "
exec spigotUp/run_server.sh
