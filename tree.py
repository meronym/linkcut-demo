#! /usr/bin/env python

import json


class Node:
    def __init__(self, root, left, right):
        self.root = root
        self.left = left
        self.right = right
        self.parent = None


class Tree:
    def __init__(self, inorder):
        self._nodes = {}
        self._root = self._from_inorder(inorder)

    @property
    def inorder(self):
        return self._to_inorder(self._root)

    def _index(self, node):
        self._nodes[node.root] = node

    def _from_inorder(self, inorder):
        if inorder is None:
            return None
        elif isinstance(inorder, list):
            left, root, right = inorder
            assert isinstance(root, str)
            left = self._from_inorder(left)
            right = self._from_inorder(right)
            node = Node(root, left, right)
            if left:
                left.parent = node
            if right:
                right.parent = node
        else:
            assert isinstance(inorder, str)
            node = Node(inorder, None, None)
        self._index(node)
        return node

    @classmethod
    def _to_inorder(cls, node):
        left = None if node.left is None else cls._to_inorder(node.left)
        right = None if node.right is None else cls._to_inorder(node.right)
        if left is None and right is None:
            # leaf node
            return node.root
        else:
            return [left, node.root, right]

    @classmethod
    def _replace_child(cls, old_child, new_child):
        parent = old_child.parent
        new_child.parent = parent
        
        if parent is None:
            return
        
        assert isinstance(parent, Node)
        assert old_child in (parent.left, parent.right)

        if old_child is parent.left:
            parent.left = new_child
        elif old_child is parent.right:
            parent.right = new_child

    def rot_right(self, node):
        root = self._nodes[node]
        pivot = root.left
        if pivot is None:
            raise ValueError('Cannot establish rotation pivot')
        
        self._replace_child(root, pivot)

        nephew = pivot.right
        root.left = nephew
        if nephew:
            nephew.parent = root
                
        pivot.right = root
        root.parent = pivot

    def rot_left(self, node):
        root = self._nodes[node]
        pivot = root.right
        if pivot is None:
            raise ValueError('Cannot establish rotation pivot')
        
        self._replace_child(root, pivot)

        nephew = pivot.left
        root.right = nephew
        if nephew:
            nephew.parent = root
                
        pivot.left = root
        root.parent = pivot


def test_traversals(case):
    t = Tree(case)
    assert t.inorder == case
    print(f'Traversal test OK: {case}')


def test_rotations(case):
    tree = Tree(case['initial'])
    for direction, root in case['operations']:
        if direction == 'right':
            tree.rot_right(root)
        else:
            tree.rot_left(root)
    print(tree.inorder)
    assert tree.inorder == case['final']


if __name__ == '__main__':
    with open('test_traversals.json') as f:
        data = json.loads(f.read())
    for case in data:
        test_traversals(case)

    with open('test_rotations.json') as f:
        data = json.loads(f.read())
    for case in data:
        test_rotations(case)
