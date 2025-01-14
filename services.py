from sqlmodel import Session, select

from src.database import engine


class BaseService:
    model = None

    @classmethod
    def get_all(cls, order_by=None, **filter_by):
        with Session(engine) as session:
            query = select(cls.model).filter_by(**filter_by)
            if order_by is not None:
                query = query.order_by(order_by)
            result = session.exec(query)
            return result.all()


    @classmethod
    def get_one_or_none(cls, **filter_by):
        with Session(engine) as session:
            query = select(cls.model).filter_by(**filter_by)
            result = session.exec(query)
            return result.one_or_none()


    @classmethod
    def get_one_by_id(cls, model_id: int):
        with Session(engine) as session:
            query = select(cls.model).filter_by(id=int(model_id))
            result = session.exec(query)
            return result.one_or_none()


    @classmethod
    def create(cls, data):
        with Session(engine) as session:
            data_dict = data.model_dump()
            instance = cls.model(**data_dict)
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance


    @classmethod
    def delete(cls, model_id: int):
        with Session(engine) as session:
            query = select(cls.model).filter_by(id=int(model_id))
            result = session.exec(query)
            instance = result.one_or_none()
            if instance:
                session.delete(instance)
                session.commit()
                return {"result": True}


    @classmethod
    def update(cls, model_id: int, update_data):
        with Session(engine) as session:
            query = select(cls.model).filter_by(id=int(model_id))
            result = session.exec(query)
            instance = result.one_or_none()
            if instance:
                for key, value in update_data.model_dump().items():
                    setattr(instance, key, value)
                session.commit()
                session.refresh(instance)
                return instance
            else:
                raise Exception('No such instance')


    @classmethod
    def patch(cls, model_id: int, update_data):
        with Session(engine) as session:
            query = select(cls.model).filter_by(id=int(model_id))
            result = session.exec(query)
            instance = result.one_or_none()
            if instance:
                for key, value in update_data.model_dump(exclude_unset=True).items():
                    setattr(instance, key, value)
                session.commit()
                session.refresh(instance)
                return instance
            else:
                raise Exception('No such instance')
