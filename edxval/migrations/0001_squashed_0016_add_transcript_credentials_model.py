# Generated by Django 2.2.11 on 2020-04-10 17:42

import django.core.validators
from django.db import migrations, models
import django.db.migrations.operations.special
import django.db.models.deletion
import django.utils.timezone
import edxval.models
import fernet_fields.fields
import model_utils.fields


# This copied fields from one column to another, then deleted the original column.
# I merged these operations such that the model is created without the deleted column.
# Therefore, this data migration is not needed.
# edxval.migrations.0013_thirdpartytranscriptcredentialsstate_copy_values

DEFAULT_PROFILES = [
    "audio_mp3",
    "hls",
    "desktop_mp4",
    "desktop_webm",
    "mobile_high",
    "mobile_low",
    "youtube",
]


def create_default_profiles(apps, schema_editor):
    """ Add default profiles """
    # Adds profiles for: 0002_data__default_profiles, 0004_data__add_hls_profile, 0011_data__add_audio_mp3_profile
    Profile = apps.get_model("edxval", "Profile")
    for profile in DEFAULT_PROFILES:
        Profile.objects.get_or_create(profile_name=profile)


def delete_default_profiles(apps, schema_editor):
    """ Remove default profiles """
    Profile = apps.get_model("edxval", "Profile")
    Profile.objects.filter(profile_name__in=DEFAULT_PROFILES).delete()


class Migration(migrations.Migration):

    replaces = [('edxval', '0001_initial'), ('edxval', '0002_data__default_profiles'), ('edxval', '0003_coursevideo_is_hidden'), ('edxval', '0004_data__add_hls_profile'), ('edxval', '0005_videoimage'), ('edxval', '0006_auto_20171009_0725'), ('edxval', '0007_transcript_credentials_state'), ('edxval', '0008_remove_subtitles'), ('edxval', '0009_auto_20171127_0406'), ('edxval', '0010_add_video_as_foreign_key'), ('edxval', '0011_data__add_audio_mp3_profile'), ('edxval', '0012_thirdpartytranscriptcredentialsstate_has_creds'), ('edxval', '0013_thirdpartytranscriptcredentialsstate_copy_values'), ('edxval', '0014_transcript_credentials_state_retype_exists'), ('edxval', '0015_remove_thirdpartytranscriptcredentialsstate_exists'), ('edxval', '0016_add_transcript_credentials_model')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_name', models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator(code='invalid profile_name', message='profile_name has invalid characters', regex='^[a-zA-Z0-9\\-_]*$')])),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edx_video_id', models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator(code='invalid edx_video_id', message='edx_video_id has invalid characters', regex='^[a-zA-Z0-9\\-_]*$')])),
                ('client_video_id', models.CharField(blank=True, db_index=True, max_length=255)),
                ('duration', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('status', models.CharField(db_index=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='EncodedVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('url', models.CharField(max_length=200)),
                ('file_size', models.PositiveIntegerField()),
                ('bitrate', models.PositiveIntegerField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='edxval.Profile')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='encoded_videos', to='edxval.Video')),
            ],
        ),
        migrations.CreateModel(
            name='CourseVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=255)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='edxval.Video')),
            ],
            options={
                'unique_together': {('course_id', 'video')},
            },
            bases=(models.Model, edxval.models.ModelFactoryWithValidation),
        ),
        migrations.AddField(
            model_name='coursevideo',
            name='is_hidden',
            field=models.BooleanField(default=False, help_text='Hide video for course.'),
        ),
        migrations.CreateModel(
            name='VideoImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('image', edxval.models.CustomizableImageField(blank=True, null=True)),
                ('generated_images', edxval.models.ListField()),
                ('course_video', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='video_image', to='edxval.CourseVideo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TranscriptPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('course_id', models.CharField(max_length=255, unique=True, verbose_name='Course ID')),
                ('provider', models.CharField(choices=[('Custom', 'Custom'), ('3PlayMedia', '3PlayMedia'), ('Cielo24', 'Cielo24')], max_length=20, verbose_name='Provider')),
                ('cielo24_fidelity', models.CharField(blank=True, choices=[('MECHANICAL', 'Mechanical, 75% Accuracy'), ('PREMIUM', 'Premium, 95% Accuracy'), ('PROFESSIONAL', 'Professional, 99% Accuracy')], max_length=20, null=True, verbose_name='Cielo24 Fidelity')),
                ('cielo24_turnaround', models.CharField(blank=True, choices=[('STANDARD', 'Standard, 48h'), ('PRIORITY', 'Priority, 24h')], max_length=20, null=True, verbose_name='Cielo24 Turnaround')),
                ('three_play_turnaround', models.CharField(blank=True, choices=[('extended', '10-Day/Extended'), ('standard', '4-Day/Standard'), ('expedited', '2-Day/Expedited'), ('rush', '24 hour/Rush'), ('same_day', 'Same Day'), ('two_hour', '2 Hour')], max_length=20, null=True, verbose_name='3PlayMedia Turnaround')),
                ('preferred_languages', edxval.models.ListField(blank=True, default=[], max_items=50, verbose_name='Preferred Languages')),
                ('video_source_language', models.CharField(blank=True, help_text='This specifies the speech language of a Video.', max_length=50, null=True, verbose_name='Video Source Language')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VideoTranscript',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('transcript', edxval.models.CustomizableFileField(blank=True, null=True)),
                ('language_code', models.CharField(db_index=True, max_length=50)),
                ('provider', models.CharField(choices=[('Custom', 'Custom'), ('3PlayMedia', '3PlayMedia'), ('Cielo24', 'Cielo24')], default='Custom', max_length=30)),
                ('file_format', models.CharField(choices=[('srt', 'SubRip'), ('sjson', 'SRT JSON')], db_index=True, max_length=20)),
                ('video', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='video_transcripts', to='edxval.Video')),
            ],
            options={
                'unique_together': {('video', 'language_code')},
            },
        ),
        migrations.CreateModel(
            name='ThirdPartyTranscriptCredentialsState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('org', models.CharField(max_length=32, verbose_name='Course Organization')),
                ('provider', models.CharField(choices=[('Custom', 'Custom'), ('3PlayMedia', '3PlayMedia'), ('Cielo24', 'Cielo24')], max_length=20, verbose_name='Transcript Provider')),
            ],
            options={
                'unique_together': {('org', 'provider')},
            },
        ),
        migrations.AddField(
            model_name='thirdpartytranscriptcredentialsstate',
            name='has_creds',
            field=models.BooleanField(default=False, help_text='Transcript credentials state'),
        ),
        migrations.CreateModel(
            name='TranscriptCredentials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('org', models.CharField(help_text='This value must match the value of organization in studio/edx-platform.', max_length=50, verbose_name='Organization')),
                ('provider', models.CharField(choices=[('Custom', 'Custom'), ('3PlayMedia', '3PlayMedia'), ('Cielo24', 'Cielo24')], max_length=50, verbose_name='Transcript provider')),
                ('api_key', fernet_fields.fields.EncryptedTextField(max_length=255, verbose_name='API key')),
                ('api_secret', fernet_fields.fields.EncryptedTextField(max_length=255, verbose_name='API secret')),
            ],
            options={
                'verbose_name_plural': 'Transcript Credentials',
                'unique_together': {('org', 'provider')},
            },
        ),
        migrations.RunPython(
            code=create_default_profiles,
            reverse_code=delete_default_profiles,
        ),
    ]