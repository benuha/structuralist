from os import walk

from structuralist.java_struct import JavaStruct

source_dir = 'D:\\MyProjects\\PycharmProjects\\StructuralistPython\\javaxampleapp'


if __name__ == '__main__':
    f = []
    for (dir_path, dir_names, file_names) in walk(source_dir):
        for file_name in file_names:
            if file_name.endswith(".java"):
                f.append(dir_path + "\\" + file_name)

    for s in f:
        print(s, end='\n')
    JavaStruct.draw_all_in_dir('home_graph', source_dir)

    pass
