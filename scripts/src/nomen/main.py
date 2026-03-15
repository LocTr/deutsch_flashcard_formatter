import os

from scripts.src.nomen.nomen_compiler import NomenCompiler
from scripts.src.nomen.nomen_tokenizer import NomenTokenizer

FILES_DIR = os.path.join(os.path.dirname(__file__), "..", "files")


def execute():
    tokenizer = NomenTokenizer()
    compiler = NomenCompiler()

    source_path = os.path.join(FILES_DIR, "../files/nomen/source.txt")
    result_path = os.path.join(FILES_DIR, "../files/nomen/result.txt")

    with open(source_path, "r", encoding="utf-8") as f:
        text = f.read()

    lines = tokenizer.tokenizeEachLine(text)

    compiled_lines = []
    for line in lines:
        # Pipeline: str -> Nomen -> Node list -> HTML string
        nomen = tokenizer.parseToNomen(line)
        nodes = tokenizer.nomenToNodes(nomen)
        compiled_lines.append(compiler.compileNomen(nomen, nodes))

    with open(result_path, "w", encoding="utf-8") as f:
        f.write(compiler.joinStrings(compiled_lines))


if __name__ == "__main__":
    execute()
