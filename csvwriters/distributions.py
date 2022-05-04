from csv import DictWriter
import yaml
import os
from urllib.parse import urlparse

__location__ = os.path.realpath(os.path.join(
    os.getcwd(),
    os.path.dirname(__file__))
)

fieldnames_distribution = [
    "distribution_id",
    "format",
    "media_type",
    "download_url",
]

terms_of_use_mapping = {
    'NonCommercialAllowed-CommercialAllowed-ReferenceNotRequired': 'open',
    'NonCommercialAllowed-CommercialAllowed-ReferenceRequired': 'by',
    'NonCommercialAllowed-CommercialWithPermission-ReferenceNotRequired': 'ask',
    'NonCommercialAllowed-CommercialWithPermission-ReferenceRequired': 'by_ask',
    'ClosedData': 'closed',
}


class FormatMappingNotLoadedError(Exception):
    pass


def ogdch_get_format_mapping():
    """reads in the format mapping from a yaml file"""
    try:
        mapping_path = os.path.join(__location__, 'mapping.yaml')
        with open(mapping_path, 'r') as format_mapping_file:
            format_mapping = yaml.safe_load(format_mapping_file)
            reverse_format_mapping = {}
            for key, format_list in format_mapping.items():
                for format in format_list:
                    reverse_format_mapping[format] = key
    except (IOError, yaml.YAMLError) as exception:
        raise FormatMappingNotLoadedError(
            'Loading Format-Mapping from Path: (%s) '
            'failed with Exception: (%s)'
            % (mapping_path, exception)
        )

    return format_mapping, reverse_format_mapping


format_mapping, reverse_format_mapping = ogdch_get_format_mapping()


def distribution_writer(datasets):
    rights_set = set()
    distribution_to_rights = []
    format_set = set()
    distribution_to_format = []
    with open('distributions.csv', "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames_distribution)
        writer.writeheader()
        for dataset in datasets:
            if dataset.get('resources'):
                for resource in dataset.get('resources'):
                    distribution_id = resource.get('id')
                    writer.writerow({
                        'distribution_id': distribution_id,
                        'format': resource.get('format'),
                        'media_type': resource.get('media_type'),
                        'download_url': resource.get('download_url'),
                    })
                    rights = resource.get('rights')
                    if rights:
                        rights_set.add(rights)
                        distribution_to_rights.append((distribution_id, rights))
                    format = get_resource_format(resource.get('media_type'), resource.get('format'), resource.get('download_url'))
                    if format:
                        format_set.add(format)
                        distribution_to_format.append((distribution_id, format))
    with open('rights.csv', "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=['term', 'right'])
        writer.writeheader()
        for item in rights_set:
            writer.writerow({
                'term': terms_of_use_mapping.get(item),
                'right': item,
            })
    with open('formats.csv', "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=['format'])
        writer.writeheader()
        for item in format_set:
            writer.writerow({
                'format': item,
            })
    with open('distributions_to_rights.csv', "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=['distribution_id', 'term'])
        writer.writeheader()
        for item in distribution_to_rights:
            writer.writerow({
                'distribution_id': item[0],
                'term': terms_of_use_mapping.get(item[1]),
            })
    with open('distributions_to_formats.csv', "w") as csvfile:
        writer = DictWriter(csvfile, fieldnames=['distribution_id', 'format'])
        writer.writeheader()
        for item in distribution_to_format:
            writer.writerow({
                'distribution_id': item[0],
                'format': item[1],
            })


def prepare_resource_format(resource):
    """determine resource format depending on
    media_type, format and download_url
    """
    resource['format'] = get_resource_format(
        media_type=resource.get('media_type'),
        format=resource.get('format'),
        download_url=resource.get('download_url')
    )
    return resource


def get_resource_format(media_type, format, download_url):
    """the format of the resource is derived in the following way:
    the first matching case is taken
    - case 1 media_type is set and matches as format
             from the format list: this format will be taken
    - case 2 format is set: check whether the format is already mapped
             or whether it can be mapped
    - case 3 download url is set: check if the format can be derived
             from the file extention, otherwise if the media type is
             set and valid take the media type as format, otherwise
             set it as blank
    - case 4 no download url: set the format to SERVICE
    """
    if media_type:
        cleaned_media_type = _get_cleaned_format_or_media_type(media_type)
        format_from_media_type = _map_to_valid_format(cleaned_media_type)
        if format_from_media_type:
            return format_from_media_type

    if format:
        format_from_format = _map_to_valid_format(format, try_to_clean=True)
        if format_from_format:
            return format_from_format

    if download_url:
        format_from_file_extension = _get_format_from_path(download_url)
        if format_from_file_extension:
            return format_from_file_extension
        elif media_type:
            return cleaned_media_type
        return ""

    return 'SERVICE'


def prepare_formats_for_index(resources):
    """generates a set with formats of all resources"""
    formats = set()
    for r in resources:
        resource = prepare_resource_format(
            resource=r
        )
        if resource['format']:
            formats.add(resource['format'])
        else:
            formats.add('N/A')

    return list(formats)


def _map_to_valid_format(format, try_to_clean=False):
    """check whether the format if in the mapping:
    either as a key or as a value or if it can be derived
    after cleaning the input format string"""
    if format in format_mapping.keys():
        return format

    if format in reverse_format_mapping.keys():
        return reverse_format_mapping[format]
    if try_to_clean:
        cleaned_format = _get_cleaned_format_or_media_type(format)
        if cleaned_format in reverse_format_mapping.keys():
            return reverse_format_mapping[cleaned_format]
    return ""


def _get_cleaned_format_or_media_type(format):
    """clean the format"""
    if format:
        cleaned_format = format.split('/')[-1].lower()
        if cleaned_format:
            return cleaned_format
    return ""


def _get_format_from_path(download_url):
    """check whether the format can be derived from the file
    extension"""
    path = urlparse(download_url).path
    ext = os.path.splitext(path)[1]
    if ext:
        resource_format = ext.replace('.', '').lower()
        return _map_to_valid_format(resource_format)
    return ""
