from rest_framework import serializers
from .models import Customer, Profession, Document, DataSheet


class DataSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSheet
        fields = ('id', 'description', 'historical_data')


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'dtype', 'doc_num', 'customer')


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('id', 'description')


class CustomerSerializer(serializers.ModelSerializer):
    num_professions = serializers.SerializerMethodField()
    data_sheet = DataSheetSerializer(read_only=True)  # nested serializer
    
    # StringRelatedField calls __str__ on data_sheet obj and shows result
    # many=True required for any field that can have multiple values like fk or many-to-many fields
    # document_set = serializers.StringRelatedField(many=True)    # document has customer fk so the relation
    document_set = DocumentSerializer(many=True, read_only=True)
    # profession = serializers.PrimaryKeyRelatedField(many=True)
    profession = ProfessionSerializer(many=True)
    
    
    class Meta:
        model = Customer
        fields = ('id', 'name', 'addr', 'profession_titles', 'data_sheet',
                  'active', 'num_professions', 'document_set', 'profession',)
        
    def create(self, validated_data):
        profession = validated_data['profession']
        del validated_data['profession']
        
        customer = Customer.objects.create(**validated_data)
        
        for p in profession:
            prof = Profession.objects.create(**p)
            customer.profession.add(prof)
        
        customer.save()
        return customer
    
    def get_num_professions(self, obj):
        return obj.num_profs()
