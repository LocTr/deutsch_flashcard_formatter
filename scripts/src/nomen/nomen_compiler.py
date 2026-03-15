
from scripts.src.nomen.nomen import Nomen
from scripts.src.models.base_elements import Node


class NomenCompiler:

    def compileNomen(self, nomen: Nomen, nodes: list[Node]) -> str:
        """Compile Nomen dataclass and its nodes to HTML string for Anki."""
        # Convert nodes to HTML
        singular_html = nodes[0].to_html()
        plural_html = nodes[1].to_html()
        translation_en_html = nodes[2].to_html()
        translation_vi_html = nodes[3].to_html()
        sentence_html = nodes[4].to_html()
        tag_html = nodes[5].to_html()

        # Combine translations with line break
        translations = "<br>".join([translation_en_html, translation_vi_html])

        return f"{singular_html}<br>{plural_html}\t{translations}\t{sentence_html}\t{tag_html}"

    def joinStrings(self, strings: list[str]) -> str:
        return "\n".join(strings)