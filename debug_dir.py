import os
from pathlib import Path

base = Path(os.getcwd())
cn = base / "extracted_cn"

print(f"Base: {base}")
print(f"CN: {cn}, exists: {cn.exists()}")

if cn.exists():
    print("Listing:")
    for x in cn.iterdir():
        print(f" - {x.name} (is_dir: {x.is_dir()})")

