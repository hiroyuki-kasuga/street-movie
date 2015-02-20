# coding: utf-8

import logging
from functools import wraps
from datetime import datetime
import re
import types

logger = logging.getLogger(__name__)


def add_log():
    def _func(func):
        def __func(request, *argv, **kwargv):
            logger.info("=========================")
            logger.info("START REQUEST => %s name => %s" % (request.path, func.__name__))
            start = datetime.now()

            d = normal_dict(request.META)
            k = d.keys()
            k.sort(lambda x, y : cmp(x, y))
            logger.info("------------------------START META")
            for x in k:
                logger.info("%s => %s" % (x, d[x]))

            logger.info("------------------------END META")

            d = normal_dict(request.POST or request.GET)
            # d.update(normalDict(request.META))
            k = d.keys()
            k.sort(lambda x, y: cmp(x, y))
            logger.info("------------------------START RequestParams")
            for x in k:
                logger.info("%s => %s" % (x, d[x]))

            logger.info("------------------------END RequestParams")

            f = func(request, *argv, **kwargv)

            logger.info("------------------------START Response")
            if hasattr(f, "status_code"):
                logger.info("Response Code => %s" % f.status_code)
            if hasattr(f, "content"):
                logger.info(f.content)
            logger.info("------------------------END Response")
            end = datetime.now()
            logger.info("END REQUEST => %s name => %s Interval => %s" % (request.path, func.__name__, end - start))
            logger.info("=========================")
            return f

        return __func

    return _func


def normal_dict(request_data):
    l = lambda x: (isinstance(x, list) and len(x) > 0 ) and x[0] or x
    return dict((k, l(v)) for k, v in request_data.iteritems())


def interceptor(clazz):
    # 隠しプロパティか名前から判断する
    def _is_property_hidden(property_name):
        hidden_property_name_pattern = '^_'
        regex_pattern = re.compile(hidden_property_name_pattern)
        return True if regex_pattern.match(property_name) is not None else False

    # プロパティの型がメソッドか確認する
    def _is_property_method(property_refs):
        property_type = type(property_refs)
        return True if property_type is types.MethodType else False

    # クラスが持つプロパティ一覧を取得する
    for property_name in dir(clazz):
        # 隠しプロパティ (名前が '_' から始まる) だったら無視する
        if _is_property_hidden(property_name):
            continue
            # プロパティがメソッドでなかったら無視する
        property_refs = getattr(clazz, property_name)
        if not _is_property_method(property_refs):
            continue
            # 'interrupt' 関数でラップする
        setattr(clazz, property_name, handle_log(property_refs))
        # メソッドをラップしたクラスを返す
    return clazz


def handle_log(function):
    @wraps(function)
    def _func(self, *args, **kw):
        logger.info("------------------------START Class => %s Method => %s" % (function.im_class, function.__name__))
        start = datetime.now()
        from pprint import pformat

        logger.info("------------------------START function args")
        for arg in args:
            logger.info("------------------------args => {0}".format(pformat(arg)))
        logger.info("------------------------END function args")
        logger.info("------------------------START function kwargs")
        for k, v in kw.items():
            logger.info("------------------------{0} => {1}".format(pformat(k), pformat(v)))
        logger.info("------------------------END function kwargs")
        f = function(self, *args, **kw)
        end = datetime.now()
        logger.info("------------------------END Class => %s Method => %s Interval => %s" % (
            function.im_class, function.__name__, end - start))
        return f

    return _func