from django import template

register = template.Library()


@register.filter(name='asia_hcm_time')
def asia_hcm_time(time):
    date = str(time).split()[0]
    time = str(time).split()[1]
    date_splitted = date.split('-')
    time_splitted = time.split(':')
    return time_splitted[0] + ':' + time_splitted[1] + \
           ' ' + date_splitted[2] + '-' + date_splitted[1] + '-' + date_splitted[0]