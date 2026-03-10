
from scripts.src.models.elements import Node, Text
from scripts.src.tasks.nomen_elements import FemininColor, MaskulinColor, NeutrumColor, PluralColor, SpanElement, SubtextElement
from scripts.src.tasks.string_processor import StringProcessor

class NomenTokenizer:

    def tokenizeEachLine(self, text: str) -> list[str]:
        lines = text.split("\n")
        return [line for line in lines if line.strip()]

    # Tokenize set (singular, plural, translation, sentence,tag) into Nodes
    @staticmethod
    def tokenizeToNode(text: str) -> list[Node]:

        nodes: list[Node] = []
        tokens = text.split(";")

        # First token is word in singular form

        
        # Check if there are enough tokens
        if len(tokens) < 5:
            raise ValueError("Not enough tokens to process noun phrase. Word cause: " + text)
        
        # First token is the noun
        noun = tokens.pop(0)
        singularToken = NomenTokenizer.tokenizeSingularCase(noun)
        nodes.append(SpanElement(singularToken))

        # Second token is the plural
        pluralNoun = tokens.pop(0)
        pluralToken = NomenTokenizer.tokenizePluralCase(pluralNoun, noun)
        nodes.append(SpanElement(pluralToken))

        # Third token is the translation
        translation = tokens.pop(0).strip()
        nodes.append([Text(translation)])

        # Fourth token is the example sentence
        sentence = tokens.pop(0).strip()
        nodes.append([Text(sentence)])
        # Fifth token is the tag
        tag = tokens.pop(0).strip()
        nodes.append(Text(tag))
        return nodes

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
        
