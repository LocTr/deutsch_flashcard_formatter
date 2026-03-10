import os
import types
from scripts.src.tasks.nomen_tokenizer import NomenTokenizer
from scripts.src.tasks.nomen_compiler import NomenCompiler

FILES_DIR = os.path.join(os.path.dirname(__file__), "..", "files")


def execute():
    tokenizer = NomenTokenizer()
    compiler = NomenCompiler()

    source_path = os.path.join(FILES_DIR, "source.txt")
    result_path = os.path.join(FILES_DIR, "result.txt")

    with open(source_path, "r", encoding="utf-8") as f:
        text = f.read()

    lines = tokenizer.tokenizeEachLine(text)

    compiled_lines = []
    for line in lines:
        parts = NomenTokenizer.tokenizeToNode(line)
        node = types.SimpleNamespace(
            singular=parts[0].to_html(),
            plural=parts[1].to_html(),
            translation=parts[2][0].to_html(),
            sentence=parts[3][0].to_html(),
            tag=parts[4],
        )
        compiled_lines.append(compiler.compileNodeToString(node))

    with open(result_path, "w", encoding="utf-8") as f:
        f.write(compiler.joinStrings(compiled_lines))


if __name__ == "__main__":
    execute()
