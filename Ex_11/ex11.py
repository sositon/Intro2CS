from collections import Counter
from itertools import combinations


class Node:
    def __init__(self, data, positive_child=None, negative_child=None):
        self.data = data
        self.positive_child = positive_child
        self.negative_child = negative_child

    def __eq__(self, other):
        """
        :param other: other Node object
        :return: True if both of the nodes have the same data through the
        all tree(nodes with children)
        """
        def check_eq(node1, node2):
            if node1.is_leaf_node() and node2.is_leaf_node():
                return node1.data == node2.data
            else:
                if node1.data != node2.data:
                    return False
                return check_eq(node1.positive_child, node2.positive_child) \
                    and check_eq(node1.negative_child, node2.negative_child)
        return check_eq(self, other)

    def is_leaf_node(self):
        """
        :return: True if a node is a leaf
        """
        if self.data is None:
            return True
        return self.positive_child is None and self.negative_child is None


class Record:
    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms


def parse_data(filepath):
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    def __init__(self, root):
        self.root = root

    def diagnose(self, symptoms):
        """
        :param symptoms: a list of str represent symptoms
        :return: the illness based on the symptoms
        """

        def diagnose_helper():
            """
            :return: the illness
            """
            node = self.root
            if node.is_leaf_node():
                return node.data
            self.root = node.positive_child if node.data in symptoms else \
                node.negative_child
            return self.diagnose(symptoms)
        # save the original root
        root = self.root
        diagnosis = diagnose_helper()
        self.root = root
        return diagnosis

    def calculate_success_rate(self, records):
        """
        :param records: a list of objects from type Record
        :return: return the success rate of a diagnoser object
        """
        if len(records) == 0:
            raise ValueError("Records list is empty")
        counter = 0
        for record in records:
            tmp_diagnosis = self.diagnose(record.symptoms)
            if tmp_diagnosis == record.illness:
                counter += 1
        return counter / len(records)

    def all_illnesses(self):
        """
        :return:a sorted list with all the illnesses in the tree descending
        """

        def all_illnesses_helper(node, arr=None):
            """
            :param node: a node object
            :param arr: a default list
            :return: a list with all occurrences of any illness without None.
            """
            arr = list() if arr is None else arr
            if node is not None:
                if node.data is not None and node.is_leaf_node():
                    arr.append(node.data)
                    return
                all_illnesses_helper(node.negative_child, arr)
                all_illnesses_helper(node.positive_child, arr)
            return arr

        res = all_illnesses_helper(self.root)
        res = Counter(res).most_common()
        return [tup[0] for tup in res]

    def paths_to_illness(self, illness):
        """
        :param illness: a string or None
        :return: list of paths to the illness
        """

        def paths_to_illness_helper(node, path=None, arr=None):
            """
            :param node: node object
            :param path: a list of True and False represent the path
            :param arr: a list of paths
            :return: the list arr with all the paths to illness
            """
            arr = list() if arr is None else arr
            path = list() if path is None else path
            if node is not None:
                if node.is_leaf_node() and node.data == illness:
                    arr.append(path)
                paths_to_illness_helper(node.positive_child, path + [True],
                                        arr)
                paths_to_illness_helper(node.negative_child, path + [False],
                                        arr)
                return arr

        return paths_to_illness_helper(self.root)

    def minimize(self, remove_empty=False):
        """
        :param remove_empty: a flag that changes the way of the function
        preform
        :return: None. minimize the root of a diagnoser object
        """
        def minimize_helper(node):
            """
            :param node: a node object
            :return: new node object, minimized.
            """
            if node.is_leaf_node():
                return node

            minimized_positive_subtree = \
                minimize_helper(node.positive_child)
            minimized_negative_subtree = \
                minimize_helper(node.negative_child)

            if remove_empty:
                if minimized_positive_subtree == Node(None):
                    return minimized_negative_subtree
                if minimized_negative_subtree == Node(None):
                    return minimized_positive_subtree

            if minimized_positive_subtree == minimized_negative_subtree:
                return minimized_positive_subtree

            return Node(node.data, minimized_positive_subtree,
                        minimized_negative_subtree)
        # function call
        self.root = minimize_helper(self.root)


def check_validation(lst, type):
    """
    :param lst: a list
    :param type: a type of object that the list should contain
    :return: True if all elements from type
    """
    for element in lst:
        if not isinstance(element, type):
            return False
    return True


def leaf_matching(records, pos_set, neg_set):
    """
    :param records: a list of records from type Record
    :param pos_set: positive symptoms set
    :param neg_set: negative symptoms set
    :return: the best option of an illness out of the parameters
    """
    res = []
    for record in records:
        symptoms_set = set(record.symptoms)
        if pos_set.issubset(symptoms_set):
            if len(neg_set.intersection(symptoms_set)) == 0:
                res.append(record.illness)
    res = Counter(res).most_common()
    res = [tup[0] for tup in res]
    return res[0] if res else None


def build_tree_helper(records, symptoms, node, positive_lst=None,
                      negative_lst=None):
    """
    :param records: a list of records
    :param symptoms: a list of symptoms
    :param node: node object
    :param positive_lst: symptoms that the answer is yes
    :param negative_lst: symptoms that the answer is no
    :return: a node, that will be the root for the diagnoser object
    """
    positive_lst = list() if positive_lst is None else positive_lst
    negative_lst = list() if negative_lst is None else negative_lst
    # break condition
    if len(symptoms) == 0:
        data = leaf_matching(records, set(positive_lst + [node.data]),
                             set(negative_lst))
        node.positive_child = Node(data)
        data = leaf_matching(records, set(positive_lst),
                             set(negative_lst + [node.data]))
        node.negative_child = Node(data)
    else:
        data = symptoms[0]
        node.positive_child = Node(data)
        node.negative_child = Node(data)
        build_tree_helper(records, symptoms[1:], node.positive_child,
                          positive_lst + [node.data], negative_lst)
        build_tree_helper(records, symptoms[1:], node.negative_child,
                          positive_lst, negative_lst + [node.data])


def build_tree(records, symptoms):
    """
    :param records: a list of objects from type Record
    :param symptoms: a list of strings that contains symptoms
    :return: a Diagnoser object with the tree we built as a root
    """
    if not check_validation(records, Record):
        raise TypeError(
            "not all of records list elements are from type Record")
    if not check_validation(symptoms, str):
        raise TypeError("not all of symptoms list elements are from type str")
    # check if symptoms is empty
    if len(symptoms):
        # init first Node
        node = Node(symptoms[0])
        # build tree
        build_tree_helper(records, symptoms[1:], node)
    else:
        node = Node(leaf_matching(records, set(), set()))
    return Diagnoser(node)


def optimal_tree(records, symptoms, depth):
    """
    :param records: a list of records
    :param symptoms: a list of symptoms
    :param depth: a number represent the size of the combinations to check
    :return: a diagnoser object with an optimized tree as root
    """
    # exceptions
    if not check_validation(records, Record):
        raise TypeError(
            "not all of records list elements are from type Record")
    if not check_validation(symptoms, str):
        raise TypeError("not all of symptoms list elements are from type str")
    if len(symptoms) != len(set(symptoms)):
        raise ValueError("symptoms list contain double symptom")
    if not 0 <= depth <= len(symptoms):
        raise ValueError("depth value is invalid")
    # build trees
    maximum_success_rate = 0
    result_tree = Diagnoser(Node(None))
    for symp_lst in combinations(symptoms, depth):
        temp_tree = build_tree(records, symp_lst)
        temp_success_rate = temp_tree.calculate_success_rate(records)
        if temp_success_rate >= maximum_success_rate:
            maximum_success_rate = temp_success_rate
            result_tree = temp_tree
    return result_tree


if __name__ == "__main__":

    # Manually build a simple tree.
    #                cough
    #          Yes /       \ No
    #        fever           healthy
    #   Yes /     \ No
    # influenza   cold

    flu_leaf = Node("influenza", None, None)
    cold_leaf = Node("cold", None, None)
    cold_leaf_2 = Node("cold", None, None)
    inner_vertex = Node("fever", flu_leaf, cold_leaf)
    healthy_leaf = Node("healthy", None, None)
    root = Node("cough", inner_vertex, healthy_leaf)

    diagnoser = Diagnoser(root)

    # Simple test 1
    diagnosis = diagnoser.diagnose(["cough"])
    print(diagnoser.root is root)
    if diagnosis == "cold":
        print("Test passed")
    else:
        print("Test failed. Should have printed cold, printed: ", diagnosis)

    # Simple test 2
    records_1 = [Record("healthy", [])]
    records_2 = []
    try:
        print(diagnoser.calculate_success_rate(records_1))
        print(diagnoser.calculate_success_rate(records_2))
    except ValueError as e:
        print(e)

    # Simple test 3
    print(diagnoser.all_illnesses())

    # Simple test 4
    print(diagnoser.paths_to_illness("cold"))
