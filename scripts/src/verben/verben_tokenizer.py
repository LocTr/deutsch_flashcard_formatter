from scripts.src.models.base_elements import Node, Text
from scripts.src.models.elements import HighlightColor, SpanElement, SubtextElement
from scripts.src.verben.verben import Verben


class VerbenTokenizer:

    @staticmethod
    def tokenizeEachLine(text: str) -> list[str]:
        lines = text.split("\n")
        return [line for line in lines if line.strip()]
    
    @staticmethod
    def parseToVerb(text: str) -> Verben:
        tokens = [t.strip() for t in text.split(";")]

        if len(tokens) < 10:
            raise ValueError("Not enough tokens to process verb. Line: " + text)

        return Verben(
            base_word=tokens[0],
            conjugation_ich=tokens[1],
            conjugation_du=tokens[2],
            conjugation_er_sie_es=tokens[3],
            conjugation_wir=tokens[4],
            conjugation_ihr=tokens[5],
            conjugation_sie_sie=tokens[6],
            translationEn=tokens[7],
            translationVi=tokens[8],
            sample_sentence=tokens[9]
        )

    @staticmethod
    def verbenToNodes(verb: Verben) -> list[Node]:
        """Convert Verben dataclass to Node list for HTML rendering."""
        def conjugated(person: str, word: str) -> Node:
            return SpanElement([
                SubtextElement([Text(person)]),
                Text(" "),
                HighlightColor([Text(word)]),
            ])

        return [
            Text(verb.base_word),                          # base_word
            conjugated("ich", verb.conjugation_ich),       # ich
            conjugated("du", verb.conjugation_du),         # du
            conjugated("er/sie/es", verb.conjugation_er_sie_es),  # er/sie/es
            conjugated("wir", verb.conjugation_wir),       # wir
            conjugated("ihr", verb.conjugation_ihr),       # ihr
            conjugated("Sie/sie", verb.conjugation_sie_sie),  # Sie/sie
            Text(verb.translationEn),                      # translationEn
            Text(verb.translationVi),                      # translationVi
            Text(verb.sample_sentence),                    # sentence
            Text("Verben"),                                # tag
        ]
