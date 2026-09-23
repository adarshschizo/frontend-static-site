import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType,
) -> list[TextNode]:

    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        sections = old_node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError(
                f"Invalid Markdown syntax: unclosed delimiter '{delimiter}'"
            )

        for i, section in enumerate(sections):
            if section == "":
                continue

            if i % 2 == 0:
                new_nodes.append(
                    TextNode(section, TextType.TEXT)
                )
            else:
                new_nodes.append(
                    TextNode(section, text_type)
                )

    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    pattern = r"(?<!!) \[([^\]]*)\]\(([^)]+)\)"
    return re.findall(pattern, text)