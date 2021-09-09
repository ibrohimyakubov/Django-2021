from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile, Skill
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data.get('password1') and data.get('password2'):
            if data['password1'] != data['password2']:
                raise serializers.ValidationError('Passwords must match.')
        return data

    def create(self, validated_data):
        print(validated_data)
        data = {
            key: value for key, value in validated_data.items()
            if key not in ('password1', 'password2')
        }
        data['password'] = validated_data['password1']
        data['username'] = validated_data['username']
        user = self.Meta.model.objects.create_user(**data)
        user.is_active = True
        user.save()
        return user

    class Meta:
        model = User
        exclude = ['password', 'is_superuser', 'user_permissions', 'groups', 'date_joined', 'first_name', 'last_name']
        read_only_fields = ('last_login', 'is_staff', 'is_superuser', 'is_active')
        write_only_fields = ('password1', 'password2')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['name', 'description', 'created']


class ProfileSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=True, source='skill_set')

    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'location', 'short_intro', 'bio', 'profile_image', 'social_github',
                  'social_twitter', 'social_linkedin', 'social_youtube', 'social_website', 'skill']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
