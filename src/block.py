from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    result = []

    for block in blocks:
        block = block.strip()

        if block == "":
            continue

        result.append(block)

    return result


def block_to_block_type(block):
    # Heading
    for i in range(1, 7):
        prefix = "#" * i + " "

        if block.startswith(prefix):
            return BlockType.HEADING

    # Code block
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    # Quote block
    lines = block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list
    if all(
        line.startswith(f"{i}. ")
        for i, line in enumerate(lines, start=1)
    ):
        return BlockType.ORDERED_LIST

    # Default
    return BlockType.PARAGRAPH