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

Once you have a spigot.jar file in your server folder, run the run\_server.sh script to start the server. Change the minimum and maximum amounts of memory dedicated to the server by changing the variables at the top of the file. The server is started configured as a java server with a memory cleaner, and with the outdated version message disabled. When running this file, the server will start in the current terminal, and stop when the terminal closes.

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
