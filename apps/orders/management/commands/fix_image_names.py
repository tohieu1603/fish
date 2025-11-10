"""
Management command to rename all existing order images with Vietnamese characters
to ASCII-safe filenames.
"""
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.orders.models import OrderImage
from apps.orders.models.order import order_image_upload_path


class Command(BaseCommand):
    help = 'Rename all order images to ASCII-safe filenames'

    def handle(self, *args, **options):
        images = OrderImage.objects.all()
        total = images.count()
        renamed = 0
        errors = 0

        self.stdout.write(f"Found {total} images to process...")

        for img in images:
            try:
                if not img.image:
                    continue

                # Get current file path
                old_path = img.image.path
                old_name = os.path.basename(old_path)

                # Check if file has Vietnamese characters
                if old_name.isascii():
                    self.stdout.write(f"  Skipping {old_name} (already ASCII)")
                    continue

                # Generate new safe filename
                new_relative_path = order_image_upload_path(img, old_name)
                new_path = os.path.join(settings.MEDIA_ROOT, new_relative_path)

                # Create directory if not exists
                os.makedirs(os.path.dirname(new_path), exist_ok=True)

                # Check if old file exists
                if not os.path.exists(old_path):
                    self.stdout.write(self.style.WARNING(
                        f"  File not found: {old_path}"
                    ))
                    continue

                # Rename/move the file
                os.rename(old_path, new_path)

                # Update database
                img.image.name = new_relative_path
                img.save(update_fields=['image'])

                renamed += 1
                self.stdout.write(self.style.SUCCESS(
                    f"  ✓ Renamed: {old_name} -> {os.path.basename(new_path)}"
                ))

            except Exception as e:
                errors += 1
                self.stdout.write(self.style.ERROR(
                    f"  ✗ Error processing {img.id}: {str(e)}"
                ))

        self.stdout.write(self.style.SUCCESS(
            f"\nCompleted! Renamed: {renamed}, Errors: {errors}, Total: {total}"
        ))
