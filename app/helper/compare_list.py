import collections
class CompareList:
    def __init__(self, list1: list, list2: list) -> None:
        self.list1 = list1
        self.list2 = list2

    def compare_and_remove_commons(self):
        common_elements = list(set(self.list1).intersection(self.list2))
        final_list = self.list1.copy()
        if collections.Counter(common_elements) == collections.Counter(self.list1):
            return None
        elif len(common_elements) > 0:
            for i in common_elements:
                final_list.remove(i)
            return final_list
        elif len(common_elements) == 0:
            return final_list
