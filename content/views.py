from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpRequest
from .models import MediaContent, Comment, ViewLog
from .forms import CommentForm
from django.contrib import messages  # Yuqoriga qo‘sh


def get_client_ip(request: HttpRequest):
    """
    Foydalanuvchining IP manzilini aniqlovchi funksiya.
    Reverse proxy yoki Nginx bilan ishlaganda 'HTTP_X_FORWARDED_FOR' dan foydalaniladi.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def home(request):
    """
    Asosiy sahifa view:
    - Faqat faol va chop etilgan kontentlar chiqadi.
    - Har bir foydalanuvchi har bir kontentni faqat 1 marta ko‘rgan deb hisoblanadi.
    - Fikr (comment) qo‘shish ham shu yerda ishlanadi.
    """
    # Faqat faol va chop etilgan kontentlarni olish
    contents = MediaContent.objects.filter(
        is_active=True,
        publish_time__lte=timezone.now()
    ).order_by('-publish_time')

    # Foydalanuvchi IP manzilini olish
    user_ip = get_client_ip(request)

    # Har bir kontent uchun foydalanuvchi oldin ko‘rganmi – tekshiramiz
    for item in contents:
        if not ViewLog.objects.filter(content=item, ip_address=user_ip).exists():
            # Yangi foydalanuvchi bo‘lsa — ko‘rildi deb logga yozamiz
            ViewLog.objects.create(content=item, ip_address=user_ip)
            # Ko‘rilganlar sonini 1 taga oshiramiz
            item.views_count += 1
            item.save()

    # Fikr (comment) formasi ishlovchi qism
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            content_id = request.POST.get('content_id')
            comment.content = get_object_or_404(MediaContent, id=content_id)
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()

    # Templatega ma'lumotlar jo‘natiladi
    return render(request, 'content/home.html', {
        'contents': contents,
        'form': form
    })


def delete_content(request, pk):
    """
    Kontentni o‘chirish view. Faqat POST so‘rovlarda ishlaydi.
    """
    content = get_object_or_404(MediaContent, pk=pk)
    if request.method == 'POST':
        content.delete()
        messages.success(request, "Kontent muvaffaqiyatli o‘chirildi.")
        return redirect('home')

    return render(request, 'content/confirm_delete.html', {'content': content})
