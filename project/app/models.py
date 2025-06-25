from django.db import models

class UserMaster(models.Model):
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    otp = models.IntegerField()
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

class Candidate(models.Model):
    user_id = models.ForeignKey(UserMaster, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    contact = models.CharField(max_length=50, default="Not Provided")
    state = models.CharField(max_length=50, default="Not Specified")
    city = models.CharField(max_length=50, default="Not Specified")
    address = models.CharField(max_length=250, default="Not Provided")
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, default="Not Specified")
    job_type = models.CharField(max_length=50, default="Not Specified")
    jobcategory = models.CharField(max_length=50, default="Not Specified")
    max_salary = models.BigIntegerField(blank=True, null=True)
    min_salary = models.BigIntegerField(blank=True, null=True)
    country = models.CharField(max_length=100, default="India")
    education = models.CharField(max_length=150, default="Not Specified")
    experience = models.CharField(max_length=150, default="Not Specified")

    # corrected
    resume = models.FileField(upload_to="app/resumes/", blank=True, null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"



class Company(models.Model):
    user_id = models.ForeignKey(UserMaster, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    companyname = models.CharField(max_length=50, default="Not Specified")
    state = models.CharField(max_length=50, default="Not Specified")
    city = models.CharField(max_length=50, default="Not Specified")
    contact = models.CharField(max_length=50, default="Not Provided")
    address = models.CharField(max_length=150, default="Not Provided")
    logo_pic = models.ImageField(upload_to="company_logos/", blank=True, null=True)


    def __str__(self):
        return self.companyname or f"{self.firstname} {self.lastname}"


class DetailsOfJob(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    jobname = models.CharField(max_length=250)
    jobdescription = models.TextField()
    qualification = models.CharField(max_length=250)
    responsibilities = models.TextField()
    location = models.CharField(max_length=250)
    salarypackage = models.CharField(max_length=250)
    experience = models.CharField(max_length=250)
    companyname = models.CharField(max_length=250)
    companyaddress = models.CharField(max_length=250)
    companywebsite = models.CharField(max_length=250)
    companyemail = models.EmailField(max_length=250)
    companycontact = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.jobname} at {self.companyname}"


class ApplyList(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    job = models.ForeignKey(DetailsOfJob, on_delete=models.CASCADE)
    education = models.CharField(max_length=200)
    experience = models.CharField(max_length=150)
    website = models.CharField(max_length=200, default="N/A")
    min_salary = models.IntegerField(null=True, blank=True)
    max_salary = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=200, default="Not Specified")
    resume = models.FileField(upload_to="app/resume")

    def __str__(self):
        return f"{self.candidate} -> {self.job}"
    

class ResumeRequest(models.Model):
    user_id = models.ForeignKey(UserMaster, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    education = models.TextField()
    skills = models.TextField()
    status = models.CharField(max_length=10, choices=[
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Done', 'Done'),
    ], default='Pending')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume request by {self.user.email}"
