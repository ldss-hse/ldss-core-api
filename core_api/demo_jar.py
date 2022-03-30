import enum
import json
import platform
import shutil
import subprocess
from pathlib import Path

from constants import SCRIPTS_PATH, ARTIFACTS_PATH


class DecisionMakerCrashedError(Exception):
    pass


class CLIExecutableEnum(enum.Enum):
    bash = 1
    powershell = 2
    python = 3

    def __str__(self):
        mapping = {
            CLIExecutableEnum.bash: 'bash',
            CLIExecutableEnum.python: 'python',
            CLIExecutableEnum.powershell: 'Powershell.exe',
        }
        return mapping[self]


def run_console_tool(tool_path: Path, exe: CLIExecutableEnum = CLIExecutableEnum.bash, *args, **kwargs):
    kwargs_processed = []
    for item in kwargs.items():
        if item[0] in ('env', 'debug'):
            continue
        kwargs_processed.extend(map(str, item))

    options = [str(exe)]
    if exe is CLIExecutableEnum.powershell:
        options.append('-File')

    options.extend([
        str(tool_path),
        *args,
        *kwargs_processed
    ])

    if kwargs.get('debug', False):
        print(f'Attempting to run with the following arguments: {options}')

    if kwargs.get('env'):
        return subprocess.run(options, capture_output=True, env=kwargs.get('env'))
    return subprocess.run(options, capture_output=True)


def run_jar():
    if platform.system() == 'Windows':
        tool_path = SCRIPTS_PATH / 'run_decision_maker.ps1'
        exe = CLIExecutableEnum.powershell
    else:
        tool_path = SCRIPTS_PATH / 'run_decision_maker.sh'
        exe = CLIExecutableEnum.bash

    jar_path = SCRIPTS_PATH / 'bin' / 'lingvo-dss-all.jar'
    json_path = SCRIPTS_PATH / 'bin' / 'description_multilevel.json'

    arguments = [
        '-JAR_PATH', str(jar_path),
        '-INPUT_JSON', str(json_path),
        '-OUTPUT_DIR', str(ARTIFACTS_PATH)
    ]
    res_process = run_console_tool(tool_path, exe, *arguments, debug=True)
    stdout = str(res_process.stdout.decode("utf-8"))
    print(f'SUBPROCESS: {stdout}')
    print(f'SUBPROCESS: {str(res_process.stderr.decode("utf-8"))}')

    if res_process.returncode != 0 or '[ERROR] ' in stdout:
        raise DecisionMakerCrashedError('Decision Maker did not finish successfully')


def parse_results(json_path: Path):
    with json_path.open(encoding='utf-8') as f:
        res = json.load(f)
    return res


def main():
    if ARTIFACTS_PATH.exists():
        shutil.rmtree(ARTIFACTS_PATH)

    run_jar()

    json_path = ARTIFACTS_PATH / 'result.json'
    parsed_results = parse_results(json_path)

    print(parsed_results)


if __name__ == '__main__':
    main()
