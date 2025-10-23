from django.contrib import admin
from unidades.models import Unidade
from usuarios.models import Usuario


@admin.register(Unidade)
class PorteirosAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "proprietario":
            kwargs["queryset"] = Usuario.objects.filter(
                perfil=Usuario.Perfil.PROPRIETARIO
            )
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
