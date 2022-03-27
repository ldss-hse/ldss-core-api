import argparse
import os
import shlex
import subprocess
from threading import Timer


def run(cmd, timeout_sec):
    proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timer = Timer(timeout_sec, proc.kill)
    try:
        timer.start()
        stdout, stderr = proc.communicate()
        print(stdout)
        print(stderr)
    finally:
        timer.cancel()
        print(stdout)
        print(stderr)



def parse_arguments():
    parser = argparse.ArgumentParser(description='CLI Manager for Core API application')

    parser.add_argument('--flask',
                        required=False,
                        default=False,
                        action='store_true',
                        help='Specifies whether to start Core API backend')

    return parser.parse_args()


def main():
    args = parse_arguments()

    print('All arguments passed to CLI Manager')
    print(args)

    if args.flask:
        print('Requested to run flask application, running...')
        cmd = "../../venv/bin/python app.py > /Users/demidovs/Documents/projects/1_hse/ldss-core-api/core_api/core_api/log.txt"
        cmds = shlex.split(cmd)
        print(cmds)

        # Examples: both take 1 second
        run(cmd, 1)  # process ends normally at 1 second
        # res_process = subprocess.run(cmds,
        #                              capture_output=True,
        #                              # start_new_session=True,
        #                              env=dict(os.environ,
        #                                       **{
        #                                           'FLASK_ENV': 'development',
        #                                           'FLASK_APP': 'core_api',
        #                                       })
        #                              )
        # print(f'SUBPROCESS: {str(res_process.stdout.decode("utf-8"))}')
        # print(f'SUBPROCESS: {str(res_process.stderr.decode("utf-8"))}')


if __name__ == '__main__':
    main()
