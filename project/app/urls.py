from django.urls import path
from . import views

urlpatterns = [
    # ==================== COMMON ROUTES ====================
    path("", views.IndexPage, name="index"),

    # User Registration & OTP
    path("signUp/", views.SignUpPage, name="signUp"),
    path("register/", views.RegisterUser, name="register"),
    path("otppage/", views.OtpPage, name="otppage"),
    path("otp/", views.Otpverify, name="otp"),

    # Authentication
    path("loginpage/", views.LoginPage, name="loginpage"),
    path("loginuser/", views.LoginUser, name="login"),

    # Profile
    path("profile/<int:pk>/", views.ProfilePage, name="profile"),
    path("updateprofile/<int:pk>/", views.UpdateProfile, name="updateprofile"),

    # Logout
    path("candidatelogout/", views.CandidateLogout, name="candidatelogout"),

    # ==================== CANDIDATE ROUTES ====================
    path("joblist/", views.CandidateJobListPage, name="joblist"),
    path("apply/<int:pk>/", views.Applypage, name="apply"),
    path("applyjob/<int:pk>/", views.ApplyJob, name="applyjob"),
    path("applyjoblist/", views.JobApplyList, name="applylist"),  # Admin/global

    # Resume Request + Payment
    path("resume/request/", views.Request_resume_view, name="build_resume"),
    path("resume/payment/", views.Resume_payment_view, name="resume_payment"),
    path("resume/confirm/", views.Confirm_resume_payment, name="confirm_resume_payment"),

    # ==================== COMPANY ROUTES ====================
    path("companyindex/", views.CompanyIndexPage, name="companyindex"),
    path("companyprofile/<int:pk>/", views.CompanyProfilePage, name="companyprofile"),
    path("updatecompanyprofile/<int:pk>/", views.UpdateCompanyProfile, name="updatecompanyprofile"),
    path("jobpostpage/", views.JobPostPage, name="jobpostpage"),
    path("jobpost/", views.JobDetailSubmit, name="jobpost"),
    path("companylogout/", views.CompanyLogout, name="companylogout"),

    # Company View Only Their Posts and Applications
    path("company/jobposts/", views.CompanyJobPostList, name="company_jobposts"),
    path("company/applications/", views.CompanyApplicationList, name="company_applications"),

    # ==================== ADMIN ROUTES ====================
    path("jobpostlistpage/", views.JobListPage, name="joblistpage"),  # ✅ admin/global job post list

    path("adminloginpage/", views.AdminLoginPage, name="adminloginpage"),
    path("adminlogin/", views.AdminLogin, name="adminlogin"),
    path("adminindex/", views.AdminIndexPage, name="adminindex"),
    path("adminuserlist/", views.AdminUserList, name="userlist"),
    path("admincompanylist/", views.AdminCompanyList, name="admincompanylist"),
    path("deletecandidate/<int:pk>/", views.DeleteCandidate, name="deletecandidate"),
    path("deletecompany/<int:pk>/", views.DeleteCompany, name="deletecompany"),
    path("verifycompanypage/<int:pk>/", views.VerifyCompanyPage, name="verifypage"),

    # Admin: Job posts and applications
    path("admin/jobposts/", views.AdminJobPostList, name="admin_jobposts"),
    path("admin/applications/", views.AdminApplyList, name="admin_applylist"),
]
