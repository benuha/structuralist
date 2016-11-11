"""
structuralist.java_interpreter

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


This class will translate the result of parsing java source code
to Plantuml code to express it in diagram


--------------------
"""

from javalang import parse
from pkg_resources import resource_string

from javalang.tree import ReferenceType, TypeArgument, \
    InterfaceDeclaration, BasicType, FieldDeclaration, \
    MethodDeclaration, ClassDeclaration


class Interpreter:
    def __init__(self, path):
        self._path_ = path
        source = resource_string(__name__, path)
        self.ast = parse.parse(source)
        self._class_ = ''
        self._fields_ = []

    def get_class_content(self, object_declaration):
        """
        Starting point; the method traverse through the body of class file
        and address its methods, object declarations, object types
        :param object_declaration:
        :return:
        """

        sb = []
        for m in self.ast.types:
            try:
                sb.append(self.get_class_declaration("", m, object_declaration))
            except AttributeError as e:
                print('get_class_content error', self._path_, e)
                continue

        return ''.join(sb)

    def get_class_declaration(self, parent_name, t, object_declaration):
        sb = []
        try:
            if not self._class_:
                self._class_ = t.name

            if type(t) == InterfaceDeclaration:
                has_method = False
                if t.methods:
                    has_method = True
                    sb.append(self.get_interface_declaration(parent_name, t))
                sb.append(self.get_declaration(has_method, t.name, t, object_declaration))
            else:
                sb.append('class ')
                if parent_name:
                    sb.append(parent_name)
                    sb.append('.')
                sb.append(t.name)
                sb.append(self.get_declaration(True, "", t, object_declaration))

        except AttributeError as e:
            print('get_declaration failed ', self._path_, '\n', e)
        return ''.join(sb)

    def get_declaration(self, has_method, parent_name, t, object_declaration):
        sb = []
        try:
            if t.attrs.__contains__('extends'):
                if t.extends:
                    sb.append(' extends ')
                    sb.append(self.get_object_type(t.extends, with_args = False))

            if object_declaration:
                if has_method:
                    sb.append('{')
                    sb.append('\n')
                sb.append(self.get_class_body_declarations(t.body))
                if has_method:
                    sb.append('}')
                    sb.append('\n')
                sb.append(self.get_type_declaration(parent_name, t.body, object_declaration))

            if t.attrs.__contains__('implements'):
                sb.append(self.get_class_implements(t.name, t.implements))

        except AttributeError as e:
            print('get_declaration failed ', self._path_, '\n', e)
        return ''.join(sb)

    def get_class_body_declarations(self, body):
        sb = []
        try:
            if body:
                for m in body:
                    if type(m) == FieldDeclaration:
                        sb.append(self.get_field_declarations(m))
                    elif type(m) == MethodDeclaration:
                        sb.append(self.get_method_declarations(m))
        except AttributeError as e:
            print('body_declaration failed ', self._path_, '\n', e)
        return ''.join(sb)

    def get_type_declaration(self, parent_name, body, object_declaration):
        sb = []
        try:
            if body:
                for m in body:
                    if type(m) == InterfaceDeclaration:
                        sb.append(self.get_interface_declaration(parent_name, m))
                        has_method = False
                        if m.methods:
                            has_method = True
                        sb.append(self.get_declaration(has_method, parent_name, m, object_declaration))
                    elif type(m) == ClassDeclaration:
                        sb.append(self.get_class_declaration(parent_name, m, object_declaration))
        except AttributeError as e:
            print('get_class_content error', self._path_, e)

        return ''.join(sb)

    def get_interface_declaration(self, parent_name, m_interface):
        sb = []
        try:
            sb.append('interface ')
            if parent_name:
                sb.append(parent_name)
                sb.append('.')
            sb.append(m_interface.name)

        except AttributeError as e:
            print('interface_declaration error', self._path_, e)
        return ''.join(sb)

    def get_field_declarations(self, f):
        sb = []
        try:
            if f.modifiers:
                sb.append(self.get_object_modifier(f.modifiers))

            self._fields_.append(f.type.name)
            sb.append(f.type.name)
            if type(f.type) == ReferenceType:
                if f.type.sub_type:
                    sb.append('.')
                    sb.append(f.type.sub_type.name)
                if f.type.arguments:
                    sb.append(self.get_type_args(f.type.arguments))
            sb.append(' ')
            sb.append(f.declarators[0].name)
            sb.append('\n')
        except AttributeError as e:
            print('field_declaration error', self._path_, e)

        return ''.join(sb)

    def get_method_declarations(self, m):
        sb = []
        try:
            if m.modifiers:
                sb.append(self.get_object_modifier(m.modifiers))
            sb.append(m.name)
            sb.append('(')
            if m.parameters:
                for parameter in m.parameters:
                    sb.append(self.get_method_parameter(parameter))
            sb.append(')')

            if m.return_type:
                sb.append(': ')
                sb.append(self.get_object_type(m.return_type))
            else:
                sb.append(': Void')
            sb.append('\n')
        except AttributeError as e:
            print('method_declarations failed ', self._path_,  e)
        return ''.join(sb)

    def get_method_parameter(self, parameter):
        sb = []
        try:
            if parameter:
                if parameter.type:
                    sb.append(self.get_object_type(parameter.type))
                    sb.append(' ')
                sb.append(parameter.name)

        except AttributeError as e:
            print('get_method_parameter failed', self._path_, e)
        return ''.join(sb)

    def get_object_type(self, m_type, with_args=True):
        sb = []
        try:
            if m_type:
                if type(m_type) == BasicType:
                    sb.append(m_type.name)
                elif type(m_type) == ReferenceType:
                    sb.append(m_type.name)
                    if m_type.sub_type:
                        sb.append('.')
                        sb.append(m_type.sub_type.name)
                    if with_args:
                        if m_type.arguments:
                            sb.append(self.get_type_args(m_type.arguments))
                else:
                    for m in m_type:
                        if type(m) == ReferenceType:
                            sb.append(m.name)
                            if m.sub_type:
                                sb.append('.')
                                sb.append(m.sub_type.name)
                            if with_args:
                                if m.arguments:
                                    sb.append(self.get_type_args(m.arguments))
        except AttributeError as e:
            print('get_object_type failed', self._path_, e)
        return ''.join(sb)

    def get_type_args(self, f):
        sb = ['<']
        try:
            for indx in range(0, len(f)-1):
                type_arg = f[indx]
                if type(type_arg) == TypeArgument:
                    if type_arg.type:
                        sb.append(type_arg.type.name)

                    if type(type_arg.type) == ReferenceType:
                        if type_arg.type.sub_type:
                            sb.append('.')
                            sb.append(type_arg.type.sub_type.name)

                    sb.append(', ')

            type_arg = f[len(f)-1]
            if type(type_arg) == TypeArgument:
                if type_arg.type:
                    sb.append(type_arg.type.name)

                if type(type_arg.type) == ReferenceType:
                    if type_arg.type.sub_type:
                        sb.append('.')
                        sb.append(type_arg.type.sub_type.name)

                if type_arg.type:
                    if type_arg.type.arguments:
                        sb.append(self.get_type_args(type_arg.type.arguments))

        except AttributeError as e:
            print('get_type_args failed', self._path_, e)
        sb.append('>')
        return ''.join(sb)

    @staticmethod
    def get_object_modifier(modifiers):
        modifr = str(modifiers)
        if modifr.__contains__('private'):
            return '-'
        elif modifr.__contains__('public'):
            return '+'
        else:
            return '#'
        pass

    @staticmethod
    def get_class_implements(class_name, implements):
        sb = []
        if implements:
            for i in implements:
                try:
                    if i:
                        sb.append(class_name)
                        sb.append(' ..|> ')
                        for x in i.children:
                            if x:
                                if type(x) == ReferenceType:
                                    sb.append('.')
                                    sb.append(x.name)
                                elif type(x) == str:
                                    sb.append(x)
                        sb.append('\n')
                except AttributeError as e:
                    print('get_class_implements failed', class_name, e)
                    continue

        return ''.join(sb)
