from django.shortcuts import render, HttpResponse,redirect, reverse
import google.generativeai as genai
import json, os


##gemini##########################################
############################################
# config.json 파일 경로
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(BASE_DIR, 'Gemini_config.json')

# config.json 파일 읽기
with open(config_path, 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

GOOGLE_API_KEY = config['GOOGLE_API_KEY']
model_id = config['model_id']
prompt = config['prompt']

genai.configure(api_key=GOOGLE_API_KEY)

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name=model_id,
  generation_config=generation_config,
)

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def process_file(file_path, prompt = prompt):
    # 예시로 파일을 업로드하고 처리 결과를 반환하는 함수
    uploaded_file = upload_to_gemini(file_path, mime_type="image/png")
    response = model.generate_content([uploaded_file, prompt])

    return response.text  # 결과를 저장할 형태로 반환

########################################################################################
########################################################################################
def index(request):
    return render(request, 'myapp/index.html')

def latest(request):
    list = UploadFile.objects.all().order_by('-pk')[0]
    return render( 
        request,
        'myapp/latest.html',
        {'file' : list})

from .forms import UploadFileForm
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            upload_file = form.save(commit=False)
            if request.FILES.get('file'):
                file_path = request.FILES['file'].temporary_file_path()
                output = process_file(file_path)
                upload_file.output = output
            upload_file.save()
            return redirect(reverse('myapp:latest'))
    else:
        form = UploadFileForm()
    return render(request, 'myapp/upload_form.html', {'form': form})
    
from .models import UploadFile
def file_list(request):
    list = UploadFile.objects.all().order_by('-pk')
    return render( 
        request,
        'myapp/file_list.html',
        {'list' : list})


from django.conf import settings
def delete_file(request, id):
    file = UploadFile.objects.get(pk=id)
    
    #media 파일에도 삭제
    media_root = settings.MEDIA_ROOT
    remove_file = media_root + "/" + str(file.file)
    print('삭제 : ', remove_file)

    if os.path.isfile(remove_file):
        os.remove(remove_file)
    
    #db에서 삭제
    file.delete()
    return redirect(reverse('myapp:list'))
        