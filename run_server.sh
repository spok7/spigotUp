#!/bin/bash

remove_redundants() {
    files=$(ls -la ~/spigot/backups | egrep -o $1.*)
    last_file=""
    for line in $files
    do
        parsed_line=$(echo $line | egrep -o $1........)
        parsed_prev=$(echo $last_file | egrep -o $1........)
        if [ "$parsed_line" == "$parsed_prev" ]
        then
           rm -rf "backups/$last_file"
        fi
        last_file=$line
    done
}

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."
#trap "cd spigotUp; return" SIGINT
#WORLD_NAME=$(cat server.properties | egrep "level-name=.*")
#WORLD_NAME=${WORLD_NAME:11}


java -server -Xms3G -Xmx6G -XX:+UseConcMarkSweepGC -jar -Dcom.mojang.eula.agree=true -DIReallyKnowWhatIAmDoingISwear spigot*.jar nogui
#remove_redundants $WORLD_NAME
#cp -r ${WORLD_NAME} backups/${WORLD_NAME}-$(date +%F)

echo "The server is going to restart in 5 seconds!"
echo "--- Press Ctrl + C to cancel. ---"

for i in 5 4 3 2 1
do
	echo "  Restarting in $i..."
	sleep 1
done

echo "--- The Server is Restarting! --- "
exec spigotUp/run_server.sh
