import os

import dataset

_db_directory = "dbase_dir/"  # os.path.expanduser('~') + "/siniobot/"  # "dbase_dir/"
_db_filename = 'data.db'
_db_url = "sqlite:///" + _db_directory + _db_filename


def get_db():
    if inspect():
        pass
    else:
        create_db()
    _db = dataset.connect(_db_url)
    return _db


def inspect():
    if os.path.exists(_db_directory) & os.path.isfile(_db_directory + _db_filename):
        return True
    else:
        return False


def create_db():
    if not os.path.exists(_db_directory):
        os.mkdir(_db_directory)
    db = dataset.connect(_db_url)
    # db.create_table('groups')
    # db['actions'].create_column('action')
    print "table created: %s" % 'groups'


def create_table():
    get_db().create_table('users')


if __name__ == "__main__":
    get_db()
