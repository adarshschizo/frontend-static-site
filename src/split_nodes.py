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
    pattern = r"(?<!!)\[([^\]]*)\]\(([^)]+)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        matches = extract_markdown_images(original_text)

        if not matches:
            new_nodes.append(old_node)
            continue

        remaining_text = original_text

        for alt_text, url in matches:
            image_markdown = f"![{alt_text}]({url})"

            parts = remaining_text.split(image_markdown, 1)

            before = parts[0]

            if before:
                new_nodes.append(
                    TextNode(before, TextType.TEXT)
                )

            new_nodes.append(
                TextNode(
                    alt_text,
                    TextType.IMAGE,
                    url,
                )
            )

            remaining_text = parts[1]

        if remaining_text:
            new_nodes.append(
                TextNode(
                    remaining_text,
                    TextType.TEXT,
                )
            )

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        matches = extract_markdown_links(original_text)

        if not matches:
            new_nodes.append(old_node)
            continue

        remaining_text = original_text

        for anchor_text, url in matches:
            link_markdown = f"[{anchor_text}]({url})"

            parts = remaining_text.split(link_markdown, 1)

            before = parts[0]

            if before:
                new_nodes.append(
                    TextNode(before, TextType.TEXT)
                )

            new_nodes.append(
                TextNode(
                    anchor_text,
                    TextType.LINK,
                    url,
                )
            )

            remaining_text = parts[1]

        if remaining_text:
            new_nodes.append(
                TextNode(
                    remaining_text,
                    TextType.TEXT,
                )
            )

    return new_nodes