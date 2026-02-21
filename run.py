import klang
import sys
from pathlib import Path

if len(sys.argv) > 1:
    filename = sys.argv[1]

    base_dir = Path(__file__).parent
    filepath = base_dir / "Project folder" / filename

    if filepath.exists():
        script = filepath.read_text()
        res, err = klang.run(script)
        if err:
            print(err)
    else:
        print(f"File not found in 'Project folder': {filename}")
else:
    print("Please provide a .klang file!!!")