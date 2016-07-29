import survey1

from content.survey2 import OPTIONS, t1, t3


def validate_user_input_for_test1(user_input):
    if user_input.encode('utf-8') in survey1.OPTIONS.values():
        return True
    else:
        return False


def parse_answer_value_for_test1(user_input):
    if validate_user_input_for_test1(user_input):
        inv_map = {v: k for k, v in survey1.OPTIONS.items()}
        return inv_map[user_input.encode('utf-8')]
    else:
        raise Exception('Not a valid answer')


def validate_user_input_for_test2(user_input, part, dream_cat=0):
    part = int(part)
    if part == 1:
        return True if user_input.encode('utf-8') in t1 else False
    elif part == 2:
        return True if user_input.encode('utf-8') in t3[dream_cat] else False
    elif part == 3:
        return True if user_input.encode('utf-8') in OPTIONS.values() else False


def parse_answer_value_for_test2(user_input, part, dream_cat=0):
    if validate_user_input_for_test2(user_input, part, dream_cat):
        if part == 1:
            for i, item in enumerate(t1):
                if item == user_input.encode('utf-8'):
                    return int(i)
        elif part == 2:
            for i, item in enumerate(t3[dream_cat]):
                if item == user_input.encode('utf-8'):
                    return int(i)
        elif part == 3:
            inv_map = {v: k for k, v in survey1.OPTIONS.items()}
            return int(inv_map[user_input.encode('utf-8')])
        raise Exception('Not a valid answer')


def markdown(msg):
    return "`" + msg + "`"