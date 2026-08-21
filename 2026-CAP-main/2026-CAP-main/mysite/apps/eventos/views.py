from datetime import datetime

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from apps.calendarios.models import Calendario
from apps.eventos.models import Evento


@login_required
def criar_evento(request):
    if request.method == 'POST':

        titulo = request.POST.get('titulo', '').strip()
        data = request.POST.get('data')
        inicio = request.POST.get('inicio')
        fim = request.POST.get('fim')
        descricao = request.POST.get('descricao', '').strip()
        calendario = Calendario.objects.filter(
            usuarios=request.user,
            turma=None
        ).first()

        if not calendario:
            calendario = Calendario.objects.create(
                nome='Calendário geral',
                descricao='Calendário geral do usuário'
            )

            calendario.usuarios.add(request.user)
        if titulo and data and inicio and fim:

            try:
                inicio_dt = datetime.fromisoformat(
                    f'{data}T{inicio}'
                )
                fim_dt = datetime.fromisoformat(
                    f'{data}T{fim}'
                )
                evento = Evento(
                    nome=titulo,
                    conteudo=descricao,
                    inicio=inicio_dt,
                    fim=fim_dt,
                    calendario=calendario,
                )
                evento.full_clean()
                evento.save()
            except (ValueError, ValidationError):
                pass
    return redirect('inicio')
