# 🧪 TestMultipleDLLs

A Python script to **analyze and test Windows DLL files** for:
- Architecture compatibility (32-bit or 64-bit)
- Dependency checks
- Loadability via `ctypes`

---

## 📦 Requirements

Before running the script, ensure you have the following installed:

### ✅ Python Interpreters
- One **64-bit Python interpreter**
- One **32-bit Python interpreter**

You can download them from [python.org](https://www.python.org/downloads/). Install both versions and note their paths.

### ✅ Python Modules
This script uses the `pefile` module to inspect DLL headers. You can install it via pip:

```bash
pip install pefile
```

---

## 🛠️ Configuration

Edit the following function in the script to include the correct paths to your Python interpreters:

```python
def get_python_path(target_arch):
    return {
        "64bit": r"C:\Path\To\Your\64bit\Python\python.exe",
        "32bit": r"C:\Path\To\Your\32bit\Python\python.exe"
    }.get(target_arch, sys.executable)
```

---

## 🚀 How to Run

### 🔹 Test a single DLL
```bash
python DLLtest.py "C:\Path\To\Your\File.dll"
```

### 🔹 Test all DLLs in a folder
```bash
python DLLtest.py "C:\Path\To\Your\Folder"
```

The script will:
1. Check DLL architecture (32bit or 64bit).
2. Switch to the matching Python interpreter if needed.
3. Print all dependencies and highlight any missing DLLs.
4. Attempt to load the DLL using `ctypes`.

---

## 🧾 Output Example

```text
🧪 Testing DLL: C:\Path\To\RTIME.dll
📦 DLL architecture: 32bit
🐍 Current Python interpreter: 64bit
🔁 Interpreter architecture mismatch. Relaunching with Python 32bit...

📊 Analyzing dependencies: RTIME.dll
  - KERNEL32.dll
  - NIDAG32.dll ❌ Missing
❌ Error loading DLL: Could not find module RTIME.dll (or one of its dependencies)
```

---

## ℹ️ Notes

- If a DLL cannot be loaded, it may be due to:
  - Missing dependencies (check the printed list)
  - Incorrect architecture
  - System-level issues (e.g., driver DLLs not accessible)

---

## 📤 License

This project is provided as-is for internal use and diagnostics.
