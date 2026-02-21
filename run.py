import klang
import sys

if len(sys.argv) > 1:
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        script = f.read()
        res, err = klang.run(script)
        if err: print(err)
else:
    print("Please provide a .klang file!!!")