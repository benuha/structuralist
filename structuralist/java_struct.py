"""
structuralist.java_struct

Copyright 2016 benuha
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
--------------------


Java class organize and structure diagram


--------------------
"""
from os import walk

from structuralist.java_interpreter import Interpreter


class JavaStruct:

    @staticmethod
    def make_uml_diagram_dir(file_name, m_list):
        """
        Create Plantuml class diagram code and save in a file under folder 'diagrams'
        :param file_name: save it under this file name
        :param m_list: the list of file paths inside a dir
        """
        sb = ['@startuml\n']
        workers = []
        for f_file in m_list:
            worker = Interpreter(f_file)
            sb.append(worker.get_class_content(object_declaration=True))
            workers.append(worker)

        # working on the relationship btw classes
        for i in range(0, len(workers)):
            for j in range(0, len(workers)):
                if i == j:
                    continue
                worker_1 = workers[i]
                worker_2 = workers[j]
                if worker_1._fields_.__contains__(worker_2._class_):
                    sb.append(worker_1._class_)
                    sb.append(' --> ')
                    sb.append(worker_2._class_)
                    sb.append('\n')

        sb.append('@enduml')

        with open('diagrams\\' + file_name + '.puml', 'w+') as f:
            for s in sb:
                f.write(s)

        pass

    # Make uml diagram for only file
    @staticmethod
    def make_uml_diagram(file_name, file_path):
        """
        Create Plantuml class diagram code from a java file and save it under folder 'diagrams'
        :param file_name: save it under this file name
        :param file_path: the java file path
        """
        sb = ['@startuml\n']
        worker = Interpreter(file_path)
        sb.append(worker.get_class_content(object_declaration=True))
        sb.append('@enduml')

        with open('diagrams\\' + file_name + '.puml', 'w+') as f:
            for s in sb:
                f.write(s)

        pass

    @staticmethod
    def draw_each_pkgs_diagrams(source_dir):
        """
        Create multiple Plantuml class diagram codes from java source project
        and save them to each file with name from java package folder
        under folder 'diagrams'
        :param source_dir: the java project source
        """
        # list all files in dir
        for (dir_path, dir_names, file_names) in walk(source_dir):
            dir_name = dir_path.split('\\')[-1]

            f = []
            for file_name in file_names:
                if file_name.endswith(".java"):
                    f.append(dir_path + "\\" + file_name)
            JavaStruct.make_uml_diagram_dir(dir_name, f)

    @staticmethod
    def draw_all_in_dir(save_name, source_dir):
        """
        Create Plantuml class diagram code from java source project
        and save it to a file named file_name under folder 'diagrams'
        :param save_name: name of the file to save diagram code
        :param source_dir: the java project source
        """
        f = []
        for (dir_path, dir_names, file_names) in walk(source_dir):
            for file_name in file_names:
                if file_name.endswith(".java"):
                    f.append(dir_path + "\\" + file_name)

        JavaStruct.make_uml_diagram_dir(save_name, f)

