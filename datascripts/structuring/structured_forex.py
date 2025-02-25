import pandas as pd
import os


def merge_forex_data(data_dir, output_file):
    all_data = []

    for file_name in os.listdir(data_dir):
        if file_name.startswith("forex_data_") and file_name.endswith(".csv"):
            try:
                parts = (
                    file_name.replace("forex_data_", "").replace(".csv", "").split("_")
                )
                duration = parts[0]
                currency_pair = "_".join(parts[1:])

                # Read data from csv
                filepath = os.path.join(data_dir, file_name)
                df = pd.read_csv(filepath)

                # Add durationd and currency pair columns
                df["duration"] = duration
                df["currency_pair"] = currency_pair

                all_data.append(df)

            except Exception as e:
                print(f"Error processing file {file_name}: {e}")
        else:
            print("Unexpected filename encountered")
            return

    # Concat all dataframes
    if all_data:
        merged_data = pd.concat(all_data, ignore_index=True)

        # Write to output CSV
        merged_data.to_csv(output_file, index=False)
        print(f"Successfully merged data to {output_file}")
    else:
        print("No matching files found in the directory.")


# MAIN
if __name__ == "__main__":
    # Get the current directory (Where the script is running)
    current_directory = os.path.dirname(os.path.abspath(__file__))
    data_directory = "D:\Joe Workspace\Github\python-alpha\cleaned-data\currency_pairs"

    # Use the full path to the file (in the same directory as the script)
    output_filepath = os.path.join(current_directory, "forex_structured.csv")

    # Create a dummy data directory
    if not os.path.exists(data_directory):
        print("Path does not exist")
        os.makedirs(data_directory)

    # Execute code here
    merge_forex_data(data_directory, output_filepath)
