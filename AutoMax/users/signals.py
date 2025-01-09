from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Profile, Location

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a Profile instance when a new User is created.
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Profile)
def create_profile_location(sender, instance, created, **kwargs):
    """
    Automatically create and assign a Location instance to a Profile when created.
    """
    if created and not instance.location:
        profile_location = Location.objects.create()
        # Use update instead of save to prevent triggering signals again
        Profile.objects.filter(pk=instance.pk).update(location=profile_location)

@receiver(post_delete, sender=Profile)
def delete_profile_location(sender, instance, **kwargs):
    """
    Automatically delete the Location instance when a Profile is deleted.
    """
    if instance.location:
        instance.location.delete()
