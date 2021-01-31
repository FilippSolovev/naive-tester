

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
