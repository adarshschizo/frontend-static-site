# Frontend Static Site Generator

A custom static site generator built with Python as part of the Boot.dev Static Site Generator course.

This project converts Markdown files into HTML pages using a custom-built Markdown parser and HTML node system. It recursively generates pages while preserving the directory structure and can be deployed directly to GitHub Pages.

## Features

- Convert Markdown to HTML
- Headings (`#` through `######`)
- Paragraphs
- Bold text
- Italic text
- Inline code
- Code blocks
- Links
- Images
- Blockquotes
- Ordered lists
- Unordered lists
- Recursive Markdown page generation
- Recursive static asset copying
- HTML templates
- Configurable base path for deployment
- GitHub Pages deployment
- Automated testing with Python `unittest`

## Project Structure

```text
frontend-static-site/
├── content/
│   ├── index.md
│   ├── blog/
│   │   ├── glorfindel/
│   │   ├── majesty/
│   │   └── tom/
│   └── contact/
├── static/
│   ├── images/
│   └── index.css
├── src/
│   ├── block.py
│   ├── htmlnode.py
│   ├── leafnode.py
│   ├── main.py
│   ├── parentnode.py
│   ├── split_nodes.py
│   ├── textnode.py
│   └── test_*.py
├── docs/
├── template.html
├── main.sh
├── build.sh
├── test.sh
├── .gitignore
└── README.md