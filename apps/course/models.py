from django.db import models
from django.conf import settings


class Category(models.Model):
    
    CATEGORY_CHOICES = [
        ('programacion', 'Programación y Desarrollo de Software'),
        ('data_science', 'Data Science e Inteligencia Artificial'),
        ('cloud_computing', 'Cloud Computing y DevOps'),
        ('ciberseguridad', 'Ciberseguridad'),
        ('diseno_ux_ui', 'Diseño y UX/UI'),
        ('startups', 'Startups'),
        ('finanzas', 'Finanzas e Inversiones'),
        ('ingles', 'Inglés'),
        ('habilidades_blandas', 'Habilidades Blandas'),
        ('videojuegos', 'Videojuegos'),
        ('hardware_robotica', 'Hardware, Robótica e IoT'),
        ('blockchain', 'Blockchain y Criptomonedas'),
        ('produccion_audiovisual', 'Producción Audiovisual y Contenido Digital'),
        ('marketing_digital', 'Marketing Digital'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='programacion')
    
    
    def __str__(self):
        return self.get_name_display()
    
    
    

class Course(models.Model):
    
    STATUS_CHOICES = [
        ('borrador', 'Borrador'),
        ('archivado', 'Archivado'),
        ('publicado', 'Publicado')
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    status =  models.CharField(max_length=20, choices=STATUS_CHOICES, default='borrador')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses_created')
    
    def __str__(self):
        return self.title



class Lesson(models.Model):
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    



class Enrollment(models.Model):
    
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('activo', 'Activo'), ('completado', 'Completado'), ('cancelado', 'Cancelado')],
        default='activo'
    )

    class Meta:
        unique_together = ('student', 'course')






class LessonProgress(models.Model):
    
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lessons_progress')
    progress = models.DecimalField(max_digits=5, decimal_places=2)
    completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'lesson')





class Review(models.Model):
    
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

