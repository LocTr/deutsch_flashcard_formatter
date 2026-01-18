from scripts.src.models.elements import Element, Node

class SpanElement(Element):
    def __init__(self, children: list[Node], style: str | None = None):
        super().__init__(
            tag="span",
            attributes={"style": style} if style is not None else {},
            children=children
        )

class ColorElement(Element):
    def __init__(self, children: list[Node], r: int, g: int, b: int):
        style = f"color: rgb({r}, {g}, {b});"
        super().__init__(
            tag="span",
            attributes={"style": style},
            children=children
        )

class MaskulinColor(ColorElement):
    def __init__(self, children: list[Node]):
        super().__init__(children, 138, 207, 255)
class FemininColor(ColorElement):
    def __init__(self, children: list[Node]):
        super().__init__(children, 255, 138, 138)
class NeutrumColor(ColorElement):
    def __init__(self, children: list[Node]):
        super().__init__(children, 138, 255, 138)
class PluralColor(ColorElement):
    def __init__(self, children: list[Node]):
        super().__init__(children, 255, 140, 0)


class _SubtextColor(ColorElement):
    def __init__(self, children: list[Node]):
        super().__init__(children, 181, 181, 181)

class SubtextElement(Element):
    def __init__(self, children: list[Node]):
        super().__init__(
            tag="small",
            children=[_SubtextColor(children)]
        )
class LineBreakElement(Element):
    def __init__(self):
        super().__init__(
            tag="br",
            attributes={},
            children=[]
        )
