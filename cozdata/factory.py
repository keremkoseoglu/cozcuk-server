from cozdata import dao, hard_code


def get_dao() -> dao.DataAccessObject:
    return hard_code.HardCode()
