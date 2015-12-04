class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.root.__iter__()

    def put(self, key, val):
        if self.root is not None:
            self._put(key, val, self.root)
        else:
            self.root = TreeNode(key, val)
        self.size += 1

    def _put(self, key, val, current_node):
        if key < current_node.key:
            if current_node.has_left():
                self._put(key, val, current_node.left_child)
            else:
                current_node.left_child = TreeNode(key, val, parent=current_node)
        elif key > current_node.key:
            if current_node.has_right():
                self._put(key, val, current_node.right_child)
            else:
                current_node.right_child = TreeNode(key, val, parent=current_node)
        else:
            current_node.val = val

    def __setitem__(self, key, val):
        self.put(key, val)

    def get(self, key):
        if self.root is not None:
            return self._get(key, self.root)
        else:
            return None

    def _get(self, key, current_node):
        if key < current_node.key:
            if current_node.has_left():
                return self._get(key, current_node.left_child)
            return None
        elif key > current_node.key:
            if current_node.has_right():
                return self._get(key, current_node.right_child)
            return None
        else:
            return current_node

    def __contains__(self, key):
        return self.get(key) is not None

    def __getitem__(self, key):
        return self.get(key)

    def delete(self, key):
        if self.size > 1:
            node_to_remove = self._get(key, self.root)
            if node_to_remove is not None:
                self.remove(node_to_remove)
                self.size -= 1
            else:
                raise KeyError('Error, {} is not in tree.'.format(key))
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size -= 1
        else:
            raise KeyError('Error, {} is not in tree'.format(key))

    def __delitem__(self, key):
        self.delete(key)

    def remove(self, node):
        if node.is_leaf():
            if node == node.parent.left_child:
                node.parent.left_child = None
            else:
                node.parent.right_child = None
        elif node.has_both_children():
            succ = node.find_successor()
            succ.splice_out()
            node.key = succ.key
            node.val = succ.val
        else:
            if node.has_left():
                if node.is_left_child():
                    node.left_child.parent = node.parent
                    node.parent.left_child = node.left_child
                elif node.is_right_child():
                    node.left_child.parent = node.parent
                    node.parent.right_child = node.left_child
                else:
                    node.replace_node_data(
                        node.left_child.key, node.left_child.val,
                        node.left_child.left_child, node.right_child.right_child)
            else:
                if node.is_left_child():
                    node.right_child.parent = node.parent
                    node.parent.left_child = node.right_child
                elif node.is_right_child():
                    node.right_child.parent = node.parent
                    node.parent.right_child = node.right_child
                else:
                    node.replace_node_data(
                        node.right_child.key, node.right_child.val,
                        node.right_child.left_child, node.right_child.right_child)


class TreeNode:
    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key
        self.val = val
        self.left_child = left
        self.right_child = right
        self.parent = parent

    def has_left(self):
        return self.left_child is not None

    def has_right(self):
        return self.right_child is not None

    def is_left_child(self):
        return self.parent is not None and self.parent.left_child == self

    def is_right_child(self):
        return self.parent is not None and self.parent.right_child == self

    def is_root(self):
        return self.parent is None

    def is_leaf(self):
        return self.left_child is None and self.right_child is None

    def has_any_children(self):
        return self.right_child is not None or self.left_child is not None

    def has_both_children(self):
        return self.right_child is not None and self.right_child is not None

    def replace_node_data(self, key, val, left, right):
        self.key = key
        self.val = val
        self.left_child = left
        self.right_child = right
        if self.has_left():
            self.left_child.parent = self
        if self.has_right():
            self.right_child.parent = self

    def find_successor(self):
        succ = None
        if self.has_right():
            succ = self.right_child.find_min()
        else:
            if self.parent is not None:
                if self.is_left_child():
                    succ = self.parent
                else:
                    self.parent.right_child = None
                    succ = self.parent.find_successor()
                    self.parent.right_child = self
        return succ

    def find_min(self):
        current = self
        while current.has_left():
            current = current.left_child
        return current

    def splice_out(self):
        if self.is_leaf():
            if self.is_left_child():
                self.parent.left_child = None
            else:
                self.parent.right_child = None
        elif self.has_any_children():
            if self.has_left():
                if self.is_left_child():
                    self.parent.left_child = self.left_child
                else:
                    self.parent.right_child = self.left_child
                self.left_child.parent = self.parent
            else:
                if self.is_left_child():
                    self.parent.left_child = self.right_child
                else:
                    self.parent.right_child = self.right_child
                self.right_child.parent = self.parent

    def __iter__(self):
        if self is not None:
            if self.has_left():
                for node in self.left_child:
                    yield node
            yield self
            if self.has_right():
                for node in self.right_child:
                    yield node
