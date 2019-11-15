from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator

register = template.Library()

@register.simple_tag
def column_header(table, column, text):
    selected = 'style="color: #D84A24"'
    if table.sort == column:
        sort = '-' + column
        arrow = '&darr;'
    elif table.sort == ('-' + column):
        sort = column
        arrow = '&uarr;'
    else:
        sort = '-' + column
        arrow = ''
        selected = ''

    params = dict(table.request.GET)
    params['sort'] = [sort]
    params_str = '&'.join( (k + '=' + v[0]) for k,v in params.items())

    return format_html('<th><a href="?{}"><span {}>{} {}</span></a></th>\n',
        params_str,
        mark_safe(selected),
        mark_safe(arrow),
        text
    )

@register.simple_tag
def table_footer(table):
    if table.show_all or table.paginator.num_pages == 1:
         return ''

    params = dict(table.request.GET)

    footer = '<p class="paginator">'
    for page in table.paginator.page_range:
        if page == table.page:
            footer += '<span class="this-page">%d</span>\n' % page
        else:
            params['page'] = [str(page)]
            params_str = '&'.join( (k + '=' + v[0]) for k,v in params.items())
            footer += '<a href="?%s">%d</a>\n' % (params_str, page)

    footer += ' Total: %d\n' % table.paginator.count

    del params['page']
    params['show-all'] = '1'
    params_str = '&'.join( (k + '=' + v[0]) for k,v in params.items())
    footer += ' | <a href="?%s">Show all</a>' % params_str
    footer += '</p>'
    return mark_safe(footer)


class Table:
    def __init__(self, request, queryset, default_sort, default_page_size=25):
        self.request = request
        self.sort = request.GET.get('sort', default_sort)
        self.page_size = int(request.GET.get('page-size', default_page_size))
        self.page = int(request.GET.get('page', 1))
        self.results = queryset.order_by(self.sort)
        self.show_all = request.GET.get('show-all', False)

        if not self.show_all:
            # Paginate results unless explicitely turned off
            self.paginator = Paginator(self.results, self.page_size)
            self.results = self.paginator.page(self.page)
