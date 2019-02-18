# gitPyUpdater
The intention is to provide a set of generic scripts, which, based on local config, can do automtic updates to e.g. a GitHub repo that has been cloned to a headless Linux machine.

Use case is simple - if you have na SBC running Linux in remote location and you need to add some updates to running scripts, you can leverage the included scripts that would automatically update remote machine once you push the changes to the relevant git repo.
Please see the included example configuration file that you need to include along with these scripts.


Needless to say that any credentials or specific details should exist as separate config file on the remote machine and such details should not be a part of git repo.
