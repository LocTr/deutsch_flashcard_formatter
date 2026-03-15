from dataclasses import dataclass


@dataclass
class Nomen:
	word_singular: str
	word_plural: str
	translationEn: str
	translationVi: str
	sample_sentence: str