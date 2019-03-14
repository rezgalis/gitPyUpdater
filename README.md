# gitPyUpdater
The intention is to provide a generic script, which, based on local configs, can apply automatic updates to local repos based on remote (e.g. a GitHub) on a headless Linux machine.

Use case is simple - if you have na SBC running Linux in remote location and you need to add some updates to running scripts, you can leverage this script to automatically update remote machine once you push the changes to the relevant git repo online.

//TODO: describe parameters that script can accept:
* using --dry-run that tests configs
* using --add (and params that are needed)
* using without params to run
//TODO
* logs (only latest ones)
* add new config (for each script/repo need to have separate config)
* post-update param in config
* using gitignore in your repos to exclude files to update locally (e.g. configs)
* using setting in config to control at what intervals which updates occur
