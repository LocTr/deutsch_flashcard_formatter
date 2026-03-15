import os

from scripts.src.verben.verben_compiler import VerbenCompiler
from scripts.src.verben.verben_tokenizer import VerbenTokenizer

FILES_DIR = os.path.join(os.path.dirname(__file__), "..")


def execute():
    tokenizer = VerbenTokenizer()
    compiler = VerbenCompiler()

    source_path = os.path.join(FILES_DIR, "files/verben/source.txt")
    result_path = os.path.join(FILES_DIR, "files/verben/result.txt")

    with open(source_path, "r", encoding="utf-8") as f:
        text = f.read()

    lines = tokenizer.tokenizeEachLine(text)

    compiled_lines = []
    for line in lines:
        # Pipeline: str -> Verben -> Node list -> HTML string
        verb = tokenizer.parseToVerb(line)
        nodes = tokenizer.verbenToNodes(verb)
        compiled_lines.append(compiler.compileVerben(verb, nodes))

    with open(result_path, "w", encoding="utf-8") as f:
        f.write(compiler.joinStrings(compiled_lines))


if __name__ == "__main__":
    execute()
