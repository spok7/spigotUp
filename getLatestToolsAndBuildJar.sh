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
BUILD_NUM_WEB="$(curl -s https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/buildNumber)"
BUILD_LINK="https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar"

LATEST_VERSION="$(curl -s https://launchermeta.mojang.com/mc/game/version_manifest.json | jq '.latest.release')"
LOCAL_VERSION="$(unzip -p "${SERVER_DIR}"/../spigot.jar version.json | jq ".name")"

if [ ! -d "${BT_DIR}" ]
then
    mkdir "${BT_DIR}"
    echo "Created BuildTools Directory"
fi


# if BuildTools.jar exists and local build number is equal to the newest build number
if [ -f "${BT_DIR}"/BuildTools.jar ] && \
   [ -f "${BUILD_NUM_FILE}" ] && \
   [ $(cat "${BUILD_NUM_FILE}") -eq ${BUILD_NUM_WEB} ]
then
    echo "BuildTools already on newest version; skipping update"
else 
    # backup old BuildTools.jar file
    if [ -f "${BT_DIR}"/BuildTools.jar ]
    then
        mv "${BT_DIR}"/BuildTools.jar "${BT_DIR}"/BuildTools.jar.old
        echo "Moved old BuildTools.jar file to BuildTools.jar.old"
    fi

    # download new BuildTools.jar and update local build number
    echo "Downloading BuildTools.jar"
    curl "${BUILD_LINK}" -s -o "${BT_DIR}"/BuildTools.jar || fatal_error "Download failed"
    echo "${BUILD_NUM_WEB}" > "${BUILD_NUM_FILE}"
    echo "Download complete"
fi

# generate server.jar file if it's outdated
if [ ! -f "${SERVER_DIR}"/../spigot.jar ] || ! [ ${LOCAL_VERSION} == ${LATEST_VERSION} ]
then
    echo "Building Spigot (this will take a while)"
    cd "${BT_DIR}"
    java -Xmx2G -jar BuildTools.jar --rev latest --output-dir ServerJARs > /dev/null 2>&1 || fatal_error 'Build failed'
    cd "${SERVER_DIR}"
    echo 'Build complete'
    new_build_path="$(ls -td "${BT_DIR}"/ServerJARs/spigot* | head -1)"
    cp "${new_build_path}" "$SERVER_DIR"/../spigot.jar
    echo "Server Copied"
else
    echo "Spigot already on newest version; skipping update"
fi

echo "Done"
