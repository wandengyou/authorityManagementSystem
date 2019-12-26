import logging
from datetime import timedelta
from uuid import uuid4

from flask.sessions import SessionInterface, SessionMixin
from flask_limiter import Limiter
from flask_login import LoginManager, current_user
from flask_login import UserMixin, AnonymousUserMixin
# from flask_mongoengine import MongoEngine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from pymaid.conf import settings
from werkzeug.datastructures import CallbackDict
import ujson as json
from sqlalchemy import create_engine

from core.utils import get_ip


class RedisSession(CallbackDict, SessionMixin):

    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False


class RedisSessionInterface(SessionInterface):

    serializer = json
    session_class = RedisSession

    def __init__(self, redis, prefix='session:',
                 record_prefix='session:user:'):
        self.redis = redis
        self.prefix = prefix
        self.record_prefix = record_prefix

    def get_redis_expiration_time(self, app, session):
        if session.permanent:
            return app.permanent_session_lifetime
        return timedelta(days=1)

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            return self.session_class(sid=str(uuid4()), new=True)
        val = self.redis.get(self.prefix + sid)
        if val is not None:
            return self.session_class(self.serializer.loads(val), sid=sid)
        return self.session_class(sid=sid, new=True)

    def save_session(self, app, session, response):
        skey = self.prefix + session.sid
        domain = self.get_cookie_domain(app)

        if not session:
            self.redis.delete(skey)
            if session.modified:
                response.delete_cookie(app.session_cookie_name, domain=domain)
            return

        redis_exp = self.get_redis_expiration_time(app, session)
        cookie_exp = self.get_expiration_time(app, session)
        httponly = self.get_cookie_httponly(app)
        sec = int(redis_exp.total_seconds())

        pipe = self.redis.pipeline()
        pipe.setex(skey, sec, self.serializer.dumps(session))
        if 'user_id' in session:
            pipe.get(self.record_prefix + str(session['user_id']))
            pipe.setex(self.record_prefix + str(session['user_id']), sec, skey)
        resp = pipe.execute()
        # removed previous session
        if len(resp) > 1 and skey != resp[1]:
            self.redis.delete(resp[1])

        response.set_cookie(
            app.session_cookie_name, session.sid,
            expires=cookie_exp, httponly=httponly, domain=domain
        )


class SessionUser(UserMixin):

    def __init__(self, user_id, username, user_permissions, user_type,
                 **kwargs):
        self.id = self.user_id = int(user_id)
        self.username = username
        self.permissions = user_permissions
        self.user_type = user_type
        self.kwargs = kwargs

    def __str__(self):
        return (u'<%d: %s>' % (self.user_id, self.username)).encode('utf-8')
    __repr__ = __str__

    def __unicode__(self):
        return u'<%d: %s>' % (self.user_id, self.username)


class AnonymousUser(AnonymousUserMixin):

    def __str__(self):
        return u'AnonymousUser'
    __unicode__ = __repr__ = __str__


login_manager = LoginManager()
db = SQLAlchemy()
#engine = create_engine(settings.get('SQLALCHEMY_DATABASE_URI', ns='storage'))
#session_class = sessionmaker(bind=engine)
#session = session_class()

# session_interface = RedisSessionInterface(get_cache_redis())


def limitation():
    if hasattr(current_user, 'user_id'):
        return str(current_user.user_id)
    return get_ip()


# limiter = Limiter(
#     default_limits=settings.get('LIMITER_DEFAULT_LIMITS', ns='flask'),
#     key_func=limitation,
# )

class ModelManager:
    def __init__(
        self,
        model,
        filters=None,
        order_by=None,
        page_size=None,
        page_num=None,
        serialize=True,
    ):
        if filters is None:
            filters = dict()

        self.model = model
        self.filters = filters
        self.page_size = page_size
        self.page_num = page_num
        self.records = []
        self.records_total = 0
        self.order_by = order_by
        self.serialize = serialize

    def analysis_order_by(self):
        order_by_list = []
        if self.order_by:
            for key, value in self.order_by.items():
                if hasattr(self.model, key):
                    if value == 'desc':
                        order_by_list.append(getattr(self.model, key).desc())
                    else:
                        order_by_list.append(getattr(self.model, key).asc())
        return order_by_list

    def query(self, **kwargs):
        try:
            qs = db.session.query(self.model)
            if kwargs:
                self.records = qs.filter_by(**kwargs).all()
            elif self.filters:
                self.records = qs.filter_by(**self.filters).all()
            else:
                self.records = qs.all()
        except Exception as e:
            logging.exception(e)
            db.session.rollback()
        return self.records

    def query_one_by_filter(self, **kwargs):
        try:
            qs = db.session.query(self.model)
            if kwargs:
                self.model = qs.filter_by(**kwargs).one_or_none()
            else:
                self.model = qs.filter_by(**self.filters).one_or_none()
        except Exception as e:
            logging.exception(e)
            db.session.rollback()
        return self.model

    def query_by_id(self, id):
        try:
            self.model = db.session.query(self.model).get(id)
        except Exception as e:
            logging.exception(e)
            db.session.rollback()
        return self.model

    def query_by_ids(self, ids):
        try:
            self.records = (
                db.session.query(self.model)
                .filter(self.model.id.in_(ids))
                .all()
            )
        except Exception as e:
            logging.exception(e)
            db.session.rollback()
        return self.records

    def delete_by_filter(self, **kwargs):
        try:
            qs = db.session.query(self.model)
            if kwargs:
                qs.filter_by(**kwargs).delete()
            else:
                qs.filter_by(**self.filters).delete()
            return True
        except Exception:
            db.session.rollback()
            raise

    def update_by_filter(self, **kwargs):
        try:
            db.session.query(self.model).filter_by(**self.filters).update(
                kwargs
            )
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    def paginate(self):
        try:
            qs = db.session.query(self.model)
            if self.order_by:
                if self.filters:
                    query_result = qs.filter_by(**self.filters).order_by(
                        *self.analysis_order_by()
                    )
                else:
                    query_result = qs.order_by(*self.analysis_order_by())
            else:
                if self.filters:
                    query_result = qs.filter_by(**self.filters)
                else:
                    query_result = qs
            self.records_total = query_result.count()
            if self.records_total > 0:
                if self.page_num > 0:
                    self.records = (
                        query_result.limit(self.page_size)
                        .offset((self.page_num - 1) * self.page_size)
                        .all()
                    )
            if self.serialize and self.records:
                self.records = [o.to_dict() for o in self.records]
        except Exception as e:
            logging.exception(e)
            db.session.rollback()
        return self.records, self.records_total

    def get_fields(self):
        fields = [
            name
            for name in dir(self.model)
            if not name.startswith('__') and not callable(self.model, name)
        ]
        return fields

    def save(self):
        try:
            db.session.add(self.model)
            db.session.commit()
            return self.model
        except Exception as e:
            db.session.rollback()
            raise e

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self.model, attr, value)
        try:
            db.session.commit()
            return self.model
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        try:
            db.session.delete(self.model)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
