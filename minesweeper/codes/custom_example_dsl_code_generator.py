class CustomExampleDSLCodeGenerator:
    def __init__(self):
        self.non_operands = ['program', 'initiate_game',
                             'bomb_location', 'output',
                             'bomb_placements', 'begin_scope_operator',
                             'end_scope_operator', 'hint']
        self.operand_stack = []
        self.code_stack = []

    def is_operand(self, item):
        if item in self.non_operands:
            return False
        else:
            return True

    def generate_code(self, post_order_array):
        for item in post_order_array:
            if not self.is_operand(item["label"]):
                self.generate_code_based_on_non_operand(item["label"])
            else:
                self.operand_stack.append(item["label"])

        result = ''
        for code_string in self.code_stack:
            if code_string is not None:
                result += code_string
        return result

    def generate_code_based_on_non_operand(self, item):
        if item == "program":
            self.generate_program()

        elif item == "output":
            self.set_output_type()

        elif item == "initiate_game":
            self.generate_initiate_game()

        elif item == "hint":
            self.generate_hint()

        elif item == "bomb_location":
            self.generate_bomb()

        elif item == "bomb_placements":
            self.generate_bomb_placements()

        elif item == "begin_scope_operator":
            self.generate_begin_scope_operator()

        elif item == "end_scope_operator":
            self.generate_end_scope_operator()

    def generate_program(self):

        placements_code = self.code_stack.pop()
        initiate_code = self.code_stack.pop()
        hint_code = self.code_stack.pop()
        output_type = 'console'
        if len(self.code_stack) > 0:
            temp_code = self.code_stack.pop()
            if temp_code.startswith('##COMPILER_PARAM:::output_type:::'):
                output_type = temp_code.replace('##COMPILER_PARAM:::output_type:::', '')
            else:
                self.code_stack.append(temp_code)

        if output_type == 'console':
            program_code = (initiate_code + hint_code + placements_code
                            + "for row in bombs:\n" +
                            "\tfor column in row:\n" +
                            "\t\tif column == 'x':\n" +
                            "\t\t\tprint('*', end ='')\n" +
                            "\t\telse:\n" +
                            "\t\t\tsymbol = '#' if column == 0 else column\n"
                            "\t\t\tprint(symbol, end ='')\n" +
                            "\tprint()"
                            )
            self.code_stack.append(program_code)

    def generate_initiate_game(self):
        height = int(self.operand_stack.pop())
        width = int(self.operand_stack.pop())
        code_string = f"bombs = [[0 for y in range({height})] for x in range({width})]\n"
        self.code_stack.append(code_string)

    def generate_hint(self):
        # return
        val = self.operand_stack.pop()
        match val:
            case "true":
                code = (
                    "def new_bomb(x, y):\n" +
                    "\tbombs[x][y] = 'x'\n" +
                    "\tfor i in range(x-1, x + 2):\n" +
                    "\t\tfor j in range(y-1, y+2):\n" +
                    "\t\t\tif i < 0 or j < 0 or i >= len(bombs) or j >= len(bombs[0]) or  bombs[i][j] == 'x' :\n" +
                    "\t\t\t\tcontinue\n" +
                    "\t\t\tbombs[i][j] += 1\n"
                )
            case "false":
                code = (
                    "def new_bomb(x, y):\n" +
                    "\tbombs[x][y] = 'x'\n"
                )
            case _:
                raise ValueError(f"invalid value for hint, it must be 'true' or 'false' not {val}")
        self.code_stack.append(code)

    def generate_bomb(self):
        y = int(self.operand_stack.pop())
        x = int(self.operand_stack.pop())
        code_string = f"new_bomb({x - 1}, {y - 1})\n"
        self.code_stack.append(code_string)

    def set_output_type(self):
        self.code_stack.append(f"##COMPILER_PARAM:::output_type:::{self.operand_stack.pop()}")

    def generate_bomb_placements(self):
        temp_block_stack = []
        current_code = self.code_stack.pop()
        if current_code != '##COMPILER_PARAM:::scope:::end_scope_operator':
            self.code_stack.append(current_code)
            return
        while current_code != '##COMPILER_PARAM:::scope:::begin_scope_operator':
            current_code = self.code_stack.pop()
            temp_block_stack.append(current_code)
        temp_block_stack.pop()
        result = ''
        while len(temp_block_stack) != 0:
            result = result + temp_block_stack.pop()
        self.code_stack.append(result)

    def generate_begin_scope_operator(self):
        self.code_stack.append("##COMPILER_PARAM:::scope:::begin_scope_operator")

    def generate_end_scope_operator(self):
        self.code_stack.append("##COMPILER_PARAM:::scope:::end_scope_operator")
