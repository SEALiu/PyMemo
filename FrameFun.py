import DBFun


def init_lib(libraries, library_id):
    conn = DBFun.connect_db('db_pymemo.db')
    conn.text_factory = str
    select_sql = "SELECT * FROM library"
    cursor = DBFun.select(conn, select_sql)
    result_list = cursor.fetchall()
    DBFun.close_db(conn)
    libraries.clear()
    library_id[:] = []
    for rows in result_list:
        library_id.append(rows[0])
        libraries[rows[0]] = rows[1:]


def add_lib(lib_dic, key, value):
    for i in range(len(key)):
        for j in range(len(value)):
            lib_dic[key[i]] = value[j]
    pass


def del_lib(lib_dic, key):
    del lib_dic[key]

# if __name__ == '__main__':
#     libraries = {}
#     library_id = []
#     init_lib(libraries, library_id)
#
#     print libraries
#
#     add_lib(libraries, ['000'], ['lib_name', 'lib_desc'])