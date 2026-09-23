import os
import shutil

from block import markdown_to_html_node


def copy_static_to_public(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)

    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            print(f"Copying {source_path} -> {destination_path}")
            shutil.copy(source_path, destination_path)
        else:
            copy_static_to_public(source_path, destination_path)


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("No h1 header found")


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} "
        f"to {dest_path} using {template_path}"
    )

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)

    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(full_html)


def main():
    copy_static_to_public("static", "public")

    generate_page(
        "content/index.md",
        "template.html",
        "public/index.html",
    )


if __name__ == "__main__":
    main()