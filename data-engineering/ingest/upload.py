"""A simple command line tool to process and validate the .json data for modelling."""

import json 
import traceback

from datetime import datetime
from model import Compound
from pydantic.error_wrappers import ValidationError

def process_json(input_path: str, output_path: str, dlq: str = "dlq.log") -> None:
    """Simple script to load json data, validate and output csv.
    
    Args:
        input_path (str): Full path of input json 
        output_path (str): Full path to output data to 
        dlq (str, optional): Path to dlq file for tracking bad data
    """

    # Load the json 
    with open(input_path, encoding="utf-8-sig") as fp:
        raw_data = json.load(fp)
    print(json.dumps(raw_data, indent=4))

    # Upload the data 
    with open(output_path, "w") as out_file:

        # out_file.write()

        # Iterate over compounds, loading into the pydantic model 
        for i, row in enumerate(raw_data):
            try:
                test = Compound(**row)
            # This could be extended to handle different exceptions in a different way
            # for this example just store any validation errors
            except ValidationError as e:
                tb = traceback.format_exc()
                dlq_info = {"time": datetime.now().isoformat(), "file": input_path, "row": i, "error": str(e), "trace": tb, "data": row}
                with open(dlq, "a") as dql_fp:
                    json.dump(dlq_info, dql_fp)
                    dql_fp.write("\n")
                continue 

        print(test)
        # Additional validation

        # Save data 

process_json("../../raw-data/sample.json", "./test.csv", dlq="dlqtest.json")