from scripts.src.models.base_elements import Node, Text
from scripts.src.models.elements import HighlightColor, SpanElement, SubtextElement


class VerbenTokenizer:

    def tokenizeEachLine(self, text: str) -> list[str]:
        lines = text.split("\n")
        return [line for line in lines if line.strip()]

    @staticmethod
    def tokenizeToNode(text: str) -> list[Node]:
        tokens = [t.strip() for t in text.split(";")]

        if len(tokens) < 10:
            raise ValueError("Not enough tokens to process verb. Line: " + text)

        def conjugated(person: str, word: str) -> Node:
            return SpanElement([
                SubtextElement([Text(person)]),
                Text(" "),
                HighlightColor([Text(word)]),
            ])

        return [
            Text(tokens[0]),                          # base_word
            conjugated("ich", tokens[1]),             # ich
            conjugated("du", tokens[2]),              # du
            conjugated("er/sie/es", tokens[3]),       # er/sie/es
            conjugated("wir", tokens[4]),             # wir
            conjugated("ihr", tokens[5]),             # ihr
            conjugated("Sie/sie", tokens[6]),         # Sie/sie
            Text(tokens[7]),                          # translationEn
            Text(tokens[8]),                          # translationVi
            Text(tokens[9]),                          # sentence
            Text("Verben"),                           # tag
        ]
