from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.template.defaultfilters import filesizeformat

IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp", "gif"]
DOCUMENT_EXTENSIONS = ["pdf", "doc", "docx", "xls", "xlsx", "jpg", "jpeg", "png"]

validate_image_extension = FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS)
validate_document_extension = FileExtensionValidator(allowed_extensions=DOCUMENT_EXTENSIONS)


def _validate_max_size(uploaded_file, max_mb):
    if uploaded_file.size > max_mb * 1024 * 1024:
        raise ValidationError(
            f"File is too large ({filesizeformat(uploaded_file.size)}). Maximum size is {max_mb} MB."
        )


def validate_image_size(uploaded_file):
    _validate_max_size(uploaded_file, 5)


def validate_document_size(uploaded_file):
    _validate_max_size(uploaded_file, 10)
