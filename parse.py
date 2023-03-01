import pdb


def parse(string):
    OPCODES = [
        "NO_OP",
        "LOAD_AI",
        "LOAD_BI",
        "ADD_AB",
        "SUB_AB",
        "JUMP",
        "JUMP_EQ",
        "JUMP_GT",
        "JUMP_LT",
        "SWAP_AB",
        "SWAP_AC",
        "INC_A",
        "CMP_AB",
        "-",
        "-",
        "HALT",
    ]

    lines = string.split('\n')

    trimmed_lines = [k for k in lines if k not in ('', '\n', '\t')]

    trimmed = [k.strip() for k in trimmed_lines]

    splitted = [tuple(k.split(' ')) for k in trimmed]

    operations = []

    for item in splitted:
        data = item[1]

        if data == 'None':
            data = None

        try:
            int(data)
            data = int(data)
        except Exception as e:
            pass
        operations.append((OPCODES.index(item[0]), data))



    return operations
