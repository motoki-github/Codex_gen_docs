# Codex_gen_docs

This repository provides a simple tool to generate documentation for Python
projects and view the result in a lightweight React front-end.

## Generating documentation

Use the CLI to scan a directory and write Markdown documentation to the
`output/` folder:

```bash
python generate_docs.py path/to/project -o output
```

The script walks the given directory, creates summaries and example docstrings
for all Python files and writes a Markdown file for each one. An `index.json`
file is also produced so the front-end can list the generated pages.

## Viewing the documentation

A minimal React application is located under `frontend/`. To preview the
documentation open a simple HTTP server in that directory:

```bash
cd frontend
python -m http.server 8000
```

Then visit `http://localhost:8000` in your browser. The app will load the
Markdown files from `../output/` and render them.
