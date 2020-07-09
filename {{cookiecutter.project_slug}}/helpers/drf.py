from collections import OrderedDict
from typing import Dict, Union, List, Any
{%- if cookiecutter.use_sentry == 'y' %}
from sentry_sdk import capture_exception
{%- endif %}
from django.conf import settings
from django.utils.translation import gettext_lazy as _
{%- if cookiecutter.use_drf_yasg == 'y' %}
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
{%- endif %}
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.pagination import LimitOffsetPagination as BaseLimitOffsetPagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param
from rest_framework.views import exception_handler


class LimitOffsetPagination(BaseLimitOffsetPagination):
    default_limit = 30
    max_limit = 100

    def get_first_link(self):
        url = self.request.build_absolute_uri()
        offset = 0
        first_link = replace_query_param(url, self.offset_query_param, offset)
        first_link = replace_query_param(first_link, self.limit_query_param, self.limit)
        return first_link

    def get_last_link(self):
        url = self.request.build_absolute_uri()
        offset = self.count - self.limit if (self.count - self.limit) >= 0 else 0
        last_link = replace_query_param(url, self.offset_query_param, offset)
        last_link = replace_query_param(last_link, self.limit_query_param, self.limit)
        return last_link

    def get_paginated_response(self, data):
        return Response({
            'meta': {'count': self.count},
            'links': {
                'first': self.get_first_link(),
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'last': self.get_last_link(),
            },
            'data': data,
        })


def _generate_errors_from_list(data: List, **kwargs) -> List:
    errors = []
    source = kwargs.get('source')
    status_code = kwargs.get('status_code', 0)
    for value in data:
        if isinstance(value, str):
            new_error = {'detail': value, 'source': source, 'status': status_code}
            errors.append(new_error)
        elif isinstance(value, list):
            errors.extend(_generate_errors_from_list(value, **kwargs))
        elif isinstance(value, dict):
            errors.extend(_generate_errors_from_dict(value, **kwargs))
    return errors


def _generate_errors_from_dict(data: Dict, **kwargs) -> List:
    errors = []
    source = kwargs.get('source')
    status_code = kwargs.get('status_code', 0)
    for key, value in data.items():
        source_val = f'{source}.{key}' if source else key
        if isinstance(value, str):
            new_error = {'detail': value, 'source': source_val, 'status': status_code}
            errors.append(new_error)
        elif isinstance(value, list):
            kwargs['source'] = source_val
            errors.extend(_generate_errors_from_list(value, **kwargs))
        elif isinstance(value, dict):
            kwargs['source'] = source_val
            errors.extend(_generate_errors_from_dict(value, **kwargs))
    return errors


def custom_exception_handler(exc: Any, context: Any) -> Response:
    response = exception_handler(exc, context)

    if response is not None:
        errors = []
        data = response.data
        if isinstance(data, dict):
            errors.extend(_generate_errors_from_dict(data, status_code=response.status_code))
        elif isinstance(data, list):
            errors.extend(_generate_errors_from_list(data, status_code=response.status_code))
        response.data = {'errors': errors}
    else:
        if settings.IS_PROD:
            { % - if cookiecutter.use_sentry == 'y' %}
            capture_exception(exc)
            { % - else %}
            pass
            { % - endif %}
        else:
            raise exc
        exc = APIException(exc)
        response = exception_handler(exc, context)
        response.data = {'errors': [{'detail': _('Internal Server Error'), 'source': None, 'status': response.status_code}]}

    return response

{%- if cookiecutter.use_drf_yasg == 'y' %}

def base_response(data: Union[Dict, List, None] = None, **kwargs) -> Response:
    return Response({'data': data or {}}, **kwargs)


def base_response_empty_scheme(description: str = '') -> openapi.Response:
    description = description or _('An empty object returns.')
    return openapi.Response(description, openapi.Schema(type=openapi.TYPE_OBJECT, description=_('An empty object')))


def errors_response_scheme(description: str) -> openapi.Response:
    return openapi.Response(description, openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=OrderedDict((
            ('errors', openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_OBJECT, properties=OrderedDict(
                    (('detail', openapi.Schema(type=openapi.TYPE_STRING, description=_('Detail message.'))),
                     ('source', openapi.Schema(type=openapi.TYPE_STRING, description=_(f'Source field. {settings.SERIALIZER_FIELD_NULLABLE_HELP_TEXT}'))),
                     ('status', openapi.Schema(type=openapi.TYPE_INTEGER, description=_('HTTP Status Code'))),)
                ), required=['detail', 'source', 'status']),
                description=_('Error Information')
            )),
        )),
        required=['errors']
    ))


class BaseResponseAutoSchema(SwaggerAutoSchema):
    def get_responses(self) -> openapi.Responses:
        responses = super().get_responses()

        if not responses.keys():
            return responses

        status_code = list(responses.keys())[0]
        if status.HTTP_200_OK <= int(status_code) < status.HTTP_300_MULTIPLE_CHOICES:
            if status.HTTP_204_NO_CONTENT == int(status_code):
                return responses
            else:
                responses[status_code]['schema'] = {'allOf': [
                    openapi.Schema(type=openapi.TYPE_OBJECT, properties={'data': responses[status_code]['schema']}, description=_('Data Information')),
                ]}
        else:
            responses[status_code]['schema'] = {'allOf': [
                openapi.Schema(type=openapi.TYPE_OBJECT, properties={'errors': responses[status_code]['schema']}, description=_('Error Information')),
            ]}

        return responses


class LimitOffsetPaginationResponseAutoSchema(SwaggerAutoSchema):
    def get_responses(self) -> openapi.Responses:
        responses = super().get_responses()

        if not responses.keys():
            return responses

        status_code = list(responses.keys())[0]
        if status.HTTP_200_OK <= int(status_code) < status.HTTP_300_MULTIPLE_CHOICES:
            if status.HTTP_204_NO_CONTENT == int(status_code):
                responses[status_code]['schema'] = {'allOf': []}
            else:
                responses[status_code]['schema'] = {'allOf': [
                    openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={'data': responses[status_code]['schema'],
                                    'links': openapi.Schema(
                                        title=_('Links'),
                                        type=openapi.TYPE_OBJECT,
                                        required=['first', 'last'],
                                        properties=OrderedDict((
                                            ('first', openapi.Schema(type=openapi.TYPE_STRING, title=_('Link to first object'), read_only=True, format=openapi.FORMAT_URI)),
                                            ('last', openapi.Schema(type=openapi.TYPE_STRING, title=_('Link to last object'), read_only=True, format=openapi.FORMAT_URI)),
                                            ('next', openapi.Schema(type=openapi.TYPE_STRING, title=_('Link to next object'), read_only=True, format=openapi.FORMAT_URI)),
                                            ('prev', openapi.Schema(type=openapi.TYPE_STRING, title=_('Link to prev object'), read_only=True, format=openapi.FORMAT_URI))
                                        ))),
                                    'meta': openapi.Schema(
                                        title=_('Meta of result with pagination count'),
                                        type=openapi.TYPE_OBJECT,
                                        required=['count'],
                                        properties=OrderedDict((('count', openapi.Schema(type=openapi.TYPE_INTEGER, title=_('Number of results on page.'),)),))
                                    )},
                        description=_('Data Information')),
                ]}
        else:
            responses[status_code]['schema'] = {'allOf': [
                openapi.Schema(type=openapi.TYPE_OBJECT, properties={'errors': responses[status_code]['schema']}, description=_('Error Information')),
            ]}

        return responses
{%- endif %}
