from __future__ import annotations
from typing import Dict, List
from dataclasses import dataclass
from abc import ABC, abstractmethod

class Node(ABC):
    @abstractmethod
    def to_html(self) -> str:
        pass

@dataclass
class Element(Node):
    tag: str
    attributes: Dict[str, str]
    children: List[Node]

    def to_html(self) -> str:
        attributes_str = ' '.join(f'{key}="{value}"' for key, value in self.attributes.items())
        opening_tag = f"<{self.tag} {attributes_str}>".strip()
        children_html = ''.join(child.to_html() for child in self.children)
        closing_tag = f"</{self.tag}>"
        return f"{opening_tag}{children_html}{closing_tag}"



@dataclass
class Text(Node):
    content: str

    def to_html(self) -> str:
        return self.content