import os
from pathlib import Path

from django.shortcuts import render, redirect
from viewer.forms import TiffFileForm
from viewer.models import TiffFile
from viewer.utils import convert_to_dzi
from wsi_viewer import settings


def upload_and_view(request):
    if request.method == 'POST':
        form = TiffFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            file_stem = Path(instance.uploaded_file.name).stem
            relative_dzi_path = os.path.join('dzi_files', file_stem + '.dzi')

            full_dzi_path = os.path.join(settings.MEDIA_ROOT, relative_dzi_path)
            convert_to_dzi(instance.uploaded_file.path, Path(full_dzi_path).parent / file_stem)
            instance.dzi_file = relative_dzi_path
            instance.save()

            return redirect('view_dzi', instance.id)
    else:
        form = TiffFileForm()
    return render(request, 'upload.html', {'form': form})


def view_dzi(request, tif_id):
    tif_instance = TiffFile.objects.get(id=tif_id)
    abs_dzi_path = os.path.join(settings.MEDIA_URL, tif_instance.dzi_file)
    return render(request, 'view.html', {'dzi_path': abs_dzi_path})
