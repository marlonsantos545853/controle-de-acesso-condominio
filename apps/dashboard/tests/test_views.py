from django.test import TestCase
from django.urls import reverse_lazy
from django.utils import timezone
from model_mommy import mommy
from visitantes.models import Visitantes
from usuarios.models import Usuario


class IndexViewTests(TestCase):
    def setUp(self):
        # Cria usuário autenticado
        self.user = mommy.make(Usuario, email="teste@exemplo.com", perfil=Usuario.Perfil.PORTEIRO)
        self.user.set_password("123456")
        self.user.save()

        # Faz login
        self.client.login(email=self.user.email, password="123456")

    def test_index_retorna_status_200(self):
        response = self.client.get(reverse_lazy("index"))  # ajuste para o nome real da sua URL
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_index_contexto_com_visitantes(self):
        # Cria visitantes em diferentes status
        mommy.make(Visitantes, status="AGUARDANDO")
        mommy.make(Visitantes, status="EM_VISITA")
        mommy.make(Visitantes, status="FINALIZADO")

        response = self.client.get(reverse_lazy("index"))
        context = response.context

        self.assertEqual(context["visita_aguardando"], 1)
        self.assertEqual(context["visita_em_andamento"], 1)
        self.assertEqual(context["visita_finalizada"], 1)

    # def test_index_total_mes_somente_do_mes_atual(self):
    #     agora = timezone.now()

    #     # visitante do mês atual
    #     mommy.make(Visitantes, horario_chegada=agora)

    #     # visitante de mês diferente
    #     mommy.make(
    #         Visitantes,
    #         horario_chegada=agora.replace(month=agora.month - 1)
    #     )

    #     mommy.make(
    #         Visitantes,
    #         horario_chegada=agora.replace(month=agora.month - 1)
    #     )

    #     # horario_chegada=agora.replace(month=agora.month - 1)
    #     # self.assertEqual(agora, horario_chegada)
    #     response = self.client.get(reverse_lazy("index"))
    #     self.assertEqual(response.context["total_mes"], 1)

    def test_index_contexto_contem_perfil(self):
        response = self.client.get(reverse_lazy("index"))
        self.assertEqual(response.context["perfil"], self.user.perfil)
