
from scripts.src.models.base_elements import Node, Text
from scripts.src.models.elements import FemininColor, MaskulinColor, NeutrumColor, PluralColor, SpanElement, SubtextElement
from scripts.src.shared.string_processor import StringProcessor
from scripts.src.nomen.nomen import Nomen


class NomenTokenizer:

    def tokenizeEachLine(self, text: str) -> list[str]:
        lines = text.split("\n")
        return [line for line in lines if line.strip()]

    @staticmethod
    def parseToNomen(text: str) -> Nomen:
        """Parse semicolon-separated string to Nomen dataclass."""
        tokens = [t.strip() for t in text.split(";")]

        if len(tokens) < 6:
            raise ValueError("Not enough tokens to process noun phrase. Line: " + text)

        return Nomen(
            word_singular=tokens[0],
            word_plural=tokens[1],
            translationEn=tokens[2],
            translationVi=tokens[3],
            sample_sentence=tokens[4]
        )

    @staticmethod
    def nomenToNodes(nomen: Nomen) -> list[Node]:
        """Convert Nomen dataclass to Node list for HTML rendering."""
        # Process singular
        singularToken = NomenTokenizer.tokenizeSingularCase(nomen.word_singular)
        singular_node = SpanElement(singularToken)

        # Process plural
        pluralToken = NomenTokenizer.tokenizePluralCase(nomen.word_plural, nomen.word_singular)
        plural_node = SpanElement(pluralToken)

        return [
            singular_node,                 # singular form with color
            plural_node,                   # plural form with color
            Text(nomen.translationEn),     # English translation
            Text(nomen.translationVi),     # Vietnamese translation
            Text(nomen.sample_sentence),   # sentence
            Text("Nomen"),                 # tag
        ]

    @staticmethod
    def tokenizeSingularCase(text: str) -> list[Node]:

        text = text.strip()

        node: list[Node] = []
        node.append(SubtextElement([Text("sg")]))
        node.append(Text(" "))

        if text == "-":
            node.append(Text("-"))
            return node
        
        tokens = text.split(None, 1)  # Split into article and the noun
        if len(tokens) < 2:
            raise ValueError("Not enough tokens to process. Word cause: " + text)

        article = tokens[0]
        noun = tokens[1]
        node.append(Text(article + " "))

        match article:
            case "der":
                node.append(MaskulinColor([Text(noun)]))
            case "die":
                node.append(FemininColor([Text(noun)]))
            case "das":
                node.append(NeutrumColor([Text(noun)]))
            case _:
                raise ValueError("Unknown article: " + article + " in word cause: " + text)
        return node
    
    @staticmethod
    def tokenizePluralCase(text: str, singularText: str) -> list[Node]:
        
        text = text.strip()

        node: list[Node] = []
        node.append(SubtextElement([Text("pl")]))
        node.append(Text(" "))


        if text == "-":
            node.append(Text("-"))
            return node
        
        tokens = text.split(None, 1)  # Split into article and the noun

        if len(tokens) < 2:
            raise ValueError("Not enough tokens to process. Word cause: " + text)
        
        article = tokens[0]
        noun = tokens[1]

        if article != "die":
             raise ValueError("Plural article must be 'die', found: " + article + " in word cause: " + text)

        node.append(Text(article + " "))

        # If singular doesn't exist keep it as is
        if singularText.strip() == "-":
            node.append(Text(noun))
        # If singular exists, compare and decorate only changed chars
        else:
            singularNoun = singularText.strip().split(None, 1)[1]  # Remove article from singular noun
            diffChars = StringProcessor.getDifferncedChars(singularNoun, noun)
            node.extend(StringProcessor.combineToNodes(noun, diffChars, lambda t: Text(t), lambda t: PluralColor([Text(t)])))
                    
        return node   
        
