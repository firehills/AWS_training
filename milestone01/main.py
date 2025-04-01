import sys
import argparse
import rich
from rich.console import Console


def App() -> int:
    console = Console(color_system="auto")
    args = parser.parse_args()

    console.rule(" Homework 01 ")
    console.print("[bold red]Remainder TODO")
    console.rule(" The END ") 
    return 0


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog="AWS Homework 1",
                                     add_help=True, 
                                     description="Set by Kapil .....",
                                     epilog="Author Philip Hill (2025)")
    # All args added one by one here. 

    #TODO this could be any text base information source, eg a document/paper/news article ..?
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