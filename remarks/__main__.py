import logging
import pathlib
import argparse
import os
import sys

from remarks import run_remarks

__prog_name__ = "remarks"
__version__ = "0.3.1"


def main():
    parser = argparse.ArgumentParser(__prog_name__, add_help=False)

    parser.add_argument(
        "input_dir",
        help="xochitl-derived directory that contains *.pdf, *.content, *.metadata, *.highlights/*.json and */*.rm files. Can also be given by $REMARKS_INPUT_DIR",
        metavar="INPUT_DIRECTORY",
        nargs="?"
    )
    parser.add_argument(
        "output_dir",
        help="Base directory for all files created (*.pdf, *.png, *.md, and/or *.svg). Can also be given by $REMARKS_OUTPUT_DIR",
        metavar="OUTPUT_DIRECTORY",
        nargs="?"
    )
    parser.add_argument(
        "--file_name",
        help="Work only on files whose original document names (visibleName) contain this string",
        metavar="FILENAME_STRING",
    )
    parser.add_argument(
        "--file_uuid",
        help="Work only on files whose uuid is this string",
        metavar="UUID_STRING",
    )
    parser.add_argument(
        "--file_path",
        help="Work only on files whose (meaningful) path contains this string. Overrides $REMARKS_FILE_PATH variable",
        metavar="FILEPATH_STRING",
    )
    parser.add_argument(
        "--ann_type",
        help="Force remarks to handle only a specific type of annotation: highlights or scribbles. If none is specified, remarks will handle both by default",
        default=["scribbles", "highlights"],
        metavar="ANNOTATION_TYPE",
    )
    parser.add_argument(
        "--skip_combined_pdf",
        dest="combined_pdf",
        action="store_false",
        help="Skip the creation of the default '*_remarks.pdf' file that contains all annotated pages merged into the original PDF file",
    )
    parser.add_argument(
        "--skip_combined_md",
        dest="combined_md",
        action="store_false",
        help="Skip the creation of the default '*_highlights.md' file that contains all textual content extracted from highlights",
    )
    parser.add_argument(
        "--modified_pdf",
        dest="modified_pdf",
        action="store_true",
        help="Create a '*_remarks-only.pdf' file with annotated pages only (unannotated ones will be out)",
    )
    parser.add_argument(
        "--md_hl_format",
        help="Choose how highlighted text should be written in Markdown. Options are: bullet_points or whole_block. Defaults to whole_block",
        default="whole_block",
        metavar="HIGHLIGHTS_FORMAT",
    )
    parser.add_argument(
        "--md_hl_output_dir",
        help="Choose where to save Markdown files with highlighted text. Defaults to FILE_PATH",
        metavar="HIGHLIGHTS_FOLDER_OUTPUT_DIRECTORY",
    )
    parser.add_argument(
        "--md_page_offset",
        help="For page headers in Markdown files, offset their value by PAGE_OFFSET. This is useful for citations. Defaults to 0",
        default=0,
        type=int,
        metavar="PAGE_OFFSET",
    )
    parser.add_argument(
        "--md_header_format",
        dest="md_header_format",
        default="atx",
        help="For Markdown files, use either atx headers (# Heading 1; ## Heading 2) or setex (dashes under a header title). Defaults to atx",
        metavar="HEADER_FORMAT",
    )
    parser.add_argument(
        "--md_obsidian_format",
        dest="md_obsidian_format",
        default=True,
        help="For Markdown files, use a pre-set template intended for Obsidian. Only works with 'atx' header format. Defaults to True",
        metavar="OBSIDIAN FORMAT"
    )
    parser.add_argument(
        "--per_page_targets",
        nargs="+",
        help="Target specific file formats per page. Choose at least one of the following extensions: md pdf png svg. This is empty by default",
        default=[],
        metavar="FILE_EXTENSION",
    )
    parser.add_argument(
        "--assume_malformed_pdfs",
        dest="assume_malformed_pdfs",
        action="store_true",
        help="Assume PDF files are malformed, i.e. words are NOT in their natural reading order and/or fonts are obfuscated. By default, we're optimists and assume your PDFs are well-formed",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        help="Show remarks version number",
        version="%(prog)s {version}".format(version=__version__),
    )
    parser.add_argument(
        "--log_level",
        help="Print out log messages with equal or higher severity level as specified by LOG_LEVEL. Currently supported: DEBUG < INFO < WARNING < ERROR. Choose DEBUG to print out all messages, ERROR to print out just error messages, etc. If a log level is not set, it defaults to INFO",
        default="INFO",
        metavar="LOG_LEVEL",
    )
    parser.add_argument(
        "--avoid_ocr",
        action="store_true",
        help="By default, remarks tries to use OCRmyPDF to extract highlighted text from image-based PDFs. Use this flag to skip running the ocrmypdf executable altogether. Defaults to true",
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show this help message",
    )

    parser.set_defaults(
        combined_pdf=True,
        modified_pdf=False,
        assume_malformed_pdfs=False,
        combined_md=True,
        avoid_ocr=True,
    )

    args = parser.parse_args()
    args_dict = vars(args)

    input_dir = args_dict.pop("input_dir")
    output_dir = args_dict.pop("output_dir")

    log_level = args_dict.pop("log_level")
    logging.basicConfig(
        format="%(message)s",
        level=log_level,
    )

    if input_dir is None and output_dir is None:
        input_dir = os.getenv("REMARKS_INPUT_DIR")
        output_dir = os.getenv("REMARKS_OUTPUT_DIR")
        if input_dir is None:
            print("Requires REMARKS_INPUT_DIR variable, or positional arguent.", file=sys.stderr)
        if output_dir is None:
            print("Requires REMARKS_OUTPUT_DIR variable, or positional argument.", file=sys.stderr)
        if input_dir is None or output_dir is None:
            exit(1)
    elif input_dir is None or output_dir is None:
        print("Both or neither positional argument INPUT_DIRECTORY and OUTPUT_DIRECTORY must be given", file=sys.stderr)
        exit(1)


    if not pathlib.Path(input_dir).exists():
        parser.error(f'Directory "{input_dir}" does not exist')

    if not pathlib.Path(output_dir).is_dir():
        pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)


    if args_dict["file_path"] is None:
        args_dict["file_path"] = os.getenv("REMARKS_FILE_PATH")
    if args_dict["md_hl_output_dir"] is None:
        args_dict["md_hl_output_dir"] = os.getenv("REMARKS_MD_HL_OUTPUT_DIR")

    run_remarks(input_dir, output_dir, **args_dict)


if __name__ == "__main__":
    main()
