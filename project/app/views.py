from django.shortcuts import render,redirect
from random import randint
from .models import UserMaster, Candidate ,Company ,DetailsOfJob,ApplyList # Make sure to import your models
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import ResumeRequestForm
from .models import ResumeRequest
from django.http import Http404
import razorpay
from django.conf import settings
from django.core.mail import send_mail
import razorpay



# Create your views here.
# def IndexPage(request):
#     return render(request, "app/index.html")
def IndexPage(request):
    jobs = DetailsOfJob.objects.all()
    return render(request, "app/index.html", {"all_jobs": jobs})


def SignUpPage(request):
    return render(request, "app/signup.html")

def RegisterUser(request):
    if request.method == "POST":
        role = request.POST.get('role')  # Use .get() to avoid KeyError

        if role == "Candidate":
            fname = request.POST.get('firstname')
            lname = request.POST.get('lastname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            cpassword = request.POST.get('cpassword')

            user = UserMaster.objects.filter(email=email).first()

            if user:
                message = "User already exists!"
                return render(request, "app/signup.html", {'msg': message})
            else:
                if password == cpassword:
                    otp = randint(1000, 9999)
                    newuser = UserMaster.objects.create(role=role, otp=otp, email=email, password=password)
                    newcand = Candidate.objects.create(user_id=newuser, firstname=fname, lastname=lname)
                    return render(request, "app/otpverify.html", {'email': email})
                else:
                    message = "Passwords do not match!"
                    return render(request, "app/signup.html", {'msg': message})

        elif role == "Company":
            fname = request.POST.get('firstname')
            lname = request.POST.get('lastname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            cpassword = request.POST.get('cpassword')

            user = UserMaster.objects.filter(email=email).first()

            if user:
                message = "User already exists!"
                return render(request, "app/signup.html", {'msg': message})
            else:
                if password == cpassword:
                    otp = randint(1000, 9999)
                    newuser = UserMaster.objects.create(role=role, otp=otp, email=email, password=password)
                    newcomp = Company.objects.create(user_id=newuser, firstname=fname, lastname=lname)
                    return render(request, "app/otpverify.html", {'email': email})
                else:
                    message = "Passwords do not match!"
                    return render(request, "app/signup.html", {'msg': message})
        else:
            # Role not provided or unknown role
            message = "Please select a valid role"
            return render(request, "app/signup.html", {'msg': message})
    else:
        # If GET request or others, redirect to signup page
        return render(request, "app/signup.html")
                    
def OtpPage(request):
    return render(request,"app/otpverify.html")

def Otpverify(request):
    if request.method == "POST":
        email = request.POST.get('email')
        otp = request.POST.get('otp')

        if not email or not otp:
            message = "Missing email or OTP."
            return render(request, "app/otpverify.html", {'msg': message})

        try:
            otp = int(otp)
            user = UserMaster.objects.get(email=email)  #Tries to find a user in the database with the given email. If the user doesn't exist, it raises UserMaster.DoesNotExist.
            if user.otp == otp:
                message = "OTP verified successfully!"
                return render(request, "app/login.html", {'msg': message})
            else:
                message = "OTP is incorrect!"
                return render(request, "app/otpverify.html", {'msg': message, 'email': email})
        except (UserMaster.DoesNotExist, ValueError):  #Handles cases where:1.The email doesn't match any user (DoesNotExist),2.OTP conversion to integer fails (ValueError)
            message = "Invalid request or user not found!"
            return render(request, "app/signup.html", {'msg': message})
    else:
        return redirect("signUp")

       

def LoginPage(request):
    return render(request,"app/login.html")

def LoginUser(request):
    if request.method == "POST":
        role = request.POST.get('role')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if role == "Candidate":
            try:
                user = UserMaster.objects.get(email=email)

                if user.password == password and user.role == "Candidate":
                    can = Candidate.objects.get(user_id=user)

                    # Set required session variables
                    request.session["id"] = user.id
                    request.session["candidate_id"] = can.id  #  Important for resume views
                    request.session["role"] = user.role
                    request.session["firstname"] = can.firstname
                    request.session["lastname"] = can.lastname
                    request.session["email"] = user.email

                    return redirect("index")  # Candidate homepage
                else:
                    message = "Password does not match or role is incorrect."
                    return render(request, "app/login.html", {'msg': message})

            except UserMaster.DoesNotExist:
                message = "User does not exist!"
                return render(request, "app/login.html", {'msg': message})

        elif role == "Company":
            try:
                user = UserMaster.objects.get(email=email)

                if user.password == password and user.role == "Company":
                    comp = Company.objects.get(user_id=user)

                    # Set company session variables
                    request.session["id"] = user.id
                    request.session["role"] = user.role
                    request.session["firstname"] = comp.firstname
                    request.session["lastname"] = comp.lastname
                    request.session["email"] = user.email

                    return redirect("companyindex")  # Company homepage
                else:
                    message = "Password does not match or role is incorrect."
                    return render(request, "app/login.html", {'msg': message})

            except UserMaster.DoesNotExist:
                message = "User does not exist!"
                return render(request, "app/login.html", {'msg': message})

        else:
            message = "Please select a valid role."
            return render(request, "app/login.html", {'msg': message})

    return render(request, "app/login.html")  # For GET request fallback



def ProfilePage(request, pk):
    user = UserMaster.objects.get(pk=pk)

    if user.role != "Candidate":
        raise Http404("Profile not found for this user.")

    try:
        can = Candidate.objects.get(user_id=user)
    except Candidate.DoesNotExist:
        raise Http404("Candidate profile not found.")

    return render(request, "app/profile.html", {'user': user, 'can': can})


def UpdateProfile(request, pk):
    user = get_object_or_404(UserMaster, pk=pk)

    if user.role == "Candidate":
        can = get_object_or_404(Candidate, user_id=user)

        if request.method == "POST":
            # Name fields
            can.firstname = request.POST.get("firstname")
            can.lastname = request.POST.get("lastname")

            # Contact
            contact = request.POST.get("contact")
            if not contact or not contact.isdigit() or len(contact) != 10:
                messages.error(request, "Contact number must be exactly 10 digits.")
                return redirect("profile", pk=pk)
            can.contact = contact

            # Gender, State, Address
            can.gender = request.POST.get("gender")
            can.state = request.POST.get("state")
            can.address = request.POST.get("address")

            # Job Preferences
            can.job_type = request.POST.get("jobtype")
            can.jobcategory = request.POST.get("jobcategory")
            can.education = request.POST.get("education")
            can.experience = request.POST.get("experience")

            # Location and Salary
            can.city = request.POST.get("city")
            can.country = request.POST.get("country")
            can.min_salary = request.POST.get("minsalary")
            can.max_salary = request.POST.get("maxsalary")

            # Resume Upload
            if 'resume' in request.FILES:
                can.resume = request.FILES['resume']

            # Save changes
            can.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile", pk=pk)
        
             # Auto-clean values for form display
        fields_to_clean = [
            "contact", "state", "city", "address", "gender",
            "job_type", "jobcategory", "education", "experience"
        ]
        for field in fields_to_clean:
            value = getattr(can, field)
            if value in [None, "", "Not Provided", "Not Specified"]:
                setattr(can, field, "")

        return render(request, "app/profile.html", {"user": user, "can": can})

    return redirect("loginpage")




def CandidateLogout(request):
    # Clear all session data
    request.session.flush()
    return redirect('index') 


def Applypage(request,pk):
    user = request.session['id']
    if user:
        cand = Candidate.objects.get(user_id=user)
        job = DetailsOfJob.objects.get(id=pk)
    return render(request,"app/apply.html",{'user':user,'cand':cand,'job':job})


def ApplyJob(request, pk):
    user_id = request.session.get('id')

    if user_id and request.method == 'POST':
        can = Candidate.objects.get(user_id=user_id)
        job = DetailsOfJob.objects.get(id=pk)

        edu = request.POST.get('education')
        exp = request.POST.get('experience')
        gender = request.POST.get('gender')
        resume = request.FILES.get('resume')
        min_salary = request.POST.get('min_salary')
        max_salary = request.POST.get('max_salary')

        # Save updates to candidate profile
        can.education = edu or can.education
        can.experience = exp or can.experience
        can.gender = gender or can.gender
        can.min_salary = min_salary or can.min_salary
        can.max_salary = max_salary or can.max_salary
        if resume:
            can.profile_pic = resume
        can.save()

        # Save application
        ApplyList.objects.create(
            candidate=can,
            job=job,
            education=edu,
            experience=exp,
            min_salary=min_salary,
            max_salary=max_salary,
            gender=gender,
            resume=resume
        )

        msg = "Job Applied Successfully!"
        return render(request, "app/apply.html", {
            'msg': msg,
            'user': user_id,
            'cand': can,
            'job': job
        })

    # fallback in case of error or GET
    return redirect('login')

# ================================ Resume Request Form Page ================================

def Request_resume_view(request):
    if not request.session.get('id'):
        return redirect('loginpage')  # Only logged-in candidates

    if request.method == 'POST':
        form = ResumeRequestForm(request.POST)
        if form.is_valid():
            resume_request = form.save(commit=False)
            user = UserMaster.objects.get(id=request.session['id'])  # ✅ from session
            resume_request.user_id = user
            resume_request.status = 'Pending'
            resume_request.save()
            request.session['resume_id'] = resume_request.id
            return redirect('resume_payment')
    else:
        form = ResumeRequestForm()

    return render(request, 'app/request_resume.html', {'form': form})


# ================================ Resume Payment Page ================================


def Resume_payment_view(request):
    resume_id = request.session.get('resume_id')
    if not resume_id:
        return redirect('build_resume')  # Go back to form

    amount = 299 * 100  # ₹299 in paise
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    context = {
        "payment": payment,
        "key_id": settings.RAZORPAY_KEY_ID,
        "amount_display": amount / 100,
        "resume_id": resume_id
    }

    return render(request, "app/resume_payment.html", context)

# ======================================== Confirm Payment and Update Status ==========================================

def Confirm_resume_payment(request):
    resume_id = request.session.get('resume_id')
    if not resume_id:
        return redirect('loginpage')

    resume_request = get_object_or_404(ResumeRequest, id=resume_id)
    resume_request.status = 'Paid'
    resume_request.save()

    user_email = resume_request.user_id.email

    send_mail(
        subject="Resume Payment Successful",
        message=f"Dear {user_email},\n\nYour payment is confirmed. We will send your resume soon.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False
    )

    return render(request, 'app/payment_done.html')


    # ========================== Company Side ==============================================
    
def CompanyIndexPage(request):
    return render(request,"app/company/index.html")  
    
def CompanyProfilePage(request, pk):
    user = get_object_or_404(UserMaster, pk=pk)
    if user.role != "Company":
        raise Http404("Not a company user.")
    try:
        comp = Company.objects.get(user_id=user)
    except Company.DoesNotExist:
        raise Http404("Company profile not found.")
    return render(request, "app/company/companyprofile.html", {'user': user, 'comp': comp})
   

def UpdateCompanyProfile(request, pk):
    user = get_object_or_404(UserMaster, id=pk)
    company = get_object_or_404(Company, user_id=user)

    if request.method == "POST":
        company.firstname = request.POST.get("firstname")
        company.lastname = request.POST.get("lastname")
        company.contact = request.POST.get("contact")
        company.state = request.POST.get("state")
        company.city = request.POST.get("city")
        company.address = request.POST.get("address")
        company.companyname = request.POST.get("companyname")

        if 'logo_pic' in request.FILES:
            company.logo_pic = request.FILES['logo_pic']

        company.save()

        #  Add success message
        messages.success(request, "Profile updated successfully!")

        return redirect('companyprofile', pk=user.id)

    return render(request, "app/company/updatecompanyprofile.html", {"company": company})

    
def JobPostPage(request):
    user_id = request.session.get('id')
    if user_id:
        user = UserMaster.objects.get(id=user_id)
        if user.role == "Company":
            company = Company.objects.get(user_id=user)
            return render(request, "app/company/jobpost.html", {'company': company})
    return redirect('loginpage')



def JobDetailSubmit(request):
    user_id = request.session.get('id')

    if not user_id:
        return render(request, "app/company/jobpost.html", {"msg": "Please log in first."})

    try:
        user = UserMaster.objects.get(id=user_id)
    except UserMaster.DoesNotExist:
        return render(request, "app/company/jobpost.html", {"msg": "User not found."})

    if user.role != "Company":
        return render(request, "app/company/jobpost.html", {"msg": "Access denied. Only companies can post jobs."})

    if request.method == "POST":
        comp = Company.objects.get(user_id=user)

        #  Handle company logo upload if provided
        if 'logo_pic' in request.FILES:
            comp.logo_pic = request.FILES['logo_pic']
            comp.save()

        jobname = request.POST.get('jobname')
        companyname = request.POST.get('companyname')
        companyemail = request.POST.get('companyemail')
        companycontact = request.POST.get('companycontact')
        companyaddress = request.POST.get('companyaddress')
        jobdescription = request.POST.get('jobdescription')
        qualification = request.POST.get('qualification')
        responsibilities = request.POST.get('responsibilities')
        location = request.POST.get('location')
        salarypackage = request.POST.get('salarypackage')
        experience = request.POST.get('experience')
        companywebsite = request.POST.get('companywebsite')

        # Create and save job post
        newjob = DetailsOfJob.objects.create(
            company=comp,
            jobname=jobname,
            companyname=companyname,
            companyaddress=companyaddress,
            jobdescription=jobdescription,
            qualification=qualification,
            responsibilities=responsibilities,
            location=location,
            companywebsite=companywebsite,
            companyemail=companyemail,
            companycontact=companycontact,
            salarypackage=salarypackage,
            experience=experience
        )

        message = "Job Posted Successfully!"
        return render(request, "app/company/jobpost.html", {'msg': message, 'company': comp})

    # GET request
    comp = Company.objects.get(user_id=user)
    return render(request, "app/company/jobpost.html", {'company': comp})

def JobListPage(request):
    all_jobs = DetailsOfJob.objects.all()
    return render(request, "app/admin/admin_jobpostlist.html", {"all_jobs": all_jobs})

def CandidateJobListPage(request):
    all_jobs = DetailsOfJob.objects.all()
    return render(request,"app/job-list.html",{"all_jobs": all_jobs})

def JobApplyList(request):
    if request.session.get("role") != "Company":
        return redirect("loginpage")

    try:
        company_id = request.session.get("id")
        all_jobapply = ApplyList.objects.filter(job__company__user_id=company_id)
        return render(request, "app/company/applyjoblist.html", {"all_job": all_jobapply})
    except Exception as e:
        print("Error in JobApplyList:", e)
        return redirect("companyindex")  # fallback page if something goes wrong


def CompanyLogout(request):
    request.session.flush()  # Clears the entire session
    return redirect('index')

def CompanyJobPostList(request):  # Company: View Only Their Job Posts
    if not request.session.get('id') or request.session.get('role') != 'Company':
        return redirect('loginpage')

    company = Company.objects.get(user_id=request.session['id'])
    all_jobs = DetailsOfJob.objects.filter(company=company)
    return render(request, "app/company/company_jobpostlist.html", {"all_jobs": all_jobs})

def CompanyApplicationList(request):  # Company: View Applications to Their Jobs
    if not request.session.get('id') or request.session.get('role') != 'Company':
        return redirect('loginpage')

    company = Company.objects.get(user_id=request.session['id'])
    jobs = DetailsOfJob.objects.filter(company=company)
    applications = ApplyList.objects.filter(job__in=jobs)
    return render(request, "app/company/company_applylist.html", {"applications": applications})



def CompanyApplicationList(request):
    if not request.session.get('id'):
        return redirect('loginpage')

    company = Company.objects.get(user_id=request.session['id'])
    jobs = DetailsOfJob.objects.filter(company=company)
    applications = ApplyList.objects.filter(job__in=jobs)

    return render(request, "app/company/applylist.html", {"applications": applications})

##################################### ADMIN SIDE ############################################## 

def AdminLoginPage(request):
    return render(request,"app/admin/login.html")

def AdminIndexPage(request):
    if 'username' in request.session and 'password' in request.session:
        return render(request,"app/admin/index.html")
    else:
        return redirect('adminloginpage')
    
    
from django.shortcuts import render, redirect

def AdminLogin(request):
    if request.method == "POST":
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username == "admin" and password == "admin":
            request.session['username'] = username
            request.session['password'] = password
            return redirect("adminindex")
        else:
            # This is your login failure handling
            print("Login failed!")
            message = "Username and password do not match!"
            return render(request, "app/admin/login.html", {'msg': message})
    else:
        return render(request, "app/admin/login.html")

def AdminUserList(request):
        all_user = UserMaster.objects.filter(role="Candidate")
        return render(request,"app/admin/userlist.html",{'all_user':all_user})
    
def AdminCompanyList(request):
        all_company = UserMaster.objects.filter(role="Company")
        return render(request,"app/admin/companylist.html",{'all_company':all_company})
    
def AdminJobPostList(request):  # Admin: View All Job Post
    if request.session.get('role') != 'Admin':
        return redirect('loginpage')  # secure access

    all_jobs = DetailsOfJob.objects.all()
    return render(request, "app/admin/admin_jobpostlist.html", {"all_jobs": all_jobs})


def AdminApplyList(request):  # Admin: View All Applications
    if request.session.get('role') != 'Admin':
        return redirect('loginpage')

    applications = ApplyList.objects.all()
    return render(request, "app/admin/admin_applylist.html", {"applications": applications})



    
def DeleteCandidate(request, pk):
    user = get_object_or_404(UserMaster, pk=pk, role="Candidate")
    email = user.email
    user.delete()
    messages.success(request, f"Candidate '{email}' deleted successfully.")
    return redirect("userlist")

def DeleteCompany(request, pk):
    user = get_object_or_404(UserMaster, pk=pk, role="Company")
    email = user.email
    user.delete()
    messages.success(request, f"Company '{email}' deleted successfully.")
    return redirect("admincompanylist")

def VerifyCompanyPage(request, pk):
    company = UserMaster.objects.get(pk=pk)

    if request.method == "POST":
        company.is_verified = request.POST.get("verify_status") == "True"
        company.save()
        messages.success(request, "Verification status updated successfully!")
        return redirect("admincompanylist")
    
    return render(request, "app/admin/verifycompanypage.html", {"company": company})
