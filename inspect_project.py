import os
from pathlib import Path

OUTPUT_FILE = "project_summary.txt"

def print_tree(root, output, indent=""):
    for path in sorted(Path(root).rglob("*")):
        rel_path = path.relative_to(root)
        prefix = "📁" if path.is_dir() else "📄"
        output.write(f"{indent}{prefix} {rel_path}\n")

def preview_file(file_path, output):
    output.write(f"\n📄 {file_path}:\n")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            contents = f.read()
            output.write(contents + "\n")
    except Exception as e:
        output.write(f"❌ Could not read {file_path}: {e}\n")

def main():
    base_path = Path(__file__).resolve().parent
    docs_path = base_path / "docs"
    climalysis_path = base_path / "climalysis"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as output:
        output.write("\n==== 📚 docs/ Tree ====\n\n")
        print_tree(docs_path, output)

        output.write("\n==== 🔍 Full Contents of .rst Files in docs/ ====\n")
        for rst_file in docs_path.rglob("*.rst"):
            preview_file(rst_file, output)

        output.write("\n==== 🌱 climalysis/ Tree ====\n\n")
        print_tree(climalysis_path, output)

        output.write("\n==== 🧠 Full Contents of Python Files in climalysis/ ====\n")
        for py_file in climalysis_path.rglob("*.py"):
            preview_file(py_file, output)

    print(f"\n✅ Full project contents saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
