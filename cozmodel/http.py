from cozdata import factory as dao_factory


def init_json_post(username: str, password: str) -> tuple:
    ldao = dao_factory.get_dao()
    ldao.connect()
    logged_in = ldao.login(username, password)
    if not logged_in:
        ldao.disconnect()
    return ldao, logged_in
