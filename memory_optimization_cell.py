# Memory optimization functions for notebooks
import os
import shutil
import subprocess
import gc
import time
from IPython.display import display, HTML, clear_output

# Install required packages first
!pip install -q psutil
import psutil

def clear_disk_space():
    """Clean up disk space by removing unnecessary files."""
    print("🧹 Cleaning up disk space...")
    
    # Clean apt cache
    subprocess.run("apt-get clean", shell=True)
    
    # Remove unnecessary packages
    subprocess.run("apt-get -y autoremove", shell=True)
    
    # Clean pip cache
    subprocess.run("rm -rf ~/.cache/pip", shell=True)
    
    # Remove temporary files
    temp_dirs = ['/tmp', '/var/tmp']
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            try:
                for item in os.listdir(temp_dir):
                    item_path = os.path.join(temp_dir, item)
                    # Skip our ollama directories
                    if item.startswith('ollama') or item.startswith('backdoor'):
                        continue
                    
                    try:
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                        else:
                            os.remove(item_path)
                    except Exception as e:
                        pass  # Skip files that can't be removed
            except Exception as e:
                print(f"Warning: Could not clean {temp_dir}: {e}")
    
    # Remove unused Docker images/containers if Docker is installed
    try:
        subprocess.run("docker system prune -af", shell=True, stderr=subprocess.DEVNULL)
    except:
        pass
    
    print("✅ Disk cleanup complete!")
    show_disk_usage()

def show_disk_usage():
    """Show current disk usage."""
    try:
        df_output = subprocess.check_output("df -h /", shell=True, text=True)
        print("\n📊 Disk Space Available:")
        for line in df_output.split('\n'):
            print(line)
    except:
        print("Could not retrieve disk usage information")

def show_memory_usage():
    """Show current memory usage."""
    try:
        memory = psutil.virtual_memory()
        total_gb = memory.total / (1024 ** 3)
        available_gb = memory.available / (1024 ** 3)
        used_gb = memory.used / (1024 ** 3)
        percent = memory.percent
        
        print(f"\n📊 Memory Usage:")
        print(f"Total Memory: {total_gb:.2f} GB")
        print(f"Available: {available_gb:.2f} GB")
        print(f"Used: {used_gb:.2f} GB ({percent}%)")
    except:
        print("Could not retrieve memory usage information")

def clear_memory():
    """Clear Python memory."""
    gc.collect()
    torch_available = False
    
    try:
        import torch
        torch_available = True
    except ImportError:
        pass
    
    if torch_available:
        try:
            import torch
            torch.cuda.empty_cache()
            print("✅ PyTorch CUDA cache cleared")
        except:
            pass
    
    print("✅ Python memory cleared")

def clean_model_files(keep_models=None):
    """Clean up model files to free space, optionally keeping specified models."""
    if keep_models is None:
        keep_models = []
    
    print(f"🧹 Cleaning model files (keeping: {', '.join(keep_models) if keep_models else 'none'})...")
    
    # Clean Ollama model files (except the ones specified to keep)
    ollama_dirs = ['/root/.ollama', '/tmp/ollama']
    
    for ollama_dir in ollama_dirs:
        if os.path.exists(ollama_dir):
            models_path = os.path.join(ollama_dir, 'models')
            if os.path.exists(models_path):
                for model_file in os.listdir(models_path):
                    should_keep = False
                    for keep_model in keep_models:
                        if keep_model in model_file:
                            should_keep = True
                            break
                    
                    if not should_keep:
                        try:
                            model_path = os.path.join(models_path, model_file)
                            if os.path.isdir(model_path):
                                shutil.rmtree(model_path)
                            else:
                                os.remove(model_path)
                            print(f"  - Removed: {model_file}")
                        except Exception as e:
                            print(f"  - Could not remove {model_file}: {e}")
    
    print("✅ Model cleanup complete!")

def optimize_for_large_models():
    """Run all optimizations to prepare for large language models."""
    print("🚀 Optimizing environment for large language models...")
    clear_disk_space()
    clear_memory()
    
    # Set environment variables for improved performance
    os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:512"
    
    # Show current resource usage
    show_memory_usage()
    show_disk_usage()
    
    print("\n✅ Optimization complete! Ready to continue.")

# Run optimization process
optimize_for_large_models()
