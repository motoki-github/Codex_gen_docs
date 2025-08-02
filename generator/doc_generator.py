import os
import ast
import json
from pathlib import Path
from typing import List

try:
    import openai
except ImportError:  # pragma: no cover - openai optional
    openai = None


def scan_python_files(directory: Path) -> List[Path]:
    """Recursively gather all Python files under *directory*."""
    return [p for p in directory.rglob('*.py') if p.is_file()]


def summarize_file(path: Path) -> str:
    """Return a short summary of a Python file using OpenAI if available."""
    code = path.read_text()
    if openai and os.environ.get('OPENAI_API_KEY'):
        prompt = f"Summarize the following Python code:\n\n{code}"
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content.strip()
    # Fallback simple summary
    return f"Auto generated summary for {path.name}."


def generate_docstring(node: ast.AST) -> str:
    """Create a Google style docstring for *node*."""
    if isinstance(node, ast.FunctionDef):
        args = [a.arg for a in node.args.args]
        params = "\n".join(f"    {a}: TODO" for a in args)
        return f'"""TODO: Describe {node.name}.\n\nArgs:\n{params}\n"""'
    if isinstance(node, ast.ClassDef):
        return '"""TODO: Describe class."""'
    return '"""TODO"""'


def process_file(path: Path) -> str:
    """Generate documentation for a single Python file."""
    tree = ast.parse(path.read_text())
    parts = [f"# Documentation for {path.name}"]
    parts.append("## Summary")
    parts.append(summarize_file(path))

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            parts.append(f"### {node.name}")
            docstring = generate_docstring(node)
            parts.append('```python')
            parts.append(ast.get_source_segment(path.read_text(), node) or '')
            parts.append('```')
            parts.append('Docstring:')
            parts.append('```python')
            parts.append(docstring)
            parts.append('```')

    return "\n".join(parts)


def generate_docs(target: Path, output_dir: Path) -> None:
    """Generate documentation for all Python files under *target*."""
    output_dir.mkdir(parents=True, exist_ok=True)
    files = scan_python_files(target)
    written = []
    for py_file in files:
        doc = process_file(py_file)
        out_file = output_dir / f"{py_file.stem}.md"
        out_file.write_text(doc)
        written.append(out_file.name)
    # Write index for front-end to load
    index_file = output_dir / "index.json"
    index_file.write_text(json.dumps(written))
