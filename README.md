# spigotUp - Spigot Deployment, Update, and Management Tool

This is a collection of shell scripts allowing the automatic set up, update, and management of a Spigot server on a Linux device.
The update script automatically fetches the newest BuildTools.jar and builds the newest Spigot version, the run script runs the server continuously and restarts after crashes, and the tmux script allows you to run the server in a tmux session.

Setting up a Spigot server for the first time can be a daunting challenge, especially for beginners. These scripts aim to get a Spigot server running with minimal effort.

While these scripts do guarantee that your server will always be running the newest version of minecraft, they do not guarantee that it will be stable. These scripts can fail if the build tools and server jar are inherently unstable, so use at your own risk!


## Required Programs

- [git](https://git-scm.com/downloads)
- [tmux](https://www.howtogeek.com/671422/how-to-use-tmux-on-linux-and-why-its-better-than-screen/)
- [crontab](https://www.tutorialspoint.com/unix_commands/crontab.htm) (optional)
- [java 8 or above](https://java.com/en/download/)
- [jq](https://stedolan.github.io/jq/manual/)
- [bash](https://linux.die.net/man/1/bash)
- [python3.6 or higher](https://www.python.org/downloads/)

This guide does not assume the user has any knowledge of the programs above, but knowledge prior of git, tmux, and crontab is recommended.

## Installation

Navigate to your server folder in your terminal and type the following command:
```bash
git clone https://github.com/spok7/spigotUp.git
```
You should now have a new spigotUp folder in your server folder.

## Usage

### Generating a new spigot.jar file

Navigate to the new spigotUp folder and run the update\_server.sh script. This should generate a BuildTools folder, and then later, a spigot.jar file in your server folder. The script will only generate a new spigot.jar if it detects that there has been a new minecraft update since the previous run. If you want to recompile the jar, simply delete the current spigot.jar file in your server folder and run the script again. The same applies for the BuildTools.jar file.

```bash
cd spigotUp
bash update_server.sh
```
### Running the server

Once you have a spigot.jar file in your server folder, run the run\_server.sh script to start the server. You can change the minimum and maximum amounts of memory dedicated to the server, and whether or not to create backups before starting by changing the variables at the top of the file. By default, the server will back up worlds to spigotUp/backups before starting, and the server will start with a minimum of 3G and a maximum of 6G of dedicated RAM. The server is started configured as a java server with a memory cleaner, and with the outdated version message disabled. When running this file, the server will start in the current terminal, and stop when the terminal closes.

```bash
bash run_server.sh
```

### Running the server in the background

If you don't want a tab always open on your computer or only have ssh access to your machine, you are best off running it in an app such as screen or tmux. Tmux is used in this instance for no reason at all. Once you run tmux_server.sh, the server will run in the background. To check up on the server, type `tmux a` into any console to attatch to the tmux session, and press Ctrl+B, D to disconnect. Please read up on tmux on your own beforehand. It is a really neat tool, and running spigot servers easily is only one of its many features.

```bash
bash tmux_server.sh
```

While it is entirely possible to install the server as a service, doing so is not recommended due complications in maintainance.

## Automation

The real purpose of these scripts is to make a sysadmin's life easier. Here is how one may go about a crontab for this server.

```crontab
# m h  dom mon dow   command
@reboot              ~/myserver/spigotUp/tmux_server.sh
00  04   *   *   *   ~/myserver/spigotUp/update_server.sh
15  04   *   *   *   tmux send-keys -t mcserver "stop" C-m
```

The first line guarantees the server starts whenever the computer starts. The second checks for updates at 4am. The third reloads the server at 4:15 to apply any necessary updates. Type `crontab -e` to edit your own crontab. The instructions should be included within, but again, please read up on it on your own.


## Backups

### Creating and Restoring Backups

The backups.py script is able to create and restore backups of server files in a zip format to and from the spigotUp/backups folder. The backups script does not back up jar files with the w, s, or all tags for space saving purposes, since update_server.sh does that already.

Here is the help text:
```
usage: backup.py [-h] [-r [TIME]] (-f FILES [FILES ...] | -w | -s | -all) [-t TARGET]

optional arguments:

  -h, --help            show this help message and exit

  -r [TIME]             sets the script to restore files from a specific time;
                        if -f is used, the time variable is not needed;
                        TIME format: YYYY-MM-DD-hhmm;
                        Valid TIME examples: 2020, 2020-09,       
                        2020-09-14, 2020-09-14-12, 2020-09-14-1253

  -f FILES [FILES ...]  selects a list of files to back up / 
  
  -w                    selects all worlds to back up / 
  
  -s                    selects to back up / restore server settings and
                        plugin settings;
                        when in restore mode, restores all
                        non-world files in backups folder at the given time

  -all                  selects all worlds and settings for back up / restore;
                        when in restore mode, restores
                        all the files in backups folder at the given time

  -t TARGET             specifies the target directory from
                        which to save / restore backups

  -wc WORLD_CONTAINER   speficies where to backup worlds from; default is
                        the server folder
```

Here are some example use cases:

```bash
# create backups for a few specific files
python3 backups.py -f file1 file2

# save a backup at a different location
python3 backups.py -f file1 -t ~/mybackupsfolder

# save all worlds files
# this runs in the run_server.sh file before starting the server
python3 backups.py -w

# same as above, but saves from another worlds directory
python3 backups.py -w -wc ../worlds

# save all settings files
# this runs in the update_server.sh file after fetching a new server version
python3 backups.py -s

# save all server files without server jars
# this is handy when updating the server manually
python3 backups.py -a

# restore a specific file
python3 backups.py -r -f file.zip

# restore multiple files
python3 backups.py -r -f file1.zip file2.zip file3.zip

# restore the last worlds backed up in December 2019
python3 backups.py -r 2019-12 -w

# same as above, but from a different folder
python3 backups.py -r 2019-12 -w -t "~/aDifferentFolder"

# restore all server settings from a backup made at 1:23pm on January 5th, 1970
# note that 24 hour time is used
python3 backups.py -r 1970-01-05-1323 -a
```


### Pruning Backups

The prune_backups.py script deletes all backups except all made within 24 hours of the last backup, 4 weekly backups from the last backup, 12 monthly backups from the last backup, and all yearly backups.

Assuming the script is given a folder with backups made twice a day over the past three years, the output directory would look like this:

```
file-2020-12-31-1800.zip
file-2020-12-31-0600.zip
file-2020-12-30-1800.zip
file-2020-12-29-1800.zip
file-2020-12-28-1800.zip
file-2020-12-27-1800.zip
file-2020-12-26-1800.zip
file-2020-12-25-1800.zip
file-2020-12-24-1800.zip
file-2020-11-24-1800.zip
file-2020-10-24-1800.zip
file-2020-09-24-1800.zip
file-2020-08-24-1800.zip
file-2020-07-24-1800.zip
file-2020-06-24-1800.zip
file-2020-05-24-1800.zip
file-2020-04-24-1800.zip
file-2020-03-24-1800.zip
file-2020-02-24-1800.zip
file-2020-01-24-1800.zip
file-2019-01-24-1800.zip
file-2018-01-24-1800.zip
```

Here is the help text:
```
usage: prune_backup.py [-h] [-t TARGET]

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET             specifies the target directory to prune;
                        spigotUp/backups by defualt
```