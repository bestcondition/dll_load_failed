import shutil
from pathlib import Path
import random


class PyFile:
    def __init__(self, path: Path):
        self.path = path
        self.import_lines = []

    def module_name(self):
        return self.path.stem

    def save(self):
        random.shuffle(self.import_lines)
        with self.path.open('w', encoding='utf8') as f:
            print(f"save {self.path}")
            f.write('\n'.join(self.import_lines))

    def add_import_line(self, import_line):
        self.import_lines.append(self.wrap_code(import_line))

    def wrap_code(self, code: str):
        i_m = f"it is {self.module_name()}; "
        return f"print(r'{i_m}begin {code}')\n{code}\nprint('{i_m}end {code}')\n"


def get_import_line(module_name):
    return f"from {module_name} import *"


def gen(import_code_list: list = None, file_nums=20, import_nums=20, ):
    if import_code_list is None:
        import_code_list = ['']
    gen_dir = Path(r"code")
    if gen_dir.exists():
        print("remove old code dir")
        shutil.rmtree(gen_dir)
    gen_dir.mkdir(parents=True, exist_ok=True)
    for file_index in range(file_nums):
        file_path = gen_dir / f"gen_{file_index}.py"
        py_file = PyFile(file_path)
        for _ in range(import_nums):
            import_code = random.choice(import_code_list)
            py_file.add_import_line(import_code)
        py_file.save()
        import_code_list.append(get_import_line(py_file.module_name()))
    main_file = gen_dir / "gen_main.py"
    main_py_file = PyFile(main_file)
    for line in import_code_list:
        main_py_file.add_import_line(line)
    main_py_file.save()

