from django import forms
from students.models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'className', 'phone', 'address', 
                  'math', 'physics', 'chemistry']