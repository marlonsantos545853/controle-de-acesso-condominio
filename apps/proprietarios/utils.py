import logging
from django.db.models import Model


logger = logging.getLogger("proprietarios.logs")

def log_model_creation(request, form):
    """
    Registra a criação de uma nova instância de modelo.
    """
    instance = form.instance
    model_name = instance.__class__.__name__

    logger.info(f"Usuário '{request.user}' criou {model_name} ID {instance.pk}.")


def log_model_update(request, form):
    """
    Registra as alterações em uma instância de modelo existente.
    """
    instance = form.instance
    model_name = instance.__class__.__name__

    # Se nada foi alterado, apenas registra a tentativa
    if not form.changed_data:
        logger.info(
            f"Usuário '{request.user}' salvou {model_name} ID {instance.pk} sem alterações."
        )
        return

    # Preparar dados para o log de alteração
    changed_fields = {}
    for field in form.changed_data:
        new_value = form.cleaned_data.get(field)

        # Lidar com campos de relacionamento
        if isinstance(new_value, Model):
            new_value = new_value.pk

        changed_fields[field] = str(new_value)

    # Registrar o log
    logger.info(f"Usuário '{request.user}' alterou {model_name} ID {instance.pk}.")
    logger.info(f"Novos valores: {changed_fields}")
