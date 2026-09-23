from enum import Enum

from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType
from textnode import text_node_to_html_node
from textnode import text_to_textnodes


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

    lines = block.split("\n")

    # Quote
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

    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)

    children = []

    for text_node in text_nodes:
        children.append(
            text_node_to_html_node(text_node)
        )

    return children


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        # Paragraph
        if block_type == BlockType.PARAGRAPH:
            paragraph_text = " ".join(block.split("\n"))

            children = text_to_children(paragraph_text)

            block_node = ParentNode(
                "p",
                children,
            )

            block_nodes.append(block_node)

        # Heading
        elif block_type == BlockType.HEADING:
            first_space = block.find(" ")
            heading_level = first_space

            heading_text = block[first_space + 1:]

            children = text_to_children(heading_text)

            block_node = ParentNode(
                f"h{heading_level}",
                children,
            )

            block_nodes.append(block_node)

        # Code
        # Code
        elif block_type == BlockType.CODE:
            code_text = block[4:-3]

            code_node = ParentNode(
                "code",
                [LeafNode(None, code_text)],
            )

            pre_node = ParentNode(
                "pre",
                [code_node],
            )

            block_nodes.append(pre_node)

        # Quote
        elif block_type == BlockType.QUOTE:
            quote_lines = []

            for line in block.split("\n"):
                quote_lines.append(line[1:].lstrip())

            quote_text = " ".join(quote_lines)

            children = text_to_children(quote_text)

            block_node = ParentNode(
                "blockquote",
                children,
            )

            block_nodes.append(block_node)

        # Unordered list
        elif block_type == BlockType.UNORDERED_LIST:
            list_items = []

            for line in block.split("\n"):
                item_text = line[2:]

                children = text_to_children(item_text)

                list_item = ParentNode(
                    "li",
                    children,
                )

                list_items.append(list_item)

            block_node = ParentNode(
                "ul",
                list_items,
            )

            block_nodes.append(block_node)

        # Ordered list
        elif block_type == BlockType.ORDERED_LIST:
            list_items = []

            for line in block.split("\n"):
                first_space = line.find(" ")
                item_text = line[first_space + 1:]

                children = text_to_children(item_text)

                list_item = ParentNode(
                    "li",
                    children,
                )

                list_items.append(list_item)

            block_node = ParentNode(
                "ol",
                list_items,
            )

            block_nodes.append(block_node)

    return ParentNode(
        "div",
        block_nodes,
    )