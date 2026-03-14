class VerbenCompiler:

    def compileNodeToString(self, node) -> str:
        conjugations = "<br>".join([
            node.ich, node.du, node.er_sie_es,
            node.wir, node.ihr, node.sie_Sie,
        ])
        translations = "<br>".join([node.translationEn, node.translationVi])
        return f"{node.base_word}\t{translations}\t{node.sentence}<br><br>{conjugations}\t{node.tag}"

    def joinStrings(self, strings: list[str]) -> str:
        return "\n".join(strings)
