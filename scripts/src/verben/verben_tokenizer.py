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
        def conjugated(person: str, word: str, base: str) -> Node:
            # Separable verb (e.g. base="aus·sehen", word="siehst aus")
            if '·' in base:
                _, stem_word = base.split('·', 1)
                if stem_word.endswith("en"):
                    stem = stem_word[:-2]
                elif stem_word.endswith("n"):
                    stem = stem_word[:-1]
                else:
                    stem = stem_word

                # Split conjugated form: "machst auf" → conj_word="machst", conj_prefix="auf"
                conj_word, conj_prefix = (word.rsplit(' ', 1) if ' ' in word else (word, ''))

                common_len = 0
                for i in range(min(len(stem), len(conj_word))):
                    if stem[i] == conj_word[i]:
                        common_len += 1
                    else:
                        break

                verbstamm = conj_word[:common_len]
                endung = conj_word[common_len:]

                word_parts: list[Node] = []
                if verbstamm:
                    word_parts.append(Text(verbstamm))
                if endung:
                    word_parts.append(HighlightColor([Text(endung)]))
                else:
                    word_parts.append(Text(conj_word))
                if conj_prefix:
                    word_parts.append(Text(' '))
                    word_parts.append(HighlightColor([Text(conj_prefix)]))

                return SpanElement([
                    SubtextElement([Text(person)]),
                    Text(" "),
                    *word_parts,
                ])

            # Non-separable verb: derive stem from infinitive (strip -en or -n)
            if base.endswith("en"):
                stem = base[:-2]
            elif base.endswith("n"):
                stem = base[:-1]
            else:
                stem = base

            # Find longest common prefix between stem and conjugated form
            common_len = 0
            for i in range(min(len(stem), len(word))):
                if stem[i] == word[i]:
                    common_len += 1
                else:
                    break

            verbstamm = word[:common_len]
            endung = word[common_len:]

            word_parts: list[Node] = []
            if verbstamm:
                word_parts.append(Text(verbstamm))
            if endung:
                word_parts.append(HighlightColor([Text(endung)]))
            else:
                # No suffix change — highlight nothing, just show the word as-is
                word_parts.append(Text(word))

            return SpanElement([
                SubtextElement([Text(person)]),
                Text(" "),
                *word_parts,
            ])

        return [
            Text(verb.base_word),                          # base_word
            conjugated("ich", verb.conjugation_ich, verb.base_word),       # ich
            conjugated("du", verb.conjugation_du, verb.base_word),         # du
            conjugated("er/sie/es", verb.conjugation_er_sie_es, verb.base_word),  # er/sie/es
            conjugated("wir", verb.conjugation_wir, verb.base_word),       # wir
            conjugated("ihr", verb.conjugation_ihr, verb.base_word),       # ihr
            conjugated("Sie/sie", verb.conjugation_sie_sie, verb.base_word),  # Sie/sie
            Text(verb.translationEn),                      # translationEn
            Text(verb.translationVi),                      # translationVi
            Text(verb.sample_sentence),                    # sentence
            Text("Verben"),                                # tag
        ]
