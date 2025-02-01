
from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    previous_notes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Note
        fields = ['id', 'title', 'previous_notes']
