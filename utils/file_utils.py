import os

class TreeNode:
    def __init__(self, name, path, is_dir):
        self.name = name
        self.path = path
        self.is_dir = is_dir
        self.children = []

    def render(self, prefix=''):
        lines = []
        lines.append(prefix + self.name)
        if self.is_dir:
            for i, child in enumerate(self.children):
                if i == len(self.children) - 1:
                    child_prefix = prefix + '└── '
                    next_prefix = prefix + '    '
                else:
                    child_prefix = prefix + '├── '
                    next_prefix = prefix + '│   '
                lines.extend(child.render(next_prefix).split('\n'))
        return '\n'.join(lines)

def get_project_structure(project_path):
    name = os.path.basename(project_path.rstrip(os.sep))
    root_node = TreeNode(name, project_path, True)
    build_tree(root_node)
    return root_node

def build_tree(node):
    if node.is_dir:
        try:
            items = os.listdir(node.path)
        except PermissionError:
            return
        for item in sorted(items):
            item_path = os.path.join(node.path, item)
            is_dir = os.path.isdir(item_path)
            child_node = TreeNode(item, item_path, is_dir)
            node.children.append(child_node)
            build_tree(child_node)
