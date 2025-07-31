import ast
from pathlib import Path
from typing import List


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
        index_lines = ["# Project Documentation", ""]
        for file_path in py_files:
            rel_path = file_path.relative_to(self.root_path)
            summary = self._summarize_file(file_path)
            doc_lines = [f"# {rel_path}", "", summary, ""]
            doc_lines += self._extract_docstrings(file_path)
            out_file = self.output_dir / f"{file_path.stem}.md"
            out_file.write_text("\n".join(doc_lines))
            index_lines.append(f"- [{rel_path}]({out_file.name})")
        (self.output_dir / "index.md").write_text("\n".join(index_lines))

    def _find_python_files(self) -> List[Path]:
        return list(self.root_path.rglob("*.py"))

    def _summarize_file(self, path: Path) -> str:
        """Return a placeholder summary for ``path``."""
        return f"Summary for {path.name}."

    def _extract_docstrings(self, path: Path) -> List[str]:
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
        """Return a placeholder Google-style docstring for ``node``."""
        return f"""{node.name}

Auto-generated description for {node.name}.

Args:
    *args: Positional arguments.
    **kwargs: Keyword arguments.

Returns:
    Any: Description of return value.
"""

