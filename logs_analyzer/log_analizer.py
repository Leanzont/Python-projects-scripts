# log_analyzer.py
def logs_analyzer(input_file, output_file):

    # Dictionary used to count log levels
    counters = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0
    }

    # Lists used to store categorized logs
    info_logs = []
    warning_logs = []
    error_logs = []

    # Read all lines from the input file
    with open(input_file, "r") as f:
        lines = f.readlines()

    # Analyze each line
    for line in lines:

        # Remove spaces and line breaks
        line = line.strip()

        # Categorize logs
        if line.startswith("INFO"):
            counters["INFO"] += 1
            info_logs.append(line)

        elif line.startswith("WARNING"):
            counters["WARNING"] += 1
            warning_logs.append(line)

        elif line.startswith("ERROR"):
            counters["ERROR"] += 1
            error_logs.append(line)

    # Calculate total logs
    total = sum(counters.values())

    # Display summary
    print("*" * 35)
    print("          Summary Logs")
    print("*" * 35)

    print(f"INFO: {counters['INFO']}")
    print(f"WARNING: {counters['WARNING']}")
    print(f"ERROR: {counters['ERROR']}")
    print(f"Total: {total}")

    # Calculate percentages
    if total > 0:

        percentage_error = (counters['ERROR'] / total) * 100
        percentage_info = (counters['INFO'] / total) * 100
        percentage_warning = (counters['WARNING'] / total) * 100

        print(f"% Errors: {percentage_error:.1f}%")
        print(f"% Info: {percentage_info:.1f}%")
        print(f"% Warning: {percentage_warning:.1f}%")

    # Save results into a file
    with open(output_file, "w") as f:

        f.write("------- INFO LOGS -------\n")
        f.write(f"INFO: {counters['INFO']}\n")
        f.write(f"Lines: {info_logs}\n")
        f.write("~" * 40 + "\n")

        f.write(f"WARNING: {counters['WARNING']}\n")
        f.write(f"Lines: {warning_logs}\n")
        f.write("~" * 40 + "\n")

        f.write(f"ERROR: {counters['ERROR']}\n")
        f.write(f"Lines: {error_logs}\n")

    print(f"Results saved in '{output_file}'")


# Function call
logs_analyzer("logsTest.txt", "info_logs.txt")


