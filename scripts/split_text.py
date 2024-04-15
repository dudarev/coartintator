"""
Read text from file and split it into sections.
Sections are such that they contain at most `max_words` words.
Or if adding the next line would exceed `max_words`, then the next line is added to the next section.
"""


class LineTooLong(ValueError):
    pass


def count_words(line: str) -> int:
    return len(line.split())


class LinesContainer(list):
    def __init__(self, max_words: int = None, lines: list = None):
        self.max_words = max_words
        self.n_words = 0
        if lines:
            for line in lines:
                self.append(line)

    def append(self, line):
        if len(self) == 0:
            super().append(line)
            self.n_words = count_words(line)
        elif self.max_words is None:
            super().append(line)
            self.n_words += count_words(line)
        else:
            if self.n_words + count_words(line) <= self.max_words:
                super().append(line)
                self.n_words += count_words(line)
            else:
                raise LineTooLong()

    def __repr__(self) -> str:
        return "".join(self)


def split_text(lines: LinesContainer, max_words):
    section = LinesContainer(max_words)
    for line in lines:
        try:
            section.append(line)
        except LineTooLong:
            yield section
            section = LinesContainer(max_words, [line])


FILENAME = "out.txt"
MAX_WORDS = 500


with open(FILENAME, "r") as f:
    lines = LinesContainer(None, f.readlines())
    sections_counter = 0
    for section in split_text(lines, MAX_WORDS):
        sections_counter += 1
        print(section)
        print()

    print(f"Number of sections: {sections_counter}")
