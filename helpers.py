class Helpers:

    def __init__(self, app):
        @app.context_processor
        def helpers_personalizados():
            return {'javascript': helper_javascript}

def helper_javascript(url, basepath='/static/js/', *k, **kv):
    return "<script src='{basepath}{url}' type='text/javascript'></script>".format(url=url, basepath=basepath)
