import nelta as nt
import csv
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
        self.data = data
        self.index = list(range(len(data))) if index is None else index
        self.columns = list(range(len(data[0]))) if columns is None else columns

    def __str__(self):
        table = []
        table.append(['{:^10}'.format('     ')] + ['{:^10}'.format(c) for c in self.columns])
        for i, row in enumerate(self.data):
            table.append(['{:^10}'.format(self.index[i])] + ['{:^10}'.format(r) for r in row])
        return '\n'.join([''.join(r) for r in table])

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, col_list):
        if isinstance(col_list, list):
            if type(col_list[0]) in [bool, True, False]:
                data = [self.data[i] for i in range(len(self.data)) if col_list[i]]
                index = [self.index[i] for i in range(len(self.data)) if col_list[i]]
                return Table(data, index, self.columns)
            else:
                columns = col_list
                data = [[row[self.columns.index(col)] for col in col_list] for row in self.data]
                return Table(data, self.index, columns)
        else:
            column_indices = [i for i, col in enumerate(self.columns) if col == col_list]
            if len(column_indices) == 0:
                raise KeyError(f'Column not found: {col_list}')
            elif len(column_indices) == 1:
                return LabeledList([row[column_indices[0]] for row in self.data], self.index)
            else:
                data = [[row[i] for i in column_indices] for row in self.data]
                columns = [self.columns[i] for i in column_indices]
                return Table(data, self.index, columns)

    def head(self, n):
        data = self.data[:n]
        index = self.index[:n]
        return Table(data, index, self.columns)

    def tail(self, n):
        data = self.data[-n:]
        index = self.index[-n:]
        return Table(data, index, self.columns)

    def shape(self):
        return (len(self.data), len(self.columns))



def read_csv(fn):
    data = []
    with open(fn, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        columns = header
        for i, row in enumerate(reader):
            if not all(x == '' for x in row):
                data_row = []
                for item in row:
                    try:
                        data_row.append(float(item))
                    except ValueError:
                        data_row.append(item)
                data.append(data_row)
    index = list(range(len(data)))
    return Table(data, index, columns)


if __name__ == '__main__':  
    # t = nt.read_csv('recalls-truncated.csv')
    # d= [[1000, 10, 100,1, 1.0], [200,2,2.0,2000,20], [3,300,3000,3.0, 30],[40, 4000,4.0, 400, 4],[7,8, 6, 3,41]]
    # t = Table([[1, 2, 3], [4, 5, 6]], columns=['a', 'b', 'a'])
    # print(t[[True, False, False]])
    # ll = nt.LabeledList([1, 2, 3, 4, 5], ['A', 'BB', 'BB', 'CCC', 'D'])
    # print(ll[nt.LabeledList(['A', 'BB'])])

    # print(t[LabeledList(['a', 'b'])])
    pass