"""A simple (fairly pointless!) command line tool to process and validate the .json data."""

import json 
import traceback
import argparse
import logging 

import os 
from datetime import datetime
from tqdm import tqdm
from model import Compound
from pydantic.error_wrappers import ValidationError

def write_to_dlq(file_path, json_data):
    """Add a json line to the dlq."""

    with open(file_path, "a") as dql_fp:
        json.dump(json_data, dql_fp)
        dql_fp.write("\n") 

def process_json(data_loc: str, file_name: str, output_path: str, dlq: str = "./dlq.log") -> None:
    """Simple script to load json data, validate and output csv.
    
    Args:
        data_loc (str): Full path to raw data location
        file_name (str): Name of the json file to load  
        output_path (str): Full path and name of the output data file
        dlq (str, optional): Full path and name of dlq file 
    """

    # Load the json 
    data_file_path = os.path.join(data_loc, file_name)
    with open(data_file_path, encoding="utf-8-sig") as fp:
        raw_data = json.load(fp)

    logging.info("Loaded raw data, processing...")

    # Upload the data 
    with open(output_path, "w") as out_file:

        # Write out headers 
        out_file.write("compound_id, num_rings, image\n")

        # Iterate over compounds, loading into the pydantic model 
        bad_data_counter = 0
        for i, row in enumerate(tqdm(raw_data)):
            try:
                compound_data = Compound(**row)
            # This could be extended to handle different exceptions in a different way
            # for this example just store any validation errors
            except ValidationError as e:
                tb = traceback.format_exc()
                dlq_info = {"time": datetime.now().isoformat(), 
                            "file": data_file_path, 
                            "row": i, 
                            "error": str(e), 
                            "trace": tb, 
                            "data": row}
                write_to_dlq(dlq, dlq_info)
                bad_data_counter += 1
                continue 

            # Additional validation
            # Ensure there is an associated image 
            if not compound_data.image:
                dlq_info = {"time": datetime.now().isoformat(), 
                            "file": data_file_path, 
                            "row": i, 
                            "error": "Missing image key in json data, not suitable for DS task.", 
                            "trace": None, 
                            "data": row}
                write_to_dlq(dlq, dlq_info)
                bad_data_counter += 1
                continue 

            image_file_path = os.path.join(data_loc, compound_data.image)
            if not os.path.isfile(image_file_path):
                dlq_info = {"time": datetime.now().isoformat(), 
                            "file": data_file_path, 
                            "row": i, 
                            "error": f"Missing image at {image_file_path}, not suitable for DS task.", 
                            "trace": None, 
                            "data": row}
                write_to_dlq(dlq, dlq_info)
                bad_data_counter += 1
                continue 

            # Save data
            values = f"{compound_data.compound_id}, {compound_data.num_rings}, {compound_data.image}\n"
            out_file.write(values) 

    logging.info(f"Written data to {output_path}, {bad_data_counter} lines sent to the dlq at {dlq}")
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--data_loc", help="Full path to raw data location", type=str)
    parser.add_argument("--file_name", help="Name of the json file to load", type=str)
    parser.add_argument("--output_path", help="Full path and name of the output data file", type=str)
    parser.add_argument("--dlq", help="Full path and name of the dlq file", type=str, required=False)
    parser.add_argument("--log_level", help="Output level of logging", 
                                       type=str, 
                                       default="INFO",
                                       required=False,
                                       choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])

    args = parser.parse_args()

    # Set up some basic logging 
    logging.basicConfig(format="%(levelname)s:%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S", level="INFO")

    process_json(args.data_loc, args.file_name, args.output_path, args.dlq)