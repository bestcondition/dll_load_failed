from gen_random_code import gen
from build_batch import build


def main():
    # import_code_list = open('impt.py', encoding='utf8').read().splitlines()
    import_code_list = None
    gen(import_code_list=import_code_list, file_nums=200, import_nums=30)
    build()


if __name__ == '__main__':
    main()
