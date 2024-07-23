from django import template
from menu.models import MenuItem

register = template.Library()

@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')
    items_dict = {item.id: item for item in items}
    root_items = [item for item in items if item.parent is None]
    for item in items:
        if item.parent:
            parent = items_dict[item.parent.id]
            if not hasattr(parent, 'children'):
                parent.children = []
            parent.children.append(item)
    active_item = find_active_item(items, request.path)
    return {'menu_items': root_items, 'active_item': active_item}

def find_active_item(items, current_url):
    for item in items:
        if item.get_url() == current_url:
            return item
    return None