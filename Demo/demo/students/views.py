from django.shortcuts import get_object_or_404, render, redirect
from .forms import StudentForm
from .models import Student
from .decorators import login_required_custom

# Create your views here.
@login_required_custom
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            return redirect('students_list')
    else:
        form = StudentForm()
    return render(request, 'add_Student.html', {'form': form})

@login_required_custom
def students_list(request):
    return render(request, 'students_list.html', {'students': Student.objects.all()})

@login_required_custom
def update_student(request, id):
    student = get_object_or_404(Student, studentID=id)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save()
            return redirect('students_list')
    else:
        form = StudentForm(instance=student)
        
    return render(request, 'update_student.html', {'form': form, 'student': student})

@login_required_custom
def delete_student(request, id):
    student = get_object_or_404(Student, studentID=id)
    if request.method == 'POST':
        student.delete()
        return redirect('students_list')
    return render(request, 'confirm_delete_student.html', {'student': student})