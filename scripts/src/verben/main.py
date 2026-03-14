import os
import types

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
        parts = VerbenTokenizer.tokenizeToNode(line)
        node = types.SimpleNamespace(
            base_word=parts[0].to_html(),
            ich=parts[1].to_html(),
            du=parts[2].to_html(),
            er_sie_es=parts[3].to_html(),
            wir=parts[4].to_html(),
            ihr=parts[5].to_html(),
            sie_Sie=parts[6].to_html(),
            translationEn=parts[7].to_html(),
            translationVi=parts[8].to_html(),
            sentence=parts[9].to_html(),
            tag=parts[10].to_html(),
        )
        compiled_lines.append(compiler.compileNodeToString(node))

    with open(result_path, "w", encoding="utf-8") as f:
        f.write(compiler.joinStrings(compiled_lines))


if __name__ == "__main__":
    execute()
