import os
import re
import ast
import esprima
import javalang
import clang.cindex
from bs4 import BeautifulSoup

class LanguageAnalyzer:
    def __init__(self):
        pass

    def analyze_project(self, project_path):
        files_info = {}
        for root, dirs, files in os.walk(project_path):
            for file in files:
                file_path = os.path.join(root, file)
                info = self.analyze_file(file_path)
                files_info[file_path] = info
        return files_info

    def analyze_file(self, file_path):
        info = {
            'content': '',
            'functions': [],
            'classes': [],
            'function_summaries': {},
            'class_summaries': {},
            'dependencies': []
        }
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                info['content'] = content
        except:
            return info

        ext = os.path.splitext(file_path)[1]
        if ext == '.py':
            info.update(self.analyze_python(content))
        elif ext == '.js':
            info.update(self.analyze_javascript(content))
        elif ext == '.php':
            info.update(self.analyze_php(content))
        elif ext == '.java':
            info.update(self.analyze_java(content))
        elif ext in ['.cpp', '.h', '.hpp', '.cc']:
            info.update(self.analyze_cpp(file_path))
        elif ext in ['.html', '.htm']:
            info.update(self.analyze_html(content))
        elif ext == '.css':
            info.update(self.analyze_css(content))
        else:
            info.update(self.analyze_text(content))

        return info

    def analyze_python(self, content):
        functions = []
        classes = []
        dependencies = []
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        dependencies.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    dependencies.append(node.module)
        except:
            pass
        return {
            'functions': functions,
            'classes': classes,
            'dependencies': dependencies
        }

    def analyze_javascript(self, content):
        functions = []
        classes = []
        dependencies = []
        try:
            tree = esprima.parseScript(content, tolerant=True)
            for node in tree.body:
                if node.type == 'FunctionDeclaration':
                    functions.append(node.id.name)
                elif node.type == 'ClassDeclaration':
                    classes.append(node.id.name)
                elif node.type == 'ImportDeclaration':
                    dependencies.append(node.source.value)
        except:
            pass
        return {
            'functions': functions,
            'classes': classes,
            'dependencies': dependencies
        }

    def analyze_php(self, content):
        functions = re.findall(r'function\s+(\w+)\s*\(', content)
        classes = re.findall(r'class\s+(\w+)\s*', content)
        dependencies = re.findall(r'require_once\s*[\'"](.+?)[\'"]', content)
        return {
            'functions': functions,
            'classes': classes,
            'dependencies': dependencies
        }

    def analyze_java(self, content):
        functions = []
        classes = []
        dependencies = []
        try:
            tree = javalang.parse.parse(content)
            for path, node in tree:
                if isinstance(node, javalang.tree.MethodDeclaration):
                    functions.append(node.name)
                elif isinstance(node, javalang.tree.ClassDeclaration):
                    classes.append(node.name)
                elif isinstance(node, javalang.tree.Import):
                    dependencies.append(node.path)
        except:
            pass
        return {
            'functions': functions,
            'classes': classes,
            'dependencies': dependencies
        }

    def analyze_cpp(self, file_path):
        functions = []
        classes = []
        dependencies = []
        index = clang.cindex.Index.create()
        try:
            translation_unit = index.parse(file_path)
            for cursor in translation_unit.cursor.walk_preorder():
                if cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL:
                    functions.append(cursor.spelling)
                elif cursor.kind == clang.cindex.CursorKind.CLASS_DECL:
                    classes.append(cursor.spelling)
                elif cursor.kind == clang.cindex.CursorKind.INCLUSION_DIRECTIVE:
                    dependencies.append(cursor.spelling)
        except:
            pass
        return {
            'functions': functions,
            'classes': classes,
            'dependencies': dependencies
        }

    def analyze_html(self, content):
        functions = []
        classes = []
        dependencies = []
        soup = BeautifulSoup(content, 'html.parser')
        scripts = soup.find_all('script', src=True)
        links = soup.find_all('link', href=True)
        for script in scripts:
            dependencies.append(script['src'])
        for link in links:
            dependencies.append(link['href'])
        return {
            'functions': functions,
            'classes': classes,
            'dependencies': dependencies
        }

    def analyze_css(self, content):
        classes = re.findall(r'\.(\w+)\s*\{', content)
        return {
            'functions': [],
            'classes': classes,
            'dependencies': []
        }

    def analyze_text(self, content):
        # Pour les fichiers avec des extensions inconnues, on peut éventuellement faire une analyse de texte
        return {
            'functions': [],
            'classes': [],
            'dependencies': []
        }
