from django.contrib import admin
from django.db.models import Count
from .models import Patuvanje, Vodach
# Register your models here.

class PatuvanjeAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj = None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        if obj:
            related_vodachi = Vodach.objects.filter(patuvanja_mtm = obj, user = request.user)
            return related_vodachi.exists()
        return super().has_change_permission(request, obj)

class VodachAdmin(admin.ModelAdmin):
    list_display = ('ime', 'vkupna_cena')
    readonly_fields = ('vkupna_cena',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.annotate(pat_count=Count('patuvanja_mtm')).filter(pat_count__lt=3)
        
        vodachi = Vodach.objects.filter(patuvanja_mtm__isnull=False).filter(patuvanja_mtm__related_to=request.user).values_list('patuvanja_mtm', flat = True)
        return qs.filter(pk__in=vodachi)
    
    def has_view_permission(self, request, obj = None):
        return True

admin.site.register(Patuvanje, PatuvanjeAdmin)
admin.site.register(Vodach, VodachAdmin)