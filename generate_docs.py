from pathlib import Path
import argparse

from generator.doc_generator import DocGenerator


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Markdown docs from Python files")
    parser.add_argument("path", help="Target directory to scan")
    parser.add_argument("-o", "--output", default="output", help="Output directory for docs")
    args = parser.parse_args()

    generator = DocGenerator(args.path, args.output)
    generator.generate()
    print(f"Documentation written to {Path(args.output).resolve()}")


if __name__ == "__main__":
    main()

