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

    def delete_model(self, request, obj):
        pat_na_vod = obj.patuvanja_mtm.all()

        ost_vodachi = (Vodach.objects
                        .exclude(pk=obj.pk)
                        .order_by('patuvanja_mtm')
                        )

        eligibility_flag = False
        promeneti_vodachi = []
        for vodach in ost_vodachi:
            vod_cena_kap = 50000 - vodach.vkupna_cena
            vod_pat_kap = 5 - vodach.patuvanja_mtm.count()
            for patuvanje in pat_na_vod:
                if patuvanje.cena <= vod_cena_kap and vod_pat_kap <= 5:
                    if not eligibility_flag:
                        eligibility_flag = True
                    vodach.patuvanja_mtm.add(patuvanje)
                    vod_cena_kap -= patuvanje.cena
                    vod_pat_kap += 1
                else:
                    break

            if eligibility_flag:
                promeneti_vodachi.append(vodach)
        
        if not promeneti_vodachi:
            self.message_user(request, "Ne postojat vodachi na koi mozhe da im se prenesat patuvanjata.")
            return
        
        for vodach in promeneti_vodachi:
            vodach.save()

        super().delete_model(request, obj)


admin.site.register(Patuvanje, PatuvanjeAdmin)
admin.site.register(Vodach, VodachAdmin)