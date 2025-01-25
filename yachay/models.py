from django.db import models
from django.forms import model_to_dict
# Modelo para Etiquetas
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    
    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return self.name


# Modelo para Autores
class Author(models.Model):
    TYPE_CHOICES = [
        ('BOOK', 'Book'),
        ('ESSAY', 'Essay'),
        ('ARTICLE', 'Article'),
        ('VIDEO', 'Video'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=100)
    source = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='OTHER')

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


# Modelo para Notas
class Note(models.Model):
    content = models.TextField()
    zettel_id = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    resource = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Note {self.zettel_id}"
    
    def toJSON(self):
        item = model_to_dict(self)
        return item


# Modelo para la relación many-to-many entre Note y Tag
class NoteTag(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="note_tags")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="note_tags")
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de asociación

    def __str__(self):
        return f"Tag '{self.tag.name}' for Note '{self.note.zettel_id}'"


# Modelo para Multimedia
class Media(models.Model):
    FILE_TYPE_CHOICES = [
        ('IMAGE', 'Image'),
        ('VIDEO', 'Video'),
        ('DOCUMENT', 'Document'),
        ('OTHER', 'Other'),
    ]

    file_path = models.FileField(upload_to='media_files/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES, default='OTHER')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="media_files")

    def __str__(self):
        return f"{self.file_path} ({self.get_file_type_display()})"
