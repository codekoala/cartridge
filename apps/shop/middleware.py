
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.conf import settings

from shop.settings import SSL_ENABLED, FORCE_HOST


class SSLRedirect(object):

	def process_request(self, request):
		"""
		if SHOP_FORCE_HOST is set and is not the current host, redirect to it
		if SHOP_SSL_ENABLED is True, ensure checkout views are accessed over 
		https and all other views are accessed over http
		"""
		if FORCE_HOST and request.get_host().split(":")[0] != FORCE_HOST:
			return http.HttpResponsePermanentRedirect("http://%s%s" % 
				(FORCE_HOST, request.get_full_path()))			
		if SSL_ENABLED and not getattr(settings, "DEV_SERVER", False):
			url = "%s%s" % (request.get_host(), request.get_full_path())
			if request.path in map(reverse, ("shop_checkout", "shop_complete")):
				if not request.is_secure():
					return HttpResponseRedirect("https://%s" % url)
			elif request.is_secure():
				return HttpResponseRedirect("http://%s" % url)

