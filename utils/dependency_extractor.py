def extract_dependencies(files_info):
    # Consolidate dependencies from all files
    dependencies = {}
    for file_path, info in files_info.items():
        dependencies[file_path] = info.get('dependencies', [])
    return dependencies
