from django.contrib import admin
from django.utils.html import format_html
from .models import Subject, Topic, TopicFAQ

# --- Inline FAQ ---
class TopicFAQInline(admin.TabularInline):
    model = TopicFAQ
    extra = 1
    classes = ['collapse'] # Default-e hide hoye thakbe, click korle dekhabe

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    # Image preview dekhabe list section-e
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height:45px; border-radius: 50%;" />'.format(obj.image.url))
        return "No Image"
    image_tag.short_description = 'Icon'

    list_display = ('image_tag', 'name', 'order', 'is_active', 'is_featured', 'total_topics_count')
    list_editable = ('is_active', 'is_featured', 'order') # Admin list thekei change kora jabe
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_active', 'is_featured')

    def total_topics_count(self, obj):
        return obj.total_topics()
    total_topics_count.short_description = 'Topics'

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    inlines = [TopicFAQInline] # Topic create korar somoy FAQ nichei thakbe
    
    list_display = ('title', 'subject', 'difficulty', 'order', 'views_count', 'is_published', 'updated_at')
    list_editable = ('order', 'is_published', 'difficulty') # Quick edit feature
    list_filter = ('subject', 'difficulty', 'is_published', 'created_at')
    search_fields = ('title', 'content', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    
    # Textarea-gulo arektu boro hobe metadata-r jonno
    formfield_overrides = {
        # Models-e jodi TextField thake tar size adjust kora jay
    }

    # Action feature: Ekebare onekgulo post publish ba unpublish korar jonno
    actions = ['make_published', 'make_draft']

    @admin.action(description='Mark selected topics as Published')
    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description='Mark selected topics as Draft')
    def make_draft(self, request, queryset):
        queryset.update(is_published=False)

    # UI Optimization
    fieldsets = (
        ('Core Content', {
            'fields': ('subject', 'title', 'slug', 'content', 'short_description')
        }),
        ('Settings & SEO', {
            'fields': ('difficulty', 'order', 'is_published', 'meta_keywords', 'meta_description'),
            'classes': ('collapse',), # Section-ti hide thakbe
        }),
    )

@admin.register(TopicFAQ)
class TopicFAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'topic')
    search_fields = ('question', 'answer')