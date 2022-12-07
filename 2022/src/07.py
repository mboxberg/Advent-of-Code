import numpy as np


class Folder:
    def __init__(self, name, parent=None):
        self.name = name
        self.items = dict()
        self.parent = parent

    @property
    def path(self):
        if self.parent:
            if self.parent.path == "/":
                return self.parent.path + self.name
            else:
                return self.parent.path + "/" + self.name
        else:
            return self.name

    @property
    def size(self):
        return self.get_size()

    def __getitem__(self, item):
        if item in self.items:
            return self.items[item]
        else:
            raise ValueError("'{}' not found in folder '{}'".format(item, self.path))

    def __add__(self, other):
        self.add_item(other)

    def add_item(self, item):
        if isinstance(item, Folder) or isinstance(item, File):
            self.items[item.name] = item
            item.parent = self
        else:
            raise TypeError("{} is not of Type 'Folder' or 'File'".format(item))

    def get_size(self):
        size = 0
        for item in self.items.values():
            size += item.size
        return size

    def get_contained_folders(self):
        folders = list()
        for item in self.items.values():
            if isinstance(item, Folder):
                folders.append(item)
                folders.extend(item.get_contained_folders())
        return folders

    def ls(self):
        for item in self.items:
            print("{} {}".format(self.items[item].size, self.items[item].name))

    def walk(self, level=0):
        print(" " * level + "- {} (dir)".format(self.name))
        for item in self.items.values():
            item.walk(level=level + 1)


class File:
    def __init__(self, name, size, parent=None):
        self.name = name
        self.size = size
        self.parent = parent

    def walk(self, level=0):
        print(" " * level + "- {} (file, size={})".format(self.name, self.size))


if __name__ == "__main__":
    readfiles = False
    main_directory = Folder("/")
    cwd = main_directory

    with open("../dat/07") as input_file:
        while True:
            line = input_file.readline()
            if not line:
                break

            command = line.split()

            if command[0] == "$":
                readfiles = False
                if command[1] == "cd":
                    if command[2] == "/":
                        cwd = main_directory
                    elif command[2] == "..":
                        cwd = cwd.parent
                    else:
                        cwd = cwd[command[2]]
                elif command[1] == "ls":
                    readfiles = True
            elif readfiles:
                if command[0] == "dir":
                    cwd.add_item(Folder(command[1]))
                else:
                    cwd.add_item(File(command[1], int(command[0])))

    main_directory.walk()

    size_sum = 0
    folders_in_main_directory = main_directory.get_contained_folders()
    for folder in folders_in_main_directory:
        size_sum += folder.size if folder.size <= 100000 else 0

    print("")
    print("The summed size of the small directories is {}.".format(size_sum))

    total_disk_space = 70000000
    space_needed_for_update = 30000000
    free_disk_space = total_disk_space - main_directory.get_size()
    space_needed_to_free = space_needed_for_update - free_disk_space

    print("")
    print("Total disk space: {:9d}".format(total_disk_space))
    print("Used disk space:  {:9d}".format(main_directory.get_size()))
    print("Free disk space:  {:9d}".format(free_disk_space))
    print("Update needs:     {:9d}".format(space_needed_for_update))
    print("Need to free:     {:9d}".format(space_needed_for_update - free_disk_space))
    print("")

    j = 0
    for i, folder in enumerate(folders_in_main_directory):
        if space_needed_to_free < folder.size < folders_in_main_directory[j].size:
            j = i
    print("We need to delete directory '{}' (size={}) to free enough space.".format(folders_in_main_directory[j].name,
                                                                                    folders_in_main_directory[j].size))
