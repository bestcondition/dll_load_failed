from multiprocessing.pool import Pool
import shutil
import sys
import tempfile
from pathlib import Path


def build():
    task_list = []
    root = Path(r"code")
    target = Path(r"target")
    if target.exists():
        print("remove old target dir")
        shutil.rmtree(target)
    for f in root.iterdir():
        if f.is_file() and f.suffix == ".py":
            task_list.append((str(f), str(target.joinpath(f.name).with_suffix(".pyd"))))
    with Pool() as pool:
        pool.starmap(gen_pyd, task_list)


def run_cmd(cmd_part_list: list[str], check=True):
    import subprocess
    print(f"Running command: {cmd_part_list}")
    return subprocess.run(cmd_part_list, check=check)


def gen_pyd(source_file: str, target_file: str):
    target_file = Path(target_file)
    with tempfile.TemporaryDirectory() as temp_d:
        temp_d_path = Path(temp_d)
        run_cmd([
            sys.executable,
            "-m",
            "nuitka",
            "--module",
            "--no-pyi-file",
            f'--output-dir={temp_d_path}',
            f'{source_file}'
        ])
        file = None
        for f in temp_d_path.iterdir():
            if f.is_file() and f.suffix == ".pyd":
                file = f
                break
        if file is None:
            raise Exception(f"No pyd file found, source file is {source_file}")
        target_file.parent.mkdir(parents=True, exist_ok=True)
        print(f'build source py {source_file} --> {target_file}')
        shutil.move(str(file), str(target_file))
