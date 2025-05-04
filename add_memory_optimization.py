#!/usr/bin/env python3
import json
import os
import glob

# Path to the optimization cell code
optimization_cell_path = "memory_optimization_cell.py"

# Read the optimization cell content
with open(optimization_cell_path, "r") as f:
    optimization_code = f.read()

# Get all notebook files
notebook_files = glob.glob("notebooks/ollama_config/*.ipynb")

for notebook_file in notebook_files:
    print(f"Processing {notebook_file}...")
    
    # Read the notebook
    with open(notebook_file, "r") as f:
        notebook = json.load(f)
    
    # Check if memory optimization is already present
    has_optimization = False
    for cell in notebook["cells"]:
        if cell.get("cell_type") == "code" and "memory_optimization" in "".join(cell.get("source", [])):
            has_optimization = True
            print(f"  Memory optimization already present in {notebook_file}")
            break
    
    if has_optimization:
        continue
    
    # Find where to insert the memory optimization section
    # We want to add it after the introduction markdown but before the first code cell
    insert_index = 1  # Default to after first cell
    
    # Find a better position - after introduction, before first code
    found_intro = False
    for i, cell in enumerate(notebook["cells"]):
        if cell.get("cell_type") == "markdown" and "how it works" in "".join(cell.get("source", [])).lower():
            found_intro = True
            insert_index = i + 1
        elif found_intro and cell.get("cell_type") == "code":
            break
    
    # Create markdown cell for memory optimization
    memory_markdown_cell = {
        "cell_type": "markdown",
        "metadata": {
            "id": "memory-optimization"
        },
        "source": [
            "## Memory Optimization for Large Models\n",
            "\n",
            "First, let's clear up disk space and optimize memory to ensure we have enough resources for large models."
        ]
    }
    
    # Create code cell for memory optimization
    memory_code_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {
            "id": "memory-optimization-code"
        },
        "outputs": [],
        "source": optimization_code.split("\n")
    }
    
    # Insert cells at the appropriate position
    notebook["cells"].insert(insert_index, memory_markdown_cell)
    notebook["cells"].insert(insert_index + 1, memory_code_cell)
    
    # Update the notebook title to indicate memory optimization
    for i, cell in enumerate(notebook["cells"]):
        if i == 0 and cell.get("cell_type") == "markdown":
            source = "".join(cell.get("source", []))
            if "Memory Optimized" not in source:
                title_lines = cell.get("source", [])
                for j, line in enumerate(title_lines):
                    if "# Backdoor AI" in line:
                        title_lines[j] = line.replace("# Backdoor AI", "# Backdoor AI - Memory Optimized")
                        break
                notebook["cells"][i]["source"] = title_lines
    
    # Write updated notebook
    with open(notebook_file, "w") as f:
        json.dump(notebook, f, indent=2)
    
    print(f"  Added memory optimization to {notebook_file}")

print("All notebooks updated!")
