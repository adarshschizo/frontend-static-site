from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType,
) -> list[TextNode]:

    new_nodes = []

    for old_node in old_nodes:
        # Only split TEXT nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        sections = old_node.text.split(delimiter)

        # Delimiters must come in pairs
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