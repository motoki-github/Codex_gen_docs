# Codex_gen_docs

Generate Markdown documentation for Python projects and view it in the browser.

## Usage

1. **Generate docs**

   ```bash
   python generate_docs.py path/to/project -o output
   ```

   The script scans the target directory for `*.py` files and writes a set of
   Markdown files to the `output/` folder.

2. **View docs**

   Serve the `frontend/` folder with any static file server:

   ```bash
   cd frontend
   python -m http.server 8000
   ```

   Open `http://localhost:8000` in your browser to view the generated
   documentation.

## Customising AI integration

The current implementation uses placeholder text for file summaries and
function docstrings. Update `generator/doc_generator.py` to call your AI
service in `_summarize_file` and `_generate_docstring` if desired.
