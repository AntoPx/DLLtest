import os
import sys
import platform
import subprocess
import ctypes
import pefile

# Determine whether the DLL is 32-bit or 64-bit based on PE headers
def check_architecture(dll_path):
    try:
        pe = pefile.PE(dll_path)
        return "64bit" if pe.FILE_HEADER.Machine == 0x8664 else "32bit"
    except:
        return None

# Check if a specific DLL dependency is available in system paths
def is_dll_available(dll_name):
    search_paths = os.environ['PATH'].split(os.pathsep)
    system_paths = [os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32')]
    for path in system_paths + search_paths:
        full_path = os.path.join(path, dll_name)
        if os.path.isfile(full_path):
            return True
    return False

# Analyze the dependencies of a DLL using PE headers
def analyze_dependencies(dll_path):
    try:
        pe = pefile.PE(dll_path)
    except Exception as e:
        print(f"❗ Error reading PE file: {e}")
        return

    print(f"\n📊 Analyzing dependencies: {dll_path}")
    arch = "64 bit" if pe.FILE_HEADER.Machine == 0x8664 else "32 bit"
    print(f"📦 DLL architecture: {arch}")

    if not hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
        print("ℹ️ No dependencies found.")
        return

    missing = []
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        dll_name = entry.dll.decode('utf-8')
        print(f"  - {dll_name}")
        if not is_dll_available(dll_name):
            missing.append(dll_name)

    if missing:
        print("❌ Missing DLLs:")
        for m in missing:
            print(f"  - {m}")
    else:
        print("✅ All dependencies found.")

# Try to load the DLL using ctypes
def try_load_dll(dll_path):
    print(f"\n🔄 Attempting to load DLL: {dll_path}")
    try:
        ctypes.WinDLL(dll_path)
        print("✅ DLL successfully loaded.")
    except Exception as e:
        print(f"❌ Error loading DLL: {e}")

# 👉 Update with the correct paths to your 32-bit and 64-bit Python interpreters
def get_python_path(target_arch):
    return {
        "64bit": r"C:\Users\granata\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\python.exe",
        "32bit": r"C:\Users\granata\AppData\Local\Programs\Python\Python313-32\python.exe"
    }.get(target_arch, sys.executable)

# Test a single DLL: architecture check, dependency analysis, and load attempt
def test_dll(dll_path):
    if not os.path.isfile(dll_path):
        print(f"❗ Invalid file path: {dll_path}")
        return

    target_arch = check_architecture(dll_path)
    if not target_arch:
        print(f"❗ Unable to determine architecture: {dll_path}")
        return

    current_arch = platform.architecture()[0]
    
    # Relaunch the script if current interpreter architecture doesn't match the DLL
    if current_arch != target_arch:
        print(f"🔁 Interpreter architecture mismatch. Relaunching with Python {target_arch}...")
        python_path = get_python_path(target_arch)
        subprocess.run([python_path, __file__, dll_path])
        return

    print(f"\n🧪 Testing DLL: {dll_path}")
    print(f"📦 DLL architecture: {target_arch}")
    print(f"🐍 Current Python interpreter: {current_arch}")
    
    analyze_dependencies(dll_path)
    try_load_dll(dll_path)

# If a folder is given, scan it and test all DLLs inside
def scan_folder(folder):
    for file in os.listdir(folder):
        if file.lower().endswith(".dll"):
            test_dll(os.path.join(folder, file))

# Entry point for command-line execution
if __name__ == "__main__":
    if len(sys.argv) == 2:
        path = sys.argv[1]
        if os.path.isdir(path):
            scan_folder(path)
        else:
            test_dll(path)
    else:
        print("📥 Usage: python DLLtest.py <dll_path_or_folder>")
