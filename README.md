# structuralist
From java source code to PlantUML Class Diagram

This Program interpretes Java Project/Android Project source code and creates a PlantUML diagram code. 
Work best with JetBrains Pycharm.

Open source libs and usage
-------------

* [c2nes, javalang] [2] provides a lexer and parser targeting Java 8.


Prerequisites
-------------

* [Python 3.5] [1] this project compiled with python 3 but can be run with python 2.7 
* [Pycharm 5.0.4] [2] to run the python code and view diagrams
* [Plantuml] [3] to open the the generated diagram code

How to use
----------

1.  Make sure you have installed [Python 3.5] [1]

2.  Download the master.zip file and extract and locate to your extracted folder

3.  If you use [Pycharm] [2], install plugin PlantUML Integration for Pycharm

4.  Open the project folder, locate to 'structuralist/main.py' and specify your java project source dir. Run 'main.py', the program will create PlantUML Diagrams for java code under folder 'structuralist/diagrams'. You can view generated diagrams in PlanUML tab inside Pycharm 

License
----------
*Released under the Apache License Version 2.0 by benuha*

   [1]: https://www.python.org/downloads/
   [2]: https://github.com/c2nes/javalang
   [3]: http://plantuml.com/download
