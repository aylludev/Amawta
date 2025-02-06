from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    related_notes = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ['code', 'title', 'related_notes']

    def get_related_notes(self, obj):
        return [note.code for note in obj.related_notes.all()]
