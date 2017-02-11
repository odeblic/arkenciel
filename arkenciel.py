#!/usr/bin/env python

from __future__ import print_function
import sys
import os


def print_out(line):
    line = '\033[34m' + line + '\033[39m'
    print(line, file=sys.stdout)


def print_err(line):
    line = '\033[31m' + line + '\033[39m'
    print(line, file=sys.stderr)


def rollback():
    sys.stdout.write('\033[22m')
    sys.stdout.write('\033[39m')
    sys.stdout.write('\033[49m')
    sys.stdout.flush()


def main():
    pipe_read_out, pipe_write_out = os.pipe()
    pipe_read_err, pipe_write_err = os.pipe()
    pid = os.fork()
    script = sys.argv[0]
    command = sys.argv[1]
    arguments = sys.argv[2:]

    if pid == 0:
        os.close(pipe_read_out)
        os.close(pipe_read_err)
        os.dup2(pipe_write_out, sys.stdout.fileno())
        os.dup2(pipe_write_err, sys.stderr.fileno())
        os.execvp(command, [command] + arguments)
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
                        print_out(line_out[:-1])
                    if line_err:
                        print_err(line_err[:-1])
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

