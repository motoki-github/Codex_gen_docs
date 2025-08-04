#!/usr/bin/env python
from pathlib import Path
import argparse
from generator.doc_generator import generate_docs


def main():
    parser = argparse.ArgumentParser(description="Generate Markdown docs from Python files")
    parser.add_argument("target", type=str, help="Target directory to scan")
    parser.add_argument("--output", "-o", default="output", help="Output directory")
    args = parser.parse_args()

    target = Path(args.target)
    output = Path(args.output)
    generate_docs(target, output)
    print(f"Documentation written to {output}")


if __name__ == "__main__":
    main()
