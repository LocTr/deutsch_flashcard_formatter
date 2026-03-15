from scripts.src.verben.verben import Verben
from scripts.src.models.base_elements import Node


class VerbenCompiler:

    def compileVerben(self, verb: Verben, nodes: list[Node]) -> str:
        """Compile Verben dataclass and its nodes to HTML string for Anki."""
        # Convert nodes to HTML
        base_word_html = nodes[0].to_html()
        ich_html = nodes[1].to_html()
        du_html = nodes[2].to_html()
        er_sie_es_html = nodes[3].to_html()
        wir_html = nodes[4].to_html()
        ihr_html = nodes[5].to_html()
        sie_sie_html = nodes[6].to_html()
        translation_en_html = nodes[7].to_html()
        translation_vi_html = nodes[8].to_html()
        sentence_html = nodes[9].to_html()
        tag_html = nodes[10].to_html()

        conjugations = "<br>".join([
            ich_html, du_html, er_sie_es_html,
            wir_html, ihr_html, sie_sie_html,
        ])
        translations = "<br>".join([translation_en_html, translation_vi_html])
        return f"{base_word_html}\t{translations}\t{sentence_html}<br><br>{conjugations}\t{tag_html}"

    def joinStrings(self, strings: list[str]) -> str:
        return "\n".join(strings)
