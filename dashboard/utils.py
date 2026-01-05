from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import JsonResponse, HttpResponse

def render_to_pdf(template, context):
    template = get_template(template)
    html  = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None