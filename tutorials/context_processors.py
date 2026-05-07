from .models import Subject

def extras(request):
    # Ekhane amra sob subject-ke query korchi
    subjects = Subject.objects.all()
    return {
        'global_subjects': subjects,
    }
    
    
def global_subjects(request):
    return {
        'global_subjects': Subject.objects.filter(is_active=True).order_by('order')
    }