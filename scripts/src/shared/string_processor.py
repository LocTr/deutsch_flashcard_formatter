

from dataclasses import dataclass
from enum import Enum

from scripts.src.models.base_elements import Node


class TokenType(Enum):
    DEFAULT = 1
    DIFF = 2

@dataclass
class TokenGroup:
    type: TokenType
    content: list[str]

class StringProcessor:

    @staticmethod
    def getDifferncedChars(base: str, diff: str) -> list[int]:
        diffChars: list[int] = []
        singularChar = base.strip()
        pluralChar = diff.strip()
        for i,value in enumerate(pluralChar):
            if i > len(singularChar)-1:
                diffChars.append(i)
            elif value != singularChar[i]:
                diffChars.append(i)
        return diffChars
    

    
    @staticmethod
    def combineToNodes(base: str, diff: list[int], defaultType : callable[[str], Node], diffType : callable[[str], Node]) -> list[Node]:

        # Assign each character a TokenType
        labeled: list[tuple[str, TokenType]] = []
        for i, value in enumerate(base.strip()):
            token_type = TokenType.DIFF if i in diff else TokenType.DEFAULT
            labeled.append((value, token_type))

        # Group adjacent characters with the same TokenType into TokenGroups
        groups: list[TokenGroup] = []
        for char, token_type in labeled:
            if groups and groups[-1].type == token_type:
                groups[-1].content.append(char)
            else:
                groups.append(TokenGroup(type=token_type, content=[char]))

        # Convert each TokenGroup into a Node
        nodes: list[Node] = []
        for group in groups:
            text = "".join(group.content)
            if group.type == TokenType.DIFF:
                nodes.append(diffType(text))
            else:
                nodes.append(defaultType(text))
        return nodes