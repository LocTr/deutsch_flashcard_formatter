

class NomenCompiler:

    def compileNodeToString(self, node) -> str:
        return f"{node.singular}\t{node.plural}\t{node.translation}\t{node.sentence}\t{node.tag}"
    def joinStrings(self, strings: list[str]) -> str:
        return "\n".join(strings)