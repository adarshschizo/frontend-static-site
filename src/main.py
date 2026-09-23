import os
import shutil


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


def main():
    source = "static"
    destination = "public"

    copy_static_to_public(source, destination)


if __name__ == "__main__":
    main()
