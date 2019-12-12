import argparse

parser = argparse.ArgumentParser(description='Fetch input data for processing')

parser.add_argument('source', help='The source url in http')
parser.add_argument('--stacks', action='store_true', help='Whether ther are stack under the URL')
parser.add_argument('--glob', help="Filename filter for container stacks")

def main():
    args = parser.parse_args()
    print(args)

if __name__ == "__main__":
    main()
