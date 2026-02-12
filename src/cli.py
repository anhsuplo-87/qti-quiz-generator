import argparse
import sys

from core.build import build_qti_package
from utils.logger import setup_logger


def main():
    parser = argparse.ArgumentParser(
        description='Convert JSON file to QTI XML package')

    parser.add_argument('--sample_folder', type=str,
                        default='xml-sample/sample-image', help='Folder containing sample files')
    parser.add_argument('--json_file', type=str,
                        default='json-sample/sample_image_question.json', help='JSON file to convert, (same folder with images)')
    parser.add_argument('--output_folder', type=str,
                        default='output', help='XML folder to save')
    parser.add_argument('--verbose', action='store_true',
                        help="Show debug logging")

    args = parser.parse_args()

    logger = setup_logger(verbose=args.verbose)

    try:
        build_qti_package(
            sample_folder=args.sample_folder,
            json_file=args.json_file,
            output_folder=args.output_folder
        )

    except Exception as e:
        logger.error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
