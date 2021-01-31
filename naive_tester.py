#!/usr/bin/env python3

import sys
import os
import subprocess
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')


def get_files(path, extension='.txt'):
    reference_files = []
    for dirname, _, files in os.walk(path):
        for fname in files:
            if fname.endswith(extension):
                reference_files.append(os.path.join(dirname, fname))
    # logger.info(f'total {len(reference_files)} files')
    return sorted(reference_files)


def check_file_existence(file_name, err_msg='File does not exit'):
    if not os.path.exists(file_name):
        logger.error(err_msg)
        sys.exit()


def get_result_from_file(file_name):
    check_file_existence(file_name)
    with open(file_name, 'r') as input_file:
        result = input_file.read().strip()
    return result


def do_files_comply(actual_in_files, actual_out_files):
    expected = set(map(lambda x: x[:-3] + '.out', actual_in_files))
    return not expected.difference(set(actual_out_files))


def run_job(job):
    script, args = job
    output = subprocess.run(
        [sys.executable] + [script, args],
        stdout=subprocess.PIPE,
        universal_newlines=True).stdout.strip('\n')
    return output


def assert_job(job, reference_output):
    script, args = job
    try:
        assert run_job(job) == reference_output
        logger.info(f'Successfully run the {script} with {args}')
    except AssertionError:
        logger.error(
            f'Failed run of the {script} with {args}. '
            f'The output should be {reference_output}')


def run_jobs(jobs_with_outputs):
    for job_with_output in jobs_with_outputs:
        assert_job(*job_with_output)


def main():
    if len(sys.argv) > 1:
        script_name = sys.argv[1]
        dir_name = sys.argv[2]
    else:
        sys.exit()

    check_file_existence(script_name, 'Script given does not exist')
    check_file_existence(script_name, 'Directory given does not exist')

    jobs_arguments = get_files(dir_name, '.in')
    output_files = get_files(dir_name, '.out')
    if not do_files_comply(jobs_arguments, output_files):
        logger.error('Input and output files do not comply')
        sys.exit()

    reference_outputs = []
    for file_name in output_files:
        with open(file_name, 'r') as output_file:
            output = output_file.read().strip()
            reference_outputs.append(output)

    jobs = zip([script_name for _ in jobs_arguments],
               jobs_arguments)

    jobs_with_outputs = zip(jobs, reference_outputs)

    run_jobs(jobs_with_outputs)


if __name__ == '__main__':
    main()
