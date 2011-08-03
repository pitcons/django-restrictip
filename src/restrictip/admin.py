
from django.contrib import admin
from models import Rule, RuleItem

class RuleItemInline(admin.TabularInline):
    model = RuleItem
    extra = 1

class RuleItemAdmin(admin.ModelAdmin):
    pass

class RuleAdmin(admin.ModelAdmin):
    list_display = ('path', 'policy', 'weight')
    ordering = ('weight', )
    inlines = [
        RuleItemInline,
    ]

admin.site.register(Rule, RuleAdmin)
