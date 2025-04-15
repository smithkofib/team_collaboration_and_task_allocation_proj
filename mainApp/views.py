# team_task_allocation_proj/mainApp/views.py

# Create your views here.

##### from .langChain_utils.chains import explain_task_allocation, explain_team_formation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from openai.error import APIConnectionError


from .models import (
    Candidate, SkillCategory, Skill, 
    CandidateSkill, WorkExperience, Education,
    CulturalFit, CandidateAssessment, CandidateFeedback, 
    Job, Departement, Staff, StaffDepartement
)
from .forms import (
    CandidateForm, SkillForm, WorkExperienceForm, EducationForm,
    CandidateAssessmentForm, CandidateFeedbackForm, JobForm,
    DepartementForm, StaffForm
)

from .langChain_utils import chains

def home(request):
    """Home Page"""
    return render(request, 'task_allocation/home.html')

### Candidate Views
### ------------------
### List All Candidates
def candidate_list(request):
    """List all candidates"""
    candidates = Candidate.objects.filter(approval="not_approved")
    educations = Education.objects.all()
    return render(request, 'task_allocation/candidates/candidate_list.html', {'candidates': candidates, 'educations': educations})

### Add A Candidate View
def add_candidate(request):
    """Add a new candidate"""
    if request.method == "POST":
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Candidate added successfully!")
            return redirect('candidate_list')
    else:
        form = CandidateForm()
    return render(request, 'task_allocation/candidates/add_candidate.html', {'form': form})

### View List of all uploaded Files
def file_list(request):
    files = Candidate.objects.values("id", "first_name", "last_name", "resume", "certificates")
    return render(request, 'task_allocation/load_files/file_list.html', {'files': files})

### view  A Candidate Details View
def view_candidate(request, candidate_id):
    """View candidate details"""
    candidate = get_object_or_404(Candidate, id=candidate_id)
    return render(request, 'task_allocation/candidates/view_candidate.html', {'candidate': candidate})

### Edit A Candidate View
def edit_candidate(request, candidate_id):
    """Edit candidate details"""
    candidate = get_object_or_404(Candidate, id=candidate_id)
    if request.method == "POST":
        form = CandidateForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, "Candidate updated successfully!")
            return redirect('candidate_list')
    else:
        form = CandidateForm(instance=candidate)
    return render(request, 'task_allocation/candidates/edit_candidate.html', {'form': form})

### Delete A Candidate View
def delete_candidate(request, candidate_id):
    """Delete a candidate"""
    candidate = get_object_or_404(Candidate, id=candidate_id)
    candidate.delete()
    messages.success(request, "Candidate deleted successfully!")
    return redirect('candidate_list')

### Approve A Candidate View
def approve_candidate(request, candidate_id, predicted_job):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    candidate.approval = "approved"
    candidate.role = predicted_job
    candidate.save(update_fields=['approval', 'role'])
    #Candidate.objects.filter(id=candidate_id).update(approval="approved")
    messages.success(request=request, message="Candidate has been approved successfully!")
    return redirect('approved_candidate_list')

#   Approved Candidates List
def approved_candidate_list(request):
    approved_candidates = Staff.objects.filter(candidate__approval="approved")
    #return JsonResponse(list(approved_candidates), safe=False)
    return render(request=request, template_name="task_allocation/candidates/candidate_approved_list.html", context={"approved_candidates" : approved_candidates})


### Skill Views
### ------------------
### List All Skills View
def skill_list(request):
    """List all skills"""
    skills = Skill.objects.all()
    return render(request, 'task_allocation/skills/skill_list.html', {'skills': skills})

### Add A Skill View
def add_skill(request):
    """Add a new skill"""
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill added successfully!")
            return redirect('skill_list')
    else:
        form = SkillForm()
    return render(request, 'task_allocation/skills/add_skill.html', {'form': form})

### Delete A Skill View
def delete_skill(request, skill_id):
    """Delete a skill"""
    skill = get_object_or_404(Skill, id=skill_id)
    skill.delete()
    messages.success(request, "Skill deleted successfully!")
    return redirect('skill_list')

### Registration Views
### ------------------
### Register A Canditate View
def register_candidatexxxxxxxxx(request, candidate_id):
    """ Register a candidate """
    print("Okay -kkkkkkkkkk")
    candidate = get_object_or_404(Candidate, id=candidate_id)
    if request.method == "POST":
        print("Okay -jjjjjjjj")
        educationform = EducationForm(request.POST)
        workExpform = WorkExperienceForm(request.POST)        
        if educationform.is_valid() & workExpform.is_valid():
            edu = educationform.save(commit=False)
            experience = workExpform.save(commit=False)
            
            edu.candidate = candidate
            experience.candidate = candidate 
            
            edu.save()
            experience.save()
            print("Okay -000000000000")
            messages.success(request, "Candidate registered successfully!")
            return redirect('register_list')
    else:
        workExpform = WorkExperienceForm()
        educationform = EducationForm()
    return render(request, 'task_allocation/registration/register_candidate.html', {'candidate': candidate, 'workExpform': workExpform, 'educationform': educationform})

### List All Canditates View
def register_list(request):
    """List All registered candidates"""
    candidate = Candidate.objects.filter(approval="not_approved")
    #education = Education.objects.filter(candidate=candidate)
    #workExp = WorkExperience.objects.filter(candidate=candidate)
    
    return render(request, 'task_allocation/registration/register_list.html', {'candidates': candidate})

### List A Canditates View
def candidate_register_details(request, candidate_id):
    """List registration details of a candidate"""
    candidate = get_object_or_404(Candidate, id=candidate_id)
    education = Education.objects.filter(candidate=candidate)
    workExp = WorkExperience.objects.filter(candidate=candidate)
    return render(request, 'task_allocation/registration/register_list.html', {'education': education, "workExp":workExp, 'candidate': candidate})

### Assessment Views
def assess_candidate(request, candidate_id):
    """Assess a candidate"""
    candidate = get_object_or_404(Candidate, id=candidate_id)
    if request.method == "POST":
        form = CandidateAssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.candidate = candidate
            assessment.save()
            messages.success(request, "Assessment completed!")
            return redirect('candidate_list')
    else:
        form = CandidateAssessmentForm()
    return render(request, 'task_allocation/assessments/assess.html', {'form': form, 'candidate': candidate})

### Feedback Views
def add_feedback(request, candidate_id):
    """Add feedback for a candidate"""
    candidate = get_object_or_404(Candidate, id=candidate_id)
    if request.method == "POST":
        form = CandidateFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.candidate = candidate
            feedback.save()
            messages.success(request, "Feedback added successfully!")
            return redirect('candidate_list')
    else:
        form = CandidateFeedbackForm()
    return render(request, 'task_allocation/feedback/add_feedback.html', {'form': form, 'candidate': candidate})

### Add Job
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = JobForm()
        return render(request=request, template_name="task_allocation/job/add_job.html", context={'from':form})

##### xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##### xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
##### xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

### xxxxxxxx Education Views
def education_list(request, candidate_id):
    """List education details of a candidate"""
    candidate = get_object_or_404(Candidate, id=candidate_id)
    education = Education.objects.filter(candidate=candidate)
    return render(request, 'task_allocation/education/list.html', {'education': education, 'candidate': candidate})

### xxxxxxxx
def add_education(request, candidate_id):
    """Add education details"""
    candidate = get_object_or_404(Candidate, id=candidate_id)
    if request.method == "POST":
        form = EducationForm(request.POST)
        if form.is_valid():
            edu = form.save(commit=False)
            edu.candidate = candidate
            edu.save()
            messages.success(request, "Education added successfully!")
            return redirect('education_list', candidate_id=candidate.id)
    else:
        form = EducationForm()
    return render(request, 'task_allocation/education/add.html', {'form': form, 'candidate': candidate})

### xxxxxxxx Work Experience Views
def work_experience_list(request, candidate_id):
    """List work experience of a candidate"""
    candidate = get_object_or_404(Candidate, id=candidate_id)
    experiences = WorkExperience.objects.filter(candidate=candidate)
    return render(request, 'task_allocation/work_experience/list.html', {'experiences': experiences, 'candidate': candidate})

### xxxxxxxx
def add_work_experience(request, candidate_id):
    """Add work experience"""
    candidate = get_object_or_404(Candidate, id=candidate_id)
    if request.method == "POST":
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.candidate = candidate
            experience.save()
            messages.success(request, "Work experience added!")
            return redirect('work_experience_list', candidate_id=candidate.id)
    else:
        form = WorkExperienceForm()
    return render(request, 'task_allocation/work_experience/add.html', {'form': form, 'candidate': candidate})

### LangChain predict job for a canditates view
def predict_job(request, candidate_id):
    """Predicting a job for a candidate"""
    try:
        candidate = get_object_or_404(Candidate, id=candidate_id)
        education = Education.objects.filter(candidate=candidate)
        workExp = WorkExperience.objects.filter(candidate=candidate)
        employee_fullname = candidate.first_name + " " + candidate.last_name
        employee_schools = list(map(lambda x : x, education))
        
        school_names = [y.institution_name for y in employee_schools]
        degrees = str([y.degree for y in education])
        fields_studied = [y.field_of_study for y in education]
        companies = [y.company_name for y in workExp]
        job_titles = [y.job_title for y in workExp]

        predicted_job = chains.predict_job_allocation(school_names, degrees, fields_studied, companies, job_titles)

        explanation = chains.explain_job_allocation(employee_fullname, school_names, degrees, fields_studied, companies, job_titles, predicted_job)
        print(explanation)
        return render(request, 'task_allocation/langChain/langChainResult.html', {'candidate': candidate, "predicted_job":predicted_job, "explanation":explanation})
    except APIConnectionError:
        return render(request, 'task_allocation/langChain/langChainAPIConnectionError.html', {"error":"Unable to connect to remote system. Please check your internet"})
    except Exception as e:
        return render(request, 'task_allocation/langChain/langChainAPIConnectionError.html', {"error":"Ununknown error occuired, please connacte the developer for assistance"})


### LangChain predict role for staffs within a department view
def predict_role(request, departement_id):
    """Predicting a role for a group of staffs"""
    if request.method == "POST":
        job_name = request.POST.get('job-name')
        job_description = request.POST.get('role-description-text')
    
        try:
            departement = get_object_or_404(Departement, id=departement_id)
            #staff = Staff.objects.filter(departement=departement)
            staff_ids = Staff.objects.filter(departement=departement).values_list("id", flat=True)

            workExp = WorkExperience.objects.filter(candidate__in=staff_ids)
            #staff_workExp = list(map(lambda x : x, workExp))

            staffs = Staff.objects.filter(candidate__in=staff_ids)
            #staffFullNames = list(map(lambda x : x, staff))

            """ for row1 in Staff.objects.filter(candidate__in=staff_ids).iterator():
                print(row2.institution_name, row1.dob) """

            education = {}
            work_exp = {}
            for edu, workExp in zip(Education.objects.filter(candidate__in=staff_ids).iterator(chunk_size=1), WorkExperience.objects.filter(candidate__in=staff_ids).iterator(chunk_size=1)):

                print (edu.candidate.first_name, edu.institution_name)
                print (workExp.company_name, workExp.job_title)
                education[edu.id] = {
                    "first_name": edu.candidate.first_name,
                    "last_name": edu.candidate.last_name,
                    "role": edu.candidate.role,

                    "institution_name": edu.institution_name,
                    "degree": edu.degree,
                    "field_of_study": edu.field_of_study,
                    "start_year": edu.start_year,
                    "end_year": edu.end_year
                }

                work_exp[workExp.id] = {
                    "job_title": workExp.job_title,
                    "company_name": workExp.company_name,
                    "start_date": workExp.start_date,
                    "end_date": workExp.end_date,
                    "responsibilities": workExp.responsibilities
                }

            predicted_candidate = chains.predict_role_allocation(eduction=education, working_experience=work_exp, position=job_name, job_description=job_description)
            predicted_role_explanation = chains.explain_role_allocation(position=job_name, predicted_employee=predicted_candidate)    
            print("-------------------------------------------------")
            #print("-------------------------- Education -----------------------")

            #print(education)
            #print(education[1]["institution_name"])
            #
            #print("-------------------------- Work Experience -----------------------")
            #print(work_exp)
            
            
            #print (staff_ids)
            #return JsonResponse({"r":"okayyyyyyyyyy"})
            return render(request, 'task_allocation/langChain/langChainPredictRole.html', {'position' : job_name, 'predicted_candidate': predicted_candidate, 'predicted_role_explanation': predicted_role_explanation})
        except APIConnectionError:
            return render(request, 'task_allocation/langChain/langChainAPIConnectionError.html', {"error":"Unable to connect to remote system. Please check your internet"})
            #return JsonResponse({"r":"dddd"})
        except Exception as e:
            #return render(request, 'task_allocation/langChain/langChainAPIConnectionError.html', {"error":"Ununknown error occuired, please connacte the developer for assistance"})
            return JsonResponse({"r":"kkkkkk", "e":e})
    else:
        return JsonResponse({"r":"kkkkkk"})
    
### LangChain predict role for staffs within a department view
def group_role_predict(request, departement_id):
    """Predicting a role for a group of staffs"""
    if request.method == "POST":
        job_name = request.POST.get('job-name')
        number_of_staffs = request.POST.get('number-of-staffs')
        gender = request.POST.get('gender')
        job_description = request.POST.get('role-description-text')
    
        try:
            departement = get_object_or_404(Departement, id=departement_id)
            #staff = Staff.objects.filter(departement=departement)
            staff_ids = Staff.objects.filter(departement=departement).values_list("id", flat=True)

            workExp = WorkExperience.objects.filter(candidate__in=staff_ids)
            #staff_workExp = list(map(lambda x : x, workExp))

            staffs = Staff.objects.filter(candidate__in=staff_ids)
            #staffFullNames = list(map(lambda x : x, staff))

            """ for row1 in Staff.objects.filter(candidate__in=staff_ids).iterator():
                print(row2.institution_name, row1.dob) """

            education = {}
            work_exp = {}
            for edu, workExp in zip(Education.objects.filter(candidate__in=staff_ids).iterator(chunk_size=1), WorkExperience.objects.filter(candidate__in=staff_ids).iterator(chunk_size=1)):

                print (edu.candidate.first_name, edu.institution_name)
                print (workExp.company_name, workExp.job_title)
                education[edu.id] = {
                    "first_name": edu.candidate.first_name,
                    "last_name": edu.candidate.last_name,
                    "role": edu.candidate.role,
                    "gender": edu.candidate.gender,

                    "institution_name": edu.institution_name,
                    "degree": edu.degree,
                    "field_of_study": edu.field_of_study,
                    "start_year": edu.start_year,
                    "end_year": edu.end_year
                }

                work_exp[workExp.id] = {
                    "job_title": workExp.job_title,
                    "company_name": workExp.company_name,
                    "start_date": workExp.start_date,
                    "end_date": workExp.end_date,
                    "responsibilities": workExp.responsibilities
                }

            predicted_candidate = chains.group_role_predict_allocation(eduction=education, working_experience=work_exp, position=job_name, number_of_staffs=number_of_staffs, gender=gender, job_description=job_description)
            predicted_role_explanation = chains.explain_group_role_allocation(position=job_name, predicted_employee=predicted_candidate)    
            print("-------------------------------------------------")
            #print("-------------------------- Education -----------------------")

            #print(education)
            #print(education[1]["institution_name"])
            #
            #print("-------------------------- Work Experience -----------------------")
            #print(work_exp)
            
            
            #print (staff_ids)
            #return JsonResponse({"r":"okayyyyyyyyyy"})
            return render(request, 'task_allocation/langChain/langChainPredictGroupRole.html', {'position' : job_name, 'predicted_candidate': predicted_candidate, 'predicted_role_explanation': predicted_role_explanation})

        except APIConnectionError:
            return render(request, 'task_allocation/langChain/langChainAPIConnectionError.html', {"error":"Unable to connect to remote system. Please check your internet"})
            #return JsonResponse({"r":"dddd"})
        except Exception as e:
            #return render(request, 'task_allocation/langChain/langChainAPIConnectionError.html', {"error":"Ununknown error occuired, please connacte the developer for assistance"})
            return JsonResponse({"r":"kkkkkk", "e":e})
    else:
        return JsonResponse({"r":"kkkkkk"})

### Add A Departement View
def add_departement(request):
    """Add a new departement"""
    if request.method == 'POST':
        form = DepartementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request=request, message="Departement created successfully!")
            return redirect('departement_list')
        else:
            messages.error(request=request, message='Faild to create departement')
    else:
        form = DepartementForm()
    return render(request=request, template_name='task_allocation/departement/add_departement.html', context={"form":form})

# List All Deparements View
def departement_list(request):
    departement = Departement.objects.all()
    return render(request=request, template_name='task_allocation/departement/departement_list.html', context={"departements": departement})

# List All Staffs In A Departement View
def departement_staff_list(request, departement_id):
    departement = get_object_or_404(Departement, id=departement_id)
    #staffs = Staff.objects.filter(departement=departement)
    staffs = Staff.objects.filter(departement__id=departement_id)

    return render(request=request, template_name="task_allocation/departement/departement_staff_list.html", context={"staffs": staffs, "departement": departement})

# Delete A Departement View
def delete_departement(request, departement_id):
    departement = get_object_or_404(Departement, id=departement_id)
    departement.delete()
    messages.success(request=request, message="Departement deleted successfully!")
    return redirect('departement_list')

# Add A Staff View
def add_staff(request):
    #candidate = get_object_or_404(Candidate, id=candidate_id)
    #education = Education.objects.filter(candidate=candidate)
    #workExp = WorkExperience.objects.filter(candidate=candidate)

    if request.method == "POST":
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request=request, message="Staff created successfully!")
            return redirect('staff_list')
        else:
            messages.error(request=request, message="Faild to create staff")
    else:
        form = StaffForm()
    return render(request=request, template_name="task_allocation/staff/add_staff.html", context={'form':form})

# List All Staff View
def staff_list(request):
    staffs = Staff.objects.all()
    return render(request=request, template_name="task_allocation/staff/staff_list.html", context={'staffs': staffs})

# List All Staff View
def gender_filtering(request):
    gender = request.GET.get("gender")
    staffs = Staff.objects.filter(candidate__gender=gender)
    return render(request=request, template_name="task_allocation/staff/staff_list.html", context={'staffs': staffs})

# Delete A Staff View
def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    staff.delete()
    messages.success(request=request, message="Staff deleted successfully!")
    return redirect('staff_list')

# Staff Detail View
def staff_detail(request, staff_id):
    staff_detail  = get_object_or_404(Staff, id=staff_id)
    #staff_education = get_object_or_404(Education, candidate__id=staff_id)
    staff_education = Education.objects.filter(candidate__id=staff_id)
    data = {
        "first_name": staff_detail.candidate.first_name,
        "last_name": staff_detail.candidate.last_name,
        "dob": staff_detail.dob,
        "email": staff_detail.candidate.email,
        "phone": staff_detail.candidate.phone,
        "candidate_approval": staff_detail.candidate.approval,
        "departement_name": staff_detail.departement.departement_name,
        "departement_phone": staff_detail.departement.departement_phone,        
        "departement_room_number": staff_detail.departement.departement_room_number,
        "gender": staff_detail.candidate.gender,
        "role": staff_detail.candidate.role,
        "educations": {
                        "name":[y.institution_name for y in staff_education],
                        "degree":[y.degree for y in staff_education],
                        "field":[y.field_of_study for y in staff_education],
                        "start":[y.start_year for y in staff_education],
                        "end":[y.end_year for y in staff_education]
                       } 

    }
    return JsonResponse(data)

# Edit A Staff View
def staff_edit(request, staff_id, candidate_id):
    print(staff_id, "  >>  ", candidate_id)
    staff = get_object_or_404(Staff, id=staff_id)
    candidate = get_object_or_404(Candidate, id=candidate_id)
    if request.method == "POST":
        form = StaffForm(request.POST, instance=staff)
        candidate_form = CandidateForm(request.POST, instance=candidate)
        if form.is_valid():
            candidate_form.save()
            form.save()
            messages.success(request=request, message="Staff updated successfully!")
            return redirect('staff_list')
    else:
        form = StaffForm(instance=staff)
        candidate_form = CandidateForm(instance=candidate)
    return render(request=request, template_name="task_allocation/staff/edit_staff.html", context={'form': form, "candidate_form": candidate_form})