# gitPyUpdater
The intention is to provide a generic script, which, based on local configs, can apply automatic updates to local repos based on remote (e.g. a GitHub) on a headless Linux machine.

Use case is simple - if you have na SBC running Linux in remote location and you need to add some updates to running scripts, you can leverage this script to automatically update remote machine once you push the changes to the relevant git repo online.

Sample config file: https://github.com/rezgalis/gitPyUpdater/blob/dev/repo-to-update.properties

Currently script can do the following:
* within local gitPyUpdate directory keeps latest log for each repo it has run update for (<<CONFIG_FILE_NAME>>.lastlog)
* in latest log file keeps timestamp of last checking of remote git repo (next check depends on config setting)
* can run any post-update command - see "post_update"  param in config
* uses " .gitignore" file to skip files that should not be copied locally


## How to set it up
1. Clone this repository locally
2. Create a crontab entry to call this script (every 5minutes, every hour or daily - up to you)
3. Create " .properties" file for any git repos you need to update
4. ***Please note that script you define as "post_update" variable in ".properties" file will always be executed when changes between remote and local repo are found***
