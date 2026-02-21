# values.py
class Value:
    def __init__(self, val):
        self.value = val

    def __repr__(self):
        return str(self.value)

class Array(Value):
    def __init__(self, elements):
        initial_data = elements if isinstance(elements, list) else [elements]
        super().__init__(initial_data)
        
        self.methods = {
            "length": lambda args: len(self.value),
            "append": self.klang_append,
            "bubble_sort": self.klang_bubble_sort,
            "selection_sort": self.klang_selection_sort,
            "insertion_sort": self.klang_insertion_sort
        }

    def klang_append(self, args):
        new_item = args[0]
        self.value.append(new_item)
        return self

    def klang_bubble_sort(self, args):
        data = self.value
        size = len(data)
        for i in range(size):
            for j in range(0, size - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
        return self

    def klang_selection_sort(self, args):
        data = self.value
        for i in range(len(data)):
            min_idx = i
            for j in range(i + 1, len(data)):
                if data[min_idx] > data[j]: 
                    min_idx = j
            data[i], data[min_idx] = data[min_idx], data[i]
        return self

    def klang_insertion_sort(self, args):
        data = self.value
        for i in range(1, len(data)):
            current = data[i]
            prev_idx = i - 1
            while prev_idx >= 0 and current < data[prev_idx]:
                data[prev_idx + 1] = data[prev_idx]
                prev_idx -= 1
            data[prev_idx + 1] = current
        return self

    def __repr__(self):
        return "Array(" + " ".join([str(x) for x in self.value]) + ")"

class Stack(Value):
    def __init__(self, initial_items):
        data_list = list(initial_items) if initial_items is not None else []
        super().__init__(data_list)
        
        self.methods = {
            "length": lambda args: len(self.value),
            "push": self.klang_push,
            "pop": self.klang_pop,
            "peek": self.klang_peek
        }

    def klang_push(self, args):
        item = args[0]
        self.value.append(item)
        return self

    def klang_pop(self, args):
        if not self.value: return 0
        return self.value.pop()

    def klang_peek(self, args):
        if not self.value: return 0
        return self.value[-1]

    def __repr__(self):
        stack_view = " | ".join([str(x) for x in reversed(self.value)])
        return f"Stack(Top -> {stack_view})"