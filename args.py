"""
@author: Jules Kreuer
@contact: contact@juleskreuer.eu
"""


import argparse


def main():
    return


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="A NICE TEXT")
    parser.add_argument(
        "-f",
        "--file",
        action="store",
        dest="path",
        help="Specify path to pileup file",
        required=True,
    )

    args = parser.parse_args()

    FILE_PATH = args.path

    main()
