import os
import argparse
from pathlib import Path

def generate_tree_structure(directory, prefix="", max_depth=None, current_depth=0):
    """Generate a tree-like structure of the directory"""
    if max_depth is not None and current_depth > max_depth:
        return ""
    
    items = []
    path = Path(directory)
    
    # Skip common directories/files you might want to ignore
    ignore_patterns = {'.git', '__pycache__', '.vscode', '.idea', 'node_modules', 
                      '.DS_Store', '.env', '*.pyc', '.gitignore'}
    
    try:
        # Get all items and sort them (directories first, then files)
        all_items = [item for item in path.iterdir() 
                    if not any(pattern in item.name for pattern in ignore_patterns)]
        all_items.sort(key=lambda x: (x.is_file(), x.name.lower()))
        
        for i, item in enumerate(all_items):
            is_last = i == len(all_items) - 1
            
            # Choose the right prefix symbols
            if is_last:
                current_prefix = "└── "
                next_prefix = prefix + "    "
            else:
                current_prefix = "├── "
                next_prefix = prefix + "│   "
            
            # Add current item
            items.append(f"{prefix}{current_prefix}{item.name}")
            
            # Recursively add subdirectories
            if item.is_dir():
                items.append(generate_tree_structure(
                    item, next_prefix, max_depth, current_depth + 1
                ))
                
    except PermissionError:
        items.append(f"{prefix}└── [Permission Denied]")
    
    return "\n".join(filter(None, items))

def generate_simple_list(directory, prefix="", max_depth=None, current_depth=0):
    """Generate a simple indented list structure"""
    if max_depth is not None and current_depth > max_depth:
        return ""
    
    items = []
    path = Path(directory)
    
    ignore_patterns = {'.git', '__pycache__', '.vscode', '.idea', 'node_modules', 
                      '.DS_Store', '.env', '*.pyc', '.gitignore'}
    
    try:
        all_items = [item for item in path.iterdir() 
                    if not any(pattern in item.name for pattern in ignore_patterns)]
        all_items.sort(key=lambda x: (x.is_file(), x.name.lower()))
        
        for item in all_items:
            # Add current item with indentation
            items.append(f"{prefix}{item.name}")
            
            # Recursively add subdirectories
            if item.is_dir():
                items.append(generate_simple_list(
                    item, prefix + "  ", max_depth, current_depth + 1
                ))
                
    except PermissionError:
        items.append(f"{prefix}[Permission Denied]")
    
    return "\n".join(filter(None, items))

def main():
    parser = argparse.ArgumentParser(description='Generate project file structure')
    parser.add_argument('directory', nargs='?', default='.', 
                       help='Directory to analyze (default: current directory)')
    parser.add_argument('--style', choices=['tree', 'simple'], default='tree',
                       help='Output style (default: tree)')
    parser.add_argument('--max-depth', type=int, default=None,
                       help='Maximum depth to traverse')
    parser.add_argument('--output', '-o', type=str, default=None,
                       help='Output file (default: print to console)')
    
    args = parser.parse_args()
    
    # Get the absolute path
    directory = Path(args.directory).resolve()
    
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist.")
        return
    
    if not directory.is_dir():
        print(f"Error: '{directory}' is not a directory.")
        return
    
    # Generate the structure
    print(f"Generating file structure for: {directory}")
    print(f"Style: {args.style}")
    if args.max_depth:
        print(f"Max depth: {args.max_depth}")
    print("-" * 50)
    
    if args.style == 'tree':
        structure = f"{directory.name}/\n" + generate_tree_structure(
            directory, max_depth=args.max_depth
        )
    else:
        structure = f"{directory.name}/\n" + generate_simple_list(
            directory, "  ", max_depth=args.max_depth
        )
    
    # Output the result
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(structure)
        print(f"File structure saved to: {args.output}")
    else:
        print(structure)

if __name__ == "__main__":
    main()

# Example usage:
# python file_structure.py
# python file_structure.py /path/to/your/project
# python file_structure.py --style simple --max-depth 3
# python file_structure.py --output project_structure.txt