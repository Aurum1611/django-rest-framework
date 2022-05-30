from rest_framework import serializers
from .models import Customer, Profession, Document, DataSheet


class CustomerSerializer(serializers.ModelSerializer):
    num_professions = serializers.SerializerMethodField()
    data_sheet = serializers.StringRelatedField()   # calls __str__ on data_sheet obj and shows result
    # many=True for any field that can have multiple values
    document_set = serializers.StringRelatedField(many=True)    # document has customer fk so the relation
    profession = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    
    class Meta:
        model = Customer
        fields = ('id', 'name', 'addr', 'profession_titles', 'data_sheet',
                  'active', 'num_professions', 'document_set', 'profession',)
    
    def get_num_professions(self, obj):
        return obj.num_profs()


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('id', 'description')


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'dtype', 'doc_num', 'customer')


class DataSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSheet
        fields = ('id', 'description', 'historical_data')
