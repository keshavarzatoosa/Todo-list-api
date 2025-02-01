from rest_framework.throttling import UserRateThrottle, SimpleRateThrottle


class CustomUserRateThrottle(UserRateThrottle):
    scope = 'custom_user'


class CustomRateThrottle(SimpleRateThrottle):
    scope = 'default'

    def get_cache_key(self, request, view):
        # if not request.user.is_authenticated:
        #     return None
        # if not request.user.is_authenticated:
        #     return self.cache_format % {'scope': 'anon', 'ident': self.get_ident(request)}
        if request.user.is_superuser:
            return self.cache_format % {'scope': 'superuser', 'ident': request.user.pk}
        return self.cache_format % {'scope': 'user', 'ident': request.user.pk}