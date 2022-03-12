from compiler import Compiler
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="컴파일할 파일을 선택해주세요.")
    args = parser.parse_args()
    cmp = Compiler()
    cmp.compileFile(args.file)