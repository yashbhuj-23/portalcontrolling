from django.contrib import admin
from .models import UserMaster, Candidate, Company, DetailsOfJob, ApplyList,ResumeRequest

@admin.register(UserMaster)
class UserMasterAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'is_active', 'is_verified', 'created_at', 'updated_at')
    search_fields = ('email', 'role')
    list_filter = ('role', 'is_verified')
    ordering = ('-created_at',)

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'user_id', 'contact', 'education', 'experience')
    search_fields = ('firstname', 'lastname', 'contact', 'jobcategory')
    list_filter = ('job_type', 'jobcategory', 'education')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'user_id', 'companyname', 'state', 'city','logo_pic')
    search_fields = ('companyname', 'city', 'state')

@admin.register(DetailsOfJob)
class DetailsOfJobAdmin(admin.ModelAdmin):
    list_display = ('jobname', 'companyname', 'location', 'salarypackage', 'experience')
    search_fields = ('jobname', 'companyname', 'location')
    list_filter = ('location', 'experience')

@admin.register(ApplyList)
class ApplyListAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'education', 'experience', 'gender', 'min_salary', 'max_salary')
    search_fields = ('candidate__firstname', 'job__jobname')
    list_filter = ('education', 'experience', 'gender')

@admin.register(ResumeRequest)
class ResumeRequestAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'firstname', 'contact', 'status', 'created')  # ✅ All valid fields


