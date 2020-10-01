#!/bin/bash
#
# Downloads newest BuiltTools and builds the latest jar file
# Creates a backup of the last BuildTools and jar file

# handle fatal errors
function fatal_error {
    echo "$1" >&2
    return 1
}

SERVER_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"  # path to the server, see http://stackoverflow.com/a/246128
BT_DIR="${SERVER_DIR}/BuildTools"                               # path to BuildTools folder
BUILD_NUM_FILE="${BT_DIR}/.buildToolsNumber"                    # path to the build number file
SPIGOT_VER_FILE="${BT_DIR}/.spigotVerNumber"                    # path to the spigot version file
BUILD_NUM_WEB="$(curl -s https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/buildNumber)"

BUILD_LINK="https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar"

if [ ! -d "${BT_DIR}" ]
then
    mkdir "${BT_DIR}"
    echo "Created BuildTools Directory"
fi

# if local build number is equal to the newest build number and BuildTools.jar exists
if [ -f "${BUILD_NUM_FILE}" ] && \
   [ $(cat "${BUILD_NUM_FILE}") -eq $BUILD_NUM_WEB ] && \
   [ -f "${BT_DIR/BuildTools.jar}" ]
then
    echo "No BuildTools upgrade was made"
else 
    echo "Generating new BuildTools.jar file"

    # backup old BuildTools.jar file
    if [ -f "${BT_DIR/BuildTools.jar}" ]
    then
        mv "${BT_DIR/BuildTools.jar} ${BT_DIR/BuildTools.jar.old}"
        echo "Moved old BuildTools.jar file to BuildTools.jar.old"
    fi

    # download new BuildTools.jar and update local build number
    echo "Downloading BuildTools.jar"
    curl "${BUILD_LINK}" -o "${BT_DIR}/BuildTools.jar" || fatal_error "Download failed"
    echo "Download complete"
fi

return

# Run BuildTools
echo 'Building Spigot (this will take a while)'
java -Xmx2G -jar BuildTools.jar > /dev/null 2>&1 || fatal_error 'Build failed'
echo 'Build complete'
