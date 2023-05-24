from rest_framework_mongoengine import serializers
from .models import Officer, User, Appointment
from services.bytes_conversion import to_bytes32, from_bytes32

class OfficerSerializer(serializers.Serializer):
    id = serializers.CharField()
    designation = serializers.CharField()
    department = serializers.CharField()
    zone = serializers.CharField()
    role = serializers.CharField() 

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["id"] = to_bytes32(data["id"])
        data["designation"] = data["designation"]
        data["zone"] = data["zone"]
    
    def to_internal_value(self, data):
        if isinstance(data, tuple):
            data = self.to_dict(data)
        id = from_bytes32(data.get('id', ''))
        designation = data.get('designation', '')
        zone = data.get('zone', '')
        role = [role for role in data.get('role', [])]
        _data = {
            'id': id,
            'designation': designation,
            'role': role,
            'zone': zone
        }
        print("formatted data is ")
        print(_data)
        return _data
    
    # def to_dict(self, data: List):


    

    
    

