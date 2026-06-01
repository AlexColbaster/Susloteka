from io import BytesIO

from openpyxl import Workbook
from django.apps import apps
from django.http import HttpResponse, Http404


def export_model_to_xlsx(app_label, model_name):
    model = apps.get_model(app_label, model_name)
    if model is None:
        raise Http404('Модель не найдена')

    wb = Workbook()
    ws = wb.active
    ws.title = model._meta.verbose_name_plural[:31]

    fields = [f for f in model._meta.fields if not f.many_to_many and not f.one_to_many]
    ws.append([f.verbose_name for f in fields])

    for obj in model.objects.all():
        row = []
        for field in fields:
            value = getattr(obj, field.name)
            if hasattr(value, 'isoformat'):
                value = value.isoformat(sep=' ', timespec='seconds')
            row.append('' if value is None else str(value))
        ws.append(row)

    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)
    response = HttpResponse(
        stream.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename="{model._meta.model_name}.xlsx"'
    return response
