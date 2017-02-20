# Get rid of monochrome text console with Arkenciel

## Foreword

This is my first open source project, my first contribution to this fantastic world where knowledge is the shared value. I hope this will help

## Overview

Initially, I wanted to find a solution to colorize **maven** output. It is really verbose and too much information does not help if you cannot find what is relevant, especially when you are not familiar with this application.

Indeed, colors in the terminal has nothing to do with art (maybe arguable) but with clarity. Highlighting this or that work or sentence helps a lot to find what you need on first sight.

**Arkenciel** tries to fill this gap and also covers a set of commands, with a specific pattern of colors for each of them.

## Usage

It is very simple : any command you want to colorize, just prefix them with **arkenciel** and that's all.

    arkenciel mvn
    arkenciel ipconfig

You may want to add arguments for your command. Just append them on the line and they will be passed to the command.

    arkenciel mvn -offline build
    arkenciel ipconfig interface eth0 down

## How it works

Basically, **arkenciel** just forks and forwards the arguments to the child process. Then, it waits for the termination and exits. Before they reach the terminal, the output and error streams are hooked, parsed and modified on-the-fly, adding some escape sequences to set colors.

_Standard output stream_

The **stdout** stream is hooked by **arkenciel** and is colorized accordingly to configuration.

_Standard error stream_

The **stderr** stream is hooked by **arkenciel** and is colorized accordingly to configuration.

_Standard input stream_

The **stdin** stream is not hooked by **arkenciel** and remains untouched.

_Exit status code_

The exit status code is exactly the one which is returned by the invoked command.

_Signal handling_

If any signal is sent to the invoked command, **arkenciel** will behave as if it received this signal itself.

## Installation

Good news : you do not need to be root ! Just copy the script in your home directory and set its executable bit.

    chmod +x ~/arkenciel.py

You may want to add aliases in your Bash profile to invoke your favorite commands seemlessly.

    alias mvn = ~/arkenciel.py mvn
    alias ifconfig = ~/arkenciel.py ifconfig

## Licence

This is an open source program. You can use it, distribute it, modify it.

Please mention the author when you redistribute the code.

Any suggestion of improvement is very welcome.

Enjoy !

odeblic@gmail.com

