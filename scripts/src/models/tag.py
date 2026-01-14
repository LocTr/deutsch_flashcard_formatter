class Tag:
    def __init__(self, content: str, tag: str, attributes: str):
        self.content = content
        self.tag = tag
        self.attributes = attributes

    def toHtml(self) -> str:
        return f"<{self.tag} {self.attributes}>{self.content}</{self.tag}>"

class Color(Tag):
    r: int
    g: int
    b: int

    def __init__(self, content: str, r: int, g: int, b: int):
        super().__init__(content, "span", f'style="color: rgb({r}, {g}, {b});"')

class SubTextTag(Tag):
    def __init__(self, content: str):
        super().__init__(content, "sub", "")