import sys
import argparse
from rich.console import Console

import sample_s3


def App() -> int:
    console = Console(color_system="auto")
    args = parser.parse_args()

    console.rule(" Homework 01 ")



    # S3 examples , list/create/delete buckets
    temp_bucket_name = "njashkajhsdkjahdakjsdh" 
    sample_s3.s3_list_buckets()
    sample_s3.s3_create_bucket(temp_bucket_name) # name to be globally unique I think?
    sample_s3.s3_list_buckets()
    sample_s3.s3_delete_bucket(temp_bucket_name)
    sample_s3.s3_list_buckets()


    console.rule(" The END ") 
    return 0


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog="AWS Homework 1",
                                     add_help=True, 
                                     description="AWS learnings .....",
                                     epilog="Author Philip Hill (2025)")
    # All args added one by one here. 

    parser.add_argument("--test", 
                        default="defaultvaluehere", 
                        required=False, 
                        type=str,
                        help="Help for default value")
    
    parser.add_argument("--verbose", 
                        action="store_true",
                        help="Run with extra debug output")
    
    try:
        args = parser.parse_args()
    except argparse.ArgumentError:
        # problem with args, argparse will flag the error -> just quit
        sys.exit(-1)

    sys.exit(App()) 