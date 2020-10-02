#!/bin/bash
#
# Downloads newest BuiltTools and builds the latest jar file
# Creates a backup of the last BuildTools and jar file


# handle fatal errors
function fatal_error {
    echo "$1" >&2
    return 1
}


# path to current folder and BuildTools folder
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
bt_dir="${script_dir}/BuildTools"

# latest and local BuildTool.jar build numbers
build_num_file="${bt_dir}/.buildToolsNumber"
build_num_link="$(curl -s https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/buildNumber)"

# link to newest BuildTools.jar
bt_link="https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar"

# latest and local minecraft versions
latest_ver="$(curl -s https://launchermeta.mojang.com/mc/game/version_manifest.json | jq '.latest.release')"
local_ver="$(unzip -p "${script_dir}"/../spigot.jar version.json | jq ".name")"



# create BuildTools directory if it does not exist
if [ ! -d "${bt_dir}" ]
then
    mkdir "${bt_dir}"
    echo "Created BuildTools Directory"
fi


# if BuildTools.jar exists and local build number is equal to the newest build number
if [ -f "${bt_dir}"/BuildTools.jar ] && \
   [ -f "${build_num_file}" ] && \
   [ $(cat "${build_num_file}") -eq ${build_num_link} ]
then
    echo "BuildTools already on newest version; skipping update"
else 
    # backup old BuildTools.jar file
    if [ -f "${bt_dir}"/BuildTools.jar ]
    then
        mv "${bt_dir}"/BuildTools.jar "${bt_dir}"/BuildTools.jar.old
        echo "Moved old BuildTools.jar file to BuildTools.jar.old"
    fi

    # download new BuildTools.jar and update local build number
    echo "Downloading BuildTools.jar"
    curl "${bt_link}" -s -o "${bt_dir}"/BuildTools.jar || fatal_error "Download failed"
    echo "${build_num_link}" > "${build_num_file}"
    chmod a+x "${bt_dir}"/BuildTools.jar
    echo "Download complete"
fi

# generate server.jar file if it's outdated
if [ ! -f "${script_dir}"/../spigot.jar ] || ! [ ${local_ver} == ${latest_ver} ]
then
    echo "Building Spigot (this will take a while)"
    cd "${bt_dir}"
    java -Xmx2G -jar BuildTools.jar --rev latest --output-dir ServerJARs > /dev/null 2>&1 || fatal_error 'Build failed'
    chmod a+x ServerJARs/*
    cd "${script_dir}"
    echo 'Build complete'
    new_build_path="$(ls -td "${bt_dir}"/ServerJARs/spigot* | head -1)"
    cp "${new_build_path}" "$script_dir"/..
    echo "Server Copied"
else
    echo "Spigot already on newest version; skipping update"
fi

echo "Done"
