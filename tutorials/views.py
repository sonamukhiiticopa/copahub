from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Subject, Topic

def home(request):
    """
    Landing page jekhane featured subjects ebong search bar thakbe.
    """
    featured_subjects = Subject.objects.filter(is_active=True, is_featured=True)
    all_subjects = Subject.objects.filter(is_active=True)
    
    # Search Logic
    query = request.GET.get('q')
    search_results = None
    if query:
        search_results = Topic.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            is_published=True
        ).distinct()

    context = {
        'featured_subjects': featured_subjects,
        'all_subjects': all_subjects,
        'search_results': search_results,
        'query': query,
    }
    return render(request, 'tutorials/home.html', context)

def tutorial_detail(request, subject_slug, topic_slug):
    """
    Main tutorial page jekhane sidebar-e topics ebong main area-te content thakbe.
    """
    subject = get_object_or_404(Subject, slug=subject_slug, is_active=True)
    topic = get_object_or_404(Topic, slug=topic_slug, subject=subject, is_published=True)
    
    # Topic list for Sidebar
    topics = subject.topics.filter(is_published=True).order_by('order')
    
    # View Count Logic (Simple)
    topic.views_count += 1
    topic.save(update_fields=['views_count'])
    
    # Next & Previous Topics
    next_topic = topic.get_next_topic()
    prev_topic = topic.get_previous_topic()

    context = {
        'subject': subject,
        'topic': topic,
        'topics': topics,
        'next_topic': next_topic,
        'prev_topic': prev_topic,
        # FAQ gulo template-e topic.faqs.all diye access kora jabe
    }
    return render(request, 'tutorials/detail.html', context)

def subject_list(request):
    """
    Sokol subject-er list (Landing page for all courses).
    """
    subjects = Subject.objects.filter(is_active=True).order_by('order')
    return render(request, 'tutorials/subject_list.html', {'subjects': subjects})