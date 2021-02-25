# Google Drive File Stream finally works with WSL 2 ?

Steps:
* make sure you have wsl 2 (`wsl -l -v`). If you have version 1 you need to upgrade (GIYF)
* make sure you have version **3301** of dokanccXXXX.dll in your Google Drive installation directory.
* make sure you have python3 installed
* run `python idadif.py dokancc3301.dll dokancc3301.dif`
    * change the path to the dll as appropriate for your case
* restart

Do this at your own risk: the patch is offered "as is", without any warranty. If Google Drive decides to delete all your files and call you names, that is on you, not me.

## What is this magic?
The library on which the Google Drive Filesystem is based (dokany) had a "bug" where it returned *STATUS_NOT_IMPLEMENTED*  (0xc0000002) where it should have been *STATUS_NOT_SUPPORTED* (0xc00000bb).
* See here for the reasons: https://github.com/dokan-dev/dokany/pull/933

Unfortunately Google did not port this fix into their software and we do not have their latest source code. Good news is: after a little bit of digging with Ghidra I was able to make a patch that works for me, just one byte needs to be changed

## Whay problem does it solve?
Without this patch, it was not possible to enumerate the files in google drive (while it was possible to read or write a specific file). E.g. the command
`ls /mnt/g/`
prints
`ls: reading directory: Function not implemented`
as shown in this issue: https://github.com/microsoft/WSL/issues/2999

With the patch many commands work correctly, including ls and tar.

## Known issues with this solution:
* git misbehaves under WSL
