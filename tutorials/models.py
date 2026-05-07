from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
from django.urls import reverse
from django.utils.crypto import get_random_string

class Subject(models.Model):
    # Core Fields
    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=50, help_text="FontAwesome class (e.g., fa-code)")
    image = models.ImageField(upload_to='subjects/', blank=True, null=True)
    description = models.TextField(max_length=300, blank=True)
    
    # Status & Ordering
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Home page-er top section-e dekhabe")
    order = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def total_topics(self):
        return self.topics.filter(is_published=True).count()

    def __str__(self):
        return self.name

class Topic(models.Model):
    # Difficulty Levels
    DIFFICULTY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)
    content = CKEditor5Field('Text', config_name='extends')
    
    # Meta Information
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='Beginner')
    is_published = models.BooleanField(default=True)
    short_description = models.CharField(max_length=255, blank=True)
    
    # Interaction
    views_count = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0) # Simple like counter
    
    # SEO & Timeline
    meta_keywords = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(max_length=160, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    order = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True, max_length=255)

    class Meta:
        ordering = ['order', 'created_at']
        unique_together = ('subject', 'slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            # Slug jodi same hoye jay, tobe random string add korbe
            base_slug = slugify(self.title)
            if Topic.objects.filter(slug=base_slug).exists():
                self.slug = f"{base_slug}-{get_random_string(4)}"
            else:
                self.slug = base_slug
        super().save(*args, **kwargs)

    # Next/Prev Logic
    def get_next_topic(self):
        return Topic.objects.filter(subject=self.subject, order__gt=self.order, is_published=True).first()

    def get_previous_topic(self):
        return Topic.objects.filter(subject=self.subject, order__lt=self.order, is_published=True).last()

    def __str__(self):
        return f"{self.subject.name} - {self.title}"
        
    def get_absolute_url(self):
        """
        Dynamically generates the URL for a specific topic detail page.
        """
        return reverse('tutorial_detail', kwargs={
            'subject_slug': self.subject.slug, 
            'topic_slug': self.slug
        })

# --- Extra Add-on: FAQ Section ---
# Protiti tutorial-er niche FAQ thakle SEO-te khub help hoy
class TopicFAQ(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question