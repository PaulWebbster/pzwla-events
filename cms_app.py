#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class ZawodyApp(CMSApp):
    name = _("Przegladarka zawodow")  # give your app a name, this is required
    urls = ["zawody.urls"]  # link your app to url configuration(s)
    app_name = "zawody"

apphook_pool.register(ZawodyApp)  # register your app