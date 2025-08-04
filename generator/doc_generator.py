import os
import ast
import json
from pathlib import Path
from typing import List

try:
    import openai
except ImportError:  # pragma: no cover - openai optional
    openai = None


class DocGenerator:
    """Generate Markdown documentation for Python files."""

    def __init__(self, root_path: str, output_dir: str) -> None:
        self.root_path = Path(root_path)
        self.output_dir = Path(output_dir)

    def generate(self) -> None:
        """Generate documentation files.

        Walks through the ``root_path`` directory, finds all ``.py`` files,
        creates a summary for each file, extracts docstrings for functions
        and classes, and writes the results as Markdown files in
        ``output_dir``.
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)
        py_files = self._find_python_files()
        written = []
        for file_path in py_files:
            rel_path = file_path.relative_to(self.root_path)
            summary = self._summarize_file(file_path)
            doc_lines = [f"# {rel_path}", "", summary, ""]
            doc_lines += self._extract_docstrings(file_path)
            out_file = self.output_dir / f"{file_path.stem}.md"
            out_file.write_text("\n".join(doc_lines))
            written.append(out_file.name)
        # Write index for front-end to load
        index_file = self.output_dir / "index.json"
        index_file.write_text(json.dumps(written))

    def _find_python_files(self) -> List[Path]:
        """Recursively gather all Python files under root_path."""
        return [p for p in self.root_path.rglob('*.py') if p.is_file()]

    def _summarize_file(self, path: Path) -> str:
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

    def _extract_docstrings(self, path: Path) -> List[str]:
        """Extract and format docstrings from Python file."""
        tree = ast.parse(path.read_text(), filename=str(path))
        lines: List[str] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                lines.append(f"## {node.name}")
                lines.append("")
                lines.append(self._generate_docstring(node))
                lines.append("")
        return lines

    def _generate_docstring(self, node: ast.AST) -> str:
        """Create a Google style docstring for *node*."""
        if isinstance(node, ast.FunctionDef):
            args = [a.arg for a in node.args.args]
            params = "\n".join(f"    {a}: TODO" for a in args)
            return f'"""TODO: Describe {node.name}.\n\nArgs:\n{params}\n"""'
        if isinstance(node, ast.ClassDef):
            return '"""TODO: Describe class."""'
        return '"""TODO"""'


# Backward compatibility function
def generate_docs(target: Path, output_dir: Path) -> None:
    """Generate documentation for all Python files under *target*."""
    generator = DocGenerator(str(target), str(output_dir))
    generator.generate()

