from django.db import models
from django.forms import model_to_dict
from django.utils.timezone import now

# Modelo para Autores
class Author(models.Model):
    
    name = models.CharField(max_length=100)
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return self.name

# Modelo para Lineas
class Line(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return self.name

# Modelo para Etiquetas
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return self.name

#Modelo para Notas 
class Note(models.Model):
    """Represents a note in the Zettelkasten system."""
    code = models.CharField(max_length=20, unique=True, blank=True)  # Auto-generated
    title = models.CharField(max_length=255, null=True)
    content = models.TextField()
    author = models.ForeignKey(Author, null=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    line = models.ManyToManyField(Line, blank=True, related_name="tags")
    tags = models.ManyToManyField(Tag, blank=True, related_name="notes")

    def save(self, *args, **kwargs):
        """Automatically generates a unique code before saving the note."""
        if not self.code:
            today_str = now().strftime("%Y%m%d")
            last_note = Note.objects.filter(code__startswith=today_str).order_by('-code').first()
            last_id = int(last_note.code.split("-")[1]) + 1 if last_note else 1
            self.code = f"{today_str}-{last_id}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.code} - {self.title}"

    def toJSON(self):
        item = model_to_dict(self, exclude=["created_at", "updated_at"])
        if self.line:
            item["line"] = [" "+line.name for line in self.line.all()]
        item["tags"] = [" "+tag.name for tag in self.tags.all()]
        return item

#Modelo de links entre Notas
class NoteLink(models.Model):
    """Represents directed relationships between notes (source → target)."""
    source = models.ForeignKey(Note, related_name='next_notes', on_delete=models.PROTECT)
    target = models.ForeignKey(Note, related_name='previous_notes', on_delete=models.PROTECT)

    class Meta:
        unique_together = ('source', 'target')  # Prevent duplicate links

    def __str__(self):
        return f"{self.source} → {self.target}"

    def toJSON(self):
        item = model_to_dict(self)
        return item

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

# Modelo para fuentes
class Source(models.Model):
    TYPE_CHOICES = [
        ('BOOK', 'Book'),
        ('ESSAY', 'Essay'),
        ('ARTICLE', 'Article'),
        ('VIDEO', 'Video'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='OTHER')
    author = models.ManyToManyField(Author, blank=True, related_name="author")
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

