from django.contrib import admin
from porteiros.models import Porteiros
from usuarios.models import Usuario


@admin.register(Porteiros)
class PorteirosAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "usuario":
            kwargs["queryset"] = Usuario.objects.filter(perfil=Usuario.Perfil.PORTEIRO)
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
