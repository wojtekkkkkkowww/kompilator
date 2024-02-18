import sys
from Lexer import MyLexer
from Parser import MyParser
from Analyzer import MyAnalyzer
from CodeGenerator import CodeGenerator


def main():
    if len(sys.argv) != 3:
        print('Usage: python kompilator.py <input_file_path> <output_file_path>')
        sys.exit(1)

    input_file_path = sys.argv[1]

    with open(input_file_path, 'r') as file:
        input_text = file.read()

    lexer = MyLexer()
    parser = MyParser()

    tokens = lexer.tokenize(input_text)

    ast = parser.parse(tokens)

    analizer = MyAnalyzer()
    analizer.analyze(ast)
    data =  analizer.get_data()
    code_generator = CodeGenerator(data)
    code =  code_generator.translate(ast)
    
    output_file_path = sys.argv[2]
    with open(output_file_path, 'w') as file:
        for line in code:
            file.write(line + '\n')
    

if __name__ == "__main__":
    main()