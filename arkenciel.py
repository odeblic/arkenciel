#!/usr/bin/env python

from __future__ import print_function
import sys
import os


class Colorizer(object):

    def __init__(self, command, arguments):
        self.__command = command
        self.__arguments = arguments
        self.__state = None

    def process_out(self, line):
        line = '\033[34m' + line + '\033[39m'
        print(line, file=sys.stdout)

    def process_err(self, line):
        line = '\033[31m' + line + '\033[39m'
        print(line, file=sys.stderr)


def rollback():
    sys.stdout.write('\033[22m')
    sys.stdout.write('\033[39m')
    sys.stdout.write('\033[49m')
    sys.stdout.flush()


def display_usage():
    RAINBOW = [5, 1, 3, 2, 6, 4] * 2
    TITLE = 'ARKENCIEL'
    text = '\033[37mWelcome to '
    for i in range(0, len(TITLE)):
        text += '\033[3{};1m {}'.format(RAINBOW[i], TITLE[i])
    text += '\n\033[22;37mThis script colorizes the ouput of the invoked command'
    text += '\nUsage : {} command [arguments...]'.format(sys.argv[0])
    print(text, file=sys.stdout)
    rollback()


def main():
    if len(sys.argv) < 2:
        display_usage()
        return 0

    pipe_read_out, pipe_write_out = os.pipe()
    pipe_read_err, pipe_write_err = os.pipe()
    pid = os.fork()

    script = sys.argv[0]
    command = sys.argv[1]
    arguments = sys.argv[2:]

    colorizer = Colorizer(command, arguments)

    if pid == 0:
        os.close(pipe_read_out)
        os.close(pipe_read_err)
        os.dup2(pipe_write_out, sys.stdout.fileno())
        os.dup2(pipe_write_err, sys.stderr.fileno())
        try:
            os.execvp(command, [command] + arguments)
        except OSError as e:
            print('Cannot execute the command "{}": {}'.format(command, e), file=sys.stderr)
    else:
        os.close(pipe_write_out)
        os.close(pipe_write_err)
        pipe_fd_handle_out = os.fdopen(pipe_read_out)
        pipe_fd_handle_err = os.fdopen(pipe_read_err)
        try:
            while True:
                try:
                    line_out = pipe_fd_handle_out.readline()
                    line_err = pipe_fd_handle_err.readline()
                    if line_out:
                        colorizer.process_out(line_out[:-1])
                    if line_err:
                        colorizer.process_err(line_err[:-1])
                    if not line_out and not line_err:
                        break
                except KeyboardInterrupt:
                    pass
        finally:
            rollback()
            exec_result = os.wait()
            exit_status = int(exec_result[1] / 256)
            killing_signal = int(exec_result[1] % 256)
            if killing_signal != 0:
                os.kill(os.getpid(), killing_signal)
            else:
                return exit_status


if __name__ == "__main__":
    sys.exit(main())

