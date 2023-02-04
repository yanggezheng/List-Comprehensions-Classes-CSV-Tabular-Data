import nelta as nt
class LabeledList:
    def __init__(self, data=None, index=None):
        if index is None:
            index = list(range(len(data)))
        self.values = data
        self.index = index

    def __str__(self):
        s = ''
        max_len = max([len(str(label)) for label in self.index])
        vals_max_len = max([len(str(v)) for v in self.values])
        format_spec = f'>{max_len}'
        for index, data in zip(self.index, self.values):
            s += f'{index:{format_spec}} {str(data):>{vals_max_len}}\n'
        return s

    def __iter__(self):
        return iter(self.values)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, scalar):
        if self.index:
            return LabeledList([v == scalar for v in self.values], self.index)
        else:
            return LabeledList([v == scalar for v in self.values])

    def __ne__(self, scalar):
        if self.index:
            return LabeledList([v != scalar for v in self.values], self.index)
        else:
            return LabeledList([v != scalar for v in self.values])

    def __gt__(self, scalar):
        if self.index:
            return LabeledList([v > scalar if v is not None else False for v in self.values], self.index)
        else:
            return LabeledList([v > scalar if v is not None else False for v in self.values])

    def __lt__(self, scalar):
        if self.index:
            return LabeledList([v < scalar if v is not None else False for v in self.values], self.index)
        else:
            return LabeledList([v < scalar if v is not None else False for v in self.values])

    def map(self, f):
        values = [f(val) if val is not None else None for val in self.values]
        return LabeledList(values, self.index)

    def __getitem__(self, key_list):
        # try our best to make list of keys:

        # 1. first, if it's a labeled list, use the labeled list's 
        #    values property as the list of keys
        if isinstance(key_list, LabeledList):
            key_list = key_list.values

        # 2. at this point, if we still don't have a list, then assume we 
        #    have a non-sequence type, and wrap in a list
        if not isinstance(key_list, list):
            key_list = [key_list]

        # now that we definitely have a list... check if it's only
        # booleans; one way to do this is filter for only boolean values
        # and check the length against the original unfiltered list
        if len([v for v in key_list if type(v) is bool]) == len(key_list):
            # we have a bunch of booleans, keep only the values that
            # have the same label as the labels that have true
            return self.__filter(key_list) 
        else:
            # we have a bunch of keys... so get all values with a matching
            # label / key
            index = [] # labels for returned LabeledList
            data = []  # values for returned LabeledList
            for key in key_list: 
                # find key matches, and get back both the label and value
                for label, val in self.__find(key):
                    index.append(label)
                    data.append(val)
            return data[0] if len(data) == 1 else LabeledList(data, index)

    def __filter(self, filter_list):
        """ given a list of booleans, only give back the values
        that align with True as a LabeledList
        """
        index = []
        data = []
        if len(filter_list) != len(self.index):
            raise IndexError('Length of indexes does not match length of boolean list')
        for i, include in enumerate(filter_list):
            if include:
                index.append(self.index[i])
                data.append(self.values[i])
        return LabeledList(data, index)
    
    def __find(self, k):
        """give back all labels and values based on key
        """
        index, data = [], []
        matches = [(label, self.values[i]) for i, label in enumerate(self.index) if k == label]
        if len(matches) == 0:
            raise KeyError(f'Index label not found {k}')
        return matches

    
class Table:
    # implement your table class here
    def __init__(self, data, index=None, columns=None):
        pass


if __name__ == '__main__':
    # add your manual tests here
    def squared(n):
        return n ** 2
    print(nt.LabeledList([5, 6, 7]).map(squared))
    pass



