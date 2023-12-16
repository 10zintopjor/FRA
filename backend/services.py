import database as _dt


def create_database():
    return _dt.Base.metadata.create_all(bind = _dt.engine)


create_database()