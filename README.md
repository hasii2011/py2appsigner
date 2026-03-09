[![CircleCI](https://dl.circleci.com/status-badge/img/gh/hasii2011/py2appsigner/tree/master.svg?style=shield)](https://dl.circleci.com/status-badge/redirect/gh/hasii2011/py2appsigner/tree/master)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![PyPI version](https://badge.fury.io/py/py2appsigner.svg)](https://badge.fury.io/py/py2appsigner)

## Rationale

These utilities help me sign Python applications built with [py2app](https://github.com/ronaldoussoren/py2app).  This project is a Python rewrite of the one I implemented using [Bash](https://www.gnu.org/software/bash/manual/bash.html) scripts.  See the [CodeSigningScripts](https://github.com/hasii2011/CodeSigningScripts) repository.  The source article for this code and the shell scripts is still [here](https://hsanchezii.wordpress.com/2021/10/06/code-signing-python-py2app-applications/).  The motivation to do this in Python was that supporting different Python versions necessitated implementing version specific scripts when signing the Python libraries and applications.  I thought that was unsustainable.

The goals for this project are:

- Consistent CLI interface across Python versions 
- Installable in a developer's virtual environment
- Default the signing parameters to environment variables.  This allows for short CLI invocations.  However, still allow CLI parameter overrides
- Use the built-in keychain to store the notarization tool application ID.  This avoid having to either key-in or recall from the bash history a long, long application ID.

Installation
```bash
pip install py2appsigner
```
## Dependencies

This project uses [Click](https://click.palletsprojects.com/) for CLI handling


## Required Environment Variables

The above commands depend on the following environment variables.

```bash
PROJECTS_BASE             -  The local directory where the python projects are based
PROJECT                   -  The name of the project;  It should be a directory name
IDENTITY                  - Your Apple Developer ID 
```

 An example, of a PROJECTS_BASE is:

```bash
export PROJECTS_BASE="${HOME}/PycharmProjects" 
```

This should be set in your shell startup script.  For example `.bash_profile`.

The PROJECT environment variable should be set on a project by project basis.  I recommend you use [direnv](https://direnv.net) to manage 
these.  An example of a .envrc follows:

```bash
export PROJECT=pyutmodel
source pyenv-3.10.6/bin/activate
```

## Python Console Scripts

### Sign the internal zip file

```bash
py2appSign -p 3.11 -d pyut -a Pyut  zipsign
```


### Sign the application

```bash
py2appSign -p 3.11 -d pyut -a Pyut  appsign
```


### Notarize the application

```bash
appNotarize -d pyut -a Pyut --verbose
```


### Staple the application

```bash
appStaple -d pyut -a Pyut --verbose
```


### Verify application signing

```bash
appVerify -d pyut -a Pyut
```

### Utility Scripts

#### Notarization History

```bash
notaryTool history
```

##### Specify a profile name

```bash
notaryTool -p NOTARY_TOOL_APP_ID history
```

Stores the history in the file `notaryHistory.log`.

#### Notary Details

```bash
notaryTool information -i <submission id)
```
`e.g. 5f57fc1e-23d3-42ab-b0ad-ec1d2635c4ad
`

##### Specify a profile name

```bash
notaryTool -p NOTARY_TOOL_APP_ID information -i <submission id>
```
`e.g.  5f57fc1e-23d3-42ab-b0ad-ec1d2635c4ad`

Stores the output in the file `notary-{submission id}.log`



## Weird options added over the years

As Python has rolled versions and I use the application signer for different application several weirdnesses have appeared as py2app builds the binary.   Rather that patching each individual OS X application I added the sub commands in case you encountered these errors that cause the Apple CLI (`/usr/sbin/spctl`) to fail

### The zipsign subcommand has the following option

`--delete-part-files`
This problem surfaced with Python 3.13.  This option removes these bad files that cause `appVerify` to fail.  These are in the internal `python313.zip` file in the `test/zipimport_data` subdirectory.

I only remove the `.part` files and the `zipimport_data` directory.  These leads me to question the existence of `test` subdirectory in the Python zip file with lots of other subdirectories.   I may experiment in the future in entirely removing the `test` subdirectory.  Currently, its size is 7.7 MB.

### The `appsign` subcommand has the followiing options

`--fix-lib`
`--fix-sym-link`

#### --fix-lib

This option retrieves  the following dynamic library from Homebrew.  The one packaged in the .app file is unsignable.

The option copies it into the applicaiton.  Currently, works only on Apple Silicon OS X andwith [Homebrew](https://brew.sh) installed.  You must manally do this on Intel OS X.

See: https://stackoverflow.com/questions/62095338/py2app-fails-macos-signing-on-liblzma-5-dylib

On Intel OS X

`/usr/local/Cellar/xz/5.2.5/lib/liblzma.5.dylib`

Apple Silicon

`/opt/homebrew/opt/xz/lib/liblzma.5.dylib`

####   --fix-sym-link

This option removes the following symbolic link from the application binary before signing

`{application}.app/Contents/Resources/lib/python{python version}/site.pyo`

Leaving this file in place with a signed and notarized application causes it to  fail the appVerify phase and renders the binary unusable

___

Written by <a href="mailto:email@humberto.a.sanchez.ii@gmail.com?subject=Hello Humberto">Humberto A. Sanchez II</a>  (C) 2026

---

## Note

For all kind of problems, requests, enhancements, bug reports, etc., please drop me an e-mail.


![Humberto's Modified Logo](https://raw.githubusercontent.com/wiki/hasii2011/gittodoistclone/images/SillyGitHub.png)

I am concerned about GitHub's Copilot project



I urge you to read about the [Give up GitHub](https://GiveUpGitHub.org) campaign from [the Software Freedom Conservancy](https://sfconservancy.org).

While I do not advocate for all the issues listed there I do not like that a company like Microsoft may profit from open source projects.

I continue to use GitHub because it offers the services I need for free.  But, I continue to monitor their terms of service.

Any use of this project's code by GitHub Copilot, past or present, is done without my permission.  I do not consent to GitHub's use of this project's code in Copilot.
