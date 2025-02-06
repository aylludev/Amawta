from django.db import models
from django.forms import model_to_dict

# Modelo para Autores
class Author(models.Model):
    
    name = models.CharField(max_length=100)
    
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
        item["author"] = [" "+name.name for name in self.author.all()]
        return item
    
    def __str__(self):
        return self.title

#Modelo para Notas 
class Note(models.Model):
    """Represents a note in the Zettelkasten system."""
    title = models.CharField(max_length=255, null=True)
    content = models.TextField()
    source = models.ForeignKey(Source, null=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="notes")

    def __str__(self):
        return f"{self.code} - {self.title}"

    def toJSON(self):
        item = model_to_dict(self, exclude=["created_at", "updated_at"])
        item['source'] = self.source.title if self.source else None 
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


