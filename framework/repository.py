from infrastructure.databases.SQL.pg_alchemy  import SqlDB


class GenericRepository:
    def __init__(self, model_class):
        self.db = SqlDB().get_db()
        if self.db is None:
            raise ValueError("Database not initialized")
        self.model_class = model_class

    def create(self, item):
        session = self._create_a_session()
        try:
            session.add(item)
            session.commit()
            session.refresh(item)
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
        return item

    def delete(self, item):
        session = self._create_a_session()
        try:
            session.delete(item)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
        return item

    def get_by_id(self, id: int):
        session = self._create_a_session()
        try:
            item = session.query(self.model_class)\
                    .filter(self.model_class.id == id)\
                    .first()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
        return item

    def get_all(self, page: int):
        session = self._create_a_session()
        offset = (page - 1) * 100
        limit = page * 100
        try:
            items = session.query(self.model_class)\
                .offset(offset)\
                .limit(limit)\
                .all()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
        return items

    def update(self, item):
        session = self._create_a_session()
        try:
            session.merge(item)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
        return item

    def _create_a_session(self):
        if self.db is None:
            raise ValueError("Database not initialized")
        session = self.db.get_session()
        if session is None:
            raise ValueError(
                "An error occurred while connecting to the database")
        return session
