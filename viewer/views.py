import os
from pathlib import Path

from django.shortcuts import render, redirect, get_object_or_404
from viewer.forms import UploadFileForm
from viewer.models import UploadedFile
from viewer.utils import convert_to_dzi
from wsi_viewer import settings



def upload_and_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            file_stem = Path(instance.uploaded_file.name).stem
            relative_dzi_path = os.path.join('dzi_files', file_stem + '.dzi')

            full_dzi_path = os.path.join(settings.MEDIA_ROOT, relative_dzi_path)
            convert_to_dzi(instance.uploaded_file.path, Path(full_dzi_path).parent / file_stem)
            instance.dzi_file = relative_dzi_path
            instance.save()

            return redirect('view_file', instance.id)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def view_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    return render(request, 'view.html', {'file': file})


def list_files(request):
    # Query all UploadedFile objects that have a .dzi file associated
    files = UploadedFile.objects.filter(dzi_file__isnull=False)

    return render(request, 'list_files.html', {'files': files})
