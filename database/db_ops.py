import time

import db_iface as db_if


def get_db_table(tab):
    db = db_if.get_db()
    table = db[tab]
    return table


def register_user(_id):
    data = dict(chat_id=_id)
    get_db_table('users').upsert(data, ['chat_id'])
    row = get_db_table('users').find_one(chat_id=_id)
    if 'age' in row:
        if str(row['age']).isdigit():
            return True
    return False


def save_box(_id, _list):
    data = {'chat_id': _id, 'box': ''.join(str(x) for x in _list)}
    get_db_table('users').upsert(data, ['chat_id'])


def get_box(_id):
    row = get_db_table('users').find_one(chat_id=_id)
    if 'box' in row:
        return row['box']
    else:
        return None


def save_answer(_id, _q_num, _item):
    col_names = ['t1q' + str(i + 1) for i in range(10)]
    # q_col_names = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10']
    data = {'chat_id': _id, col_names[int(_q_num) - 1]: _item}
    get_db_table('users').upsert(data, ['chat_id'])


def save_profile(_id, _field, _ans):  # _fields are 'gender' and 'age'
    data = {'chat_id': _id, _field: _ans}
    get_db_table('users').upsert(data, ['chat_id'])


def save_phone_number(_id, _phone):
    data = {'chat_id': _id, 'phone': _phone}
    get_db_table('users').upsert(data, ['chat_id'])


def clear_pre_session(_id):
    # rows = get_db_table('users').find(chat_id=_id)
    data = {'chat_id': _id}
    col_names = ['t1q' + str(i + 1) for i in range(10)]
    data.update(dict(zip(col_names, [None] * 10)))
    col_names = ['t1r' + str(i + 1) for i in range(5)]
    data.update(dict(zip(col_names, [None] * 5)))
    chat = 'chat_id'
    get_db_table('users').upsert(data, ['chat_id'])
    register_user(_id)


def delete_user(_id):
    get_db_table('users').delete(chat_id=_id)


def set_state(_id, _state_name):
    data = dict(chat_id=_id, state=_state_name)
    get_db_table('users').upsert(data, ['chat_id'])
    print "~~ state changed: %s" % str(data)


def save_test1_result(_id, res_list):
    col_names = ['t1r' + str(i + 1) for i in range(5)]
    data = {'chat_id': _id}
    data.update(dict(zip(col_names, res_list)))
    get_db_table('users').upsert(data, ['chat_id'])


def get_test1_result(_id):
    col_names = ['t1r' + str(i + 1) for i in range(5)]
    row = get_db_table('users').find_one(chat_id=_id)
    res = [row[i] for i in col_names]
    return res


def get_state(_id):
    row = get_db_table('users').find_one(chat_id=_id)
    if row is not None and 'state' in row.keys():
        return row['state']
    else:
        return 'Main'


def get_test1_answers(_id, size):
    # TODO check if the columns exist before reading it's value
    q_col_names = ["t1q{0}".format(i + 1) for i in range(size)]
    # q_col_names = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10']
    row = get_db_table('users').find_one(chat_id=_id)
    ans = []
    for q in q_col_names:
        if q in row.keys():
            ans.append(row[q])
    print ans
    return ans


def update_last_visit(_id):
    # time string format: "1464697276 16-05-30 14:23:53"
    ti = str(time.strftime("%s")) + " " + str(time.strftime("%y-%m-%d %H:%M:%S"))
    data = dict(chat_id=_id, last_visit=ti)
    get_db_table('users').upsert(data, ['chat_id'])


def print_table_contents(tab):
    db = db_if.get_db()
    table = db[tab]
    str_list = list()
    str_list.append("table " + tab + ":\n")

    for key in table.columns:
        str_list.append("{0}".format(key))
    str_list.append('\n' + '=' * 20 + '\n')

    for row in table:
        for val in row.itervalues():
            #  if isinstance(val, str):
            #       val = val.encode('utf-8')
            # str_list.append("{:<10}".format(str(val).decode('utf-8')))
            str_list.append("{0}".format(val))
        str_list.append('\n' + '-' * 20 + '\n')
    str_list.append('\n')
    return '\n'.join(str_list)


def delete_tables(cond):
    if cond:
        db = db_if.get_db()
        for tab in db.tables:
            db[tab].delete()
        return "subscribers list cleared"
    else:
        return "Hah, you are not admin"


def subscribe(_id):
    db = db_if.get_db()
    table = db['users']
    # TODO: handle duplication. if (id exist) update title return {"updated!" | time of subscription}
    table.insert(dict(chat_id=_id))
    return "chat_id '%s' successfully added" % (str(_id))


# return proper msg for duplication

def insert_batch_file(filename):
    db = db_if.get_db()
    table = db['events']
    infile = open(filename, 'r')
    for line in infile.readlines():
        line.splitlines(keepends=False)
        row = line.split(',')
        if len(row) == 4:
            table.insert(dict(action=row[0], value=row[1], date=row[2], time=row[3]))
        elif len(row) == 3:
            table.insert(dict(action=row[0], value=row[1], date=row[2]))
        else:
            pass
    print "successfully added"


def get_subscribers_name(cond):
    if cond:
        db = db_if.get_db()
        subs = []
        for row in db['users']:
            if 'title' in row:
                subs.insert(0, '- ' + str(row['title']))
        return 'Subscribed Groups:\n' + '\n'.join(list(set(subs)))
    else:
        return "Hah, you are not admin"


def get_subscribers_id():
    db = db_if.get_db()
    subs = []
    for row in db['users']:
        if 'group_id' in row:
            subs.insert(0, str(row['group_id']))
    return list(set(subs))


def get_membership_status(user_id):
    row = get_db_table('users').find_one(chat_id=user_id)
    membership = row['membership'] if 'membership' in row.keys() else 'free'
    transaction_id = row['transid'] if 'transid' in row.keys() else None
    return membership, transaction_id


def save_transaction(user_id, transid):
    get_db_table('users').upsert(dict(chat_id=user_id, transid=transid), ['chat_id'])


def set_membership(user_id, param):
    get_db_table('users').upsert(dict(chat_id=user_id, membership=param), ['chat_id'])


def get_user_data(user_id):
    row = get_db_table('users').find_one(chat_id=user_id)
    if row is not None:
        return False, dict(row)
    else:
        return True, dict(chat_id=user_id, state='Main')


def add_user(_id):
    data = dict(chat_id=_id)
    get_db_table('users').upsert(data, ['chat_id'])
    return len(get_db_table('users'))