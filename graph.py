from data_io import *


class Node:

    def __init__(self, index, title):
        self.__index = index
        self.__title = title
        self.__pre_node = []
        self.__after_node = []
        self.checked = False

    def get_index(self):
        return self.__index

    def get_title(self):
        return self.__title

    def get_pre_node(self):
        return self.__pre_node

    def get_after_node(self):
        return self.__after_node

    def insert_pre_node(self, pre_node_index):
        self.__pre_node.append(pre_node_index)

    def insert_after_node(self, after_node_index):
        self.__after_node.append(after_node_index)

    def remove_pre_node(self, pre_node_index):
        self.__pre_node.remove(pre_node_index)


class Graph:

    def __init__(self, info_list, graph_type='Orthogonal List'):
        if graph_type == 'Orthogonal List':
            self.graph = OrthogonalList(info_list)

    def print(self):
        self.graph.print()

    def get_stage(self):
        return self.graph.get_stage(update=True)


class OrthogonalList:

    def __init__(self, info_list):
        self.node_list = []
        self.index_dict = {}
        self.stage_list = []
        self.node_list_copy = None
        for info_node in info_list:
            if self.__find_node(info_node.title) < 0:
                self.add_node(info_node.title)
            current_index = self.__find_node(info_node.title)
            for pre_node_title in info_node.pre_node_titles:
                index = self.__find_node(pre_node_title)
                if index < 0:
                    self.add_node(pre_node_title)
                    self.node_list[-1].insert_after_node(current_index)
                else:
                    self.node_list[index].insert_after_node(current_index)
                self.node_list[current_index].insert_pre_node(index)

    def add_node(self, title):
        self.node_list.append(Node(len(self.node_list), title))
        self.index_dict[title] = len(self.node_list) - 1
        pass

    def add_arc(self, tail_title, head_title):
        tail_index = self.index_dict[tail_title]
        head_index = self.index_dict[head_title]
        self.node_list[tail_index].insert_after_node(head_index)
        self.node_list[head_index].insert_pre_node(tail_index)

    def print(self):
        for node in self.node_list:
            print(node.get_index(), node.get_title(), node.get_pre_node(), node.get_after_node())

    def update_stage(self):
        self.stage_list = []
        self.node_list_copy = self.node_list[:]
        stage = self.__find_no_in_node()
        while stage:
            self.stage_list.append(stage)
            self.__remove_in_arc(stage)

            stage = self.__find_no_in_node()

    def get_stage(self, update=False):
        if update:
            self.update_stage()
        return self.stage_list

    def __find_node(self, title):
        try:
            index = self.index_dict[title]
            return index
        except KeyError:
            return -1

    def __find_no_in_node(self):
        temp_list = []
        for node in self.node_list_copy:
            if not node.get_pre_node() and not node.checked:
                temp_list.append(node.get_index())
                node.checked = True
        return temp_list

    def __remove_in_arc(self, index_list):
        for index in index_list:
            for node_index in self.node_list_copy[index].get_after_node():
                self.node_list_copy[node_index].remove_pre_node(index)


course_list = load_data_xml('resource/data/data_1.xml')
graph = Graph(course_list)
print(graph.get_stage())
graph.print()
